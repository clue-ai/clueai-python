import json
from pyexpat import model
from typing import List, Any
from urllib import response
from urllib.parse import urljoin

import math

import requests
from requests import Response

from concurrent.futures import ThreadPoolExecutor

import clueai
from clueai.embeddings import Embeddings
from clueai.error import ClueaiError
from clueai.generation import Generations, Generation, TokenLikelihood
from clueai.tokenize import Tokens
from clueai.classify import Classifications, Classification, Example as ClassifyExample, Confidence
from clueai.extract import Entity, Example as ExtractExample, Extraction, Extractions

use_xhr_client = False
try:
    from js import XMLHttpRequest
    use_xhr_client = True
except ImportError:
    pass

use_go_tokenizer = False
try:
    from clueai.tokenizer import tokenizer
    use_go_tokenizer = True
except ImportError:
    pass


class Client:
    def __init__(
        self,
        api_key: str,
        version: str = None,
        num_workers: int = 8,
        request_dict: dict = {},
        check_api_key: bool = True
    ) -> None:
        self.api_key = api_key
        self.api_url = clueai.MODELFUN_API_URL
        self.num_workers = num_workers
        self.request_dict = request_dict
        if version is None:
            self.modelfun_version = clueai.MODELFUN_VERSION
        else:
            self.modelfun_version = version

        if check_api_key:
            try:
                res = self.check_api_key()
                if not res['valid']:
                    raise ClueaiError('invalid api key')
            except ClueaiError as e:
                raise ClueaiError(
                    message=e.message,
                    http_status=e.http_status,
                    headers=e.headers)

    def check_api_key(self) -> Response:
        headers = {
            'Api-Key': 'BEARER {}'.format(self.api_key),
            'Content-Type': 'application/json',
            'Request-Source': 'python-sdk',
        }
        if self.modelfun_version != '':
            headers['clueai-Version'] = self.modelfun_version

        url = urljoin(self.api_url, clueai.CHECK_API_KEY_URL)
        if use_xhr_client:
            response = self.__pyfetch(url, headers, None)
            return response
        else:
            response = requests.request('POST', url, headers=headers)

        try:
            res = json.loads(response.text)
        except Exception:
            raise ClueaiError(
                message=response.text,
                http_status=response.status_code,
                headers=response.headers)
        if 'message' in res.keys():  # has errors
            raise ClueaiError(
                message=res['message'],
                http_status=response.status_code,
                headers=response.headers)
        return res

    def generate(
        self,
        prompt: str,
        model_name: str = None,
        num_generations: int = 1,
        max_tokens: int = 20,
        temperature: float = 1.0,
        k: int = 0,
        p: float = 0.75,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        stop_sequences: List[str] = None,
        return_likelihoods: str = None
    ) -> Generations:
        json_body = json.dumps({
            'task_type': "generate",
            'model_name': model_name,
            'input_data': [prompt],
            'num_generations': num_generations,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'k': k,
            'p': p,
            'frequency_penalty': frequency_penalty,
            'presence_penalty': presence_penalty,
            'stop_sequences': stop_sequences,
            'return_likelihoods': return_likelihoods
        }, ensure_ascii=False)
        response = self.__request(json_body, clueai.GENERATE_URL, model_name)
        #print(f"res: {response}")
        generations: List[Generation] = []
        for gen in response['result']:
            likelihood = None
            token_likelihoods = None
            if return_likelihoods == 'GENERATION' or return_likelihoods == 'ALL':
                likelihood = gen['likelihood']
            if 'token_likelihoods' in gen.keys():
                token_likelihoods = []
                for index, likelihoods in gen['token_likelihoods'].items():
                    token_likelihood = likelihoods['token'] if 'token' in likelihoods.keys() else None
                    token_likelihoods.append(
                        TokenLikelihood(likelihoods['token'], likelihoods["prob"]))
            generations.append(Generation(prompt,
                gen['generate_text'], likelihood, token_likelihoods))
        return Generations(generations, return_likelihoods)

    def classify(
        self,
        inputs: List[str],
        labels:  List[str] = [],
        model_name: str = None,
        examples: List[ClassifyExample] = [],
        task_name: str = '',
    ) -> Classifications:
        examples_dicts: list[dict[str, str]] = []
        for example in examples:
            example_dict = {'text': example.text, 'label': example.label}
            examples_dicts.append(example_dict)

        json_body = json.dumps({
            'model_name': model_name,
            'task_name': task_name,
            'task_type': "classify",
            'examples': examples_dicts,
            'input_data': inputs,
            'labels': labels
        }, ensure_ascii=False)
        response = self.__request(json_body, clueai.CLASSIFY_URL, model_name)
        classifications = []
        for res in response['result']:
            confidenceObj = []
            for i in range(len(res['confidence'])):
                confidenceObj.append(Confidence(
                    res['confidence'][i]['label'],
                    res['confidence'][i]['confidence']))
            Classification(res['input'], res['prediction'], confidenceObj)
            classifications.append(Classification(
                res['input'], res['prediction'], confidenceObj))

        return Classifications(classifications)

    def unstable_extract(
        self,
        examples: List[ExtractExample],
        texts: List[str]
    ) -> Extractions:
        '''
        Makes a request to the clueai API to extract entities from a list of texts.
        Takes in a list of clueai.extract.Example objects to specify the entities to extract.
        Returns an clueai.extract.Extractions object containing extractions per text.
        '''

        json_body = json.dumps({
            'texts': texts,
            'examples': [ex.toDict() for ex in examples],
        })
        response = self.__request(json_body, clueai.EXTRACT_URL)
        extractions = []

        for res in response['results']:
            extraction = Extraction(**res)
            extraction.entities = []
            for entity in res['entities']:
                extraction.entities.append(Entity(**entity))

            extractions.append(extraction)

        return Extractions(extractions)

    def tokenize(self, text: str) -> Tokens:
        if (use_go_tokenizer):
            encoder = tokenizer.NewFromPrebuilt('modelfuntext-50k')
            goTokens = encoder.Encode(text)
            tokens = []
            for token in goTokens:
                tokens.append(token)
            return Tokens(tokens)
        else:
            json_body = json.dumps({
                'text': text,
            })
            response = self.__request(json_body, clueai.TOKENIZE_URL)
            return Tokens(response['tokens'])

    def __pyfetch(self, url, headers, json_body) -> Response:
        req = XMLHttpRequest.new()
        req.open('POST', url, False)
        for key, value in headers.items():
            req.setRequestHeader(key, value)
        try:
            req.send(json_body)
        except Exception:
            raise ClueaiError(
                message=req.responseText,
                http_status=req.status,
                headers=req.getAllResponseHeaders())
        res = json.loads(req.response)
        if 'message' in res.keys():
            raise ClueaiError(
                message=res['message'],
                http_status=req.status,
                headers=req.getAllResponseHeaders())
        return res

    def __request(self, json_body, endpoint, model_name) -> Any:
        headers = {
            'Api-Key': 'BEARER {}'.format(self.api_key),
            'Content-Type': 'application/json',
            'Request-Source': 'python-sdk',
            'Model-name': model_name
        }
        if self.modelfun_version != '':
            headers['clueai-Version'] = self.modelfun_version

        url = urljoin(self.api_url, endpoint)
        #print(json_body)
        if use_xhr_client:
            response = self.__pyfetch(url, headers, json_body)
            return response
        else:
            response = requests.post(url, json=json.loads(json_body), headers=headers)
            try:
                res = json.loads(response.text)
            except Exception:
                raise ClueaiError(
                    message=response.text,
                    http_status=response.status_code,
                    headers=response.headers)
            if 'message' in res.keys():  # has errors
                raise ClueaiError(
                    message=res['message'],
                    http_status=response.status_code,
                    headers=response.headers)
        return res
