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
from clueai.match import Match, Matches, Score
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
        self.text_2_image_api_url = clueai.TEXT_TO_IMAGE_URL
        self.clueai_api_url = clueai.CLUEAI_API_URL
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

    def upload_finetune_corpus(
        self,
        file_path: str,
        input_field: str = "input",
        target_field: str = "output",
        headers: dict = {},
        model_name: str = None,
        sync: bool = True
        ):
        tmp_headers = {
            'Api-Key': 'BEARER {}'.format(self.api_key),
            'Content-Type': 'application/json',
            'Request-Source': 'python-sdk',
            'Model-name': model_name
        }
        if self.modelfun_version != '':
            tmp_headers['clueai-Version'] = self.modelfun_version
        data_json = {
            "input_field": input_field,
            "target_field": target_field
        }
        files = {'file': open(file_path,'rb')}
        tmp_headers.update(headers)

        is_sync = "sync/" if sync else ""
        res = requests.post(f"{self.clueai_api_url}/finetune/upload/{is_sync}",
            files=files, data=data_json, headers=headers)
        return res.json()

    def start_finetune_model(self,
        engine_key: str,
        headers: dict = {}):
        json_body = {
            'engine_key': engine_key,
        }
        tmp_headers = {
            'Api-Key': 'BEARER {}'.format(self.api_key),
            'Content-Type': 'application/json',
            'Request-Source': 'python-sdk',
        }
        if self.modelfun_version != '':
            tmp_headers['clueai-Version'] = self.modelfun_version
        tmp_headers.update(headers)

        finished_train_res = requests.post(f"{self.clueai_api_url}/finetune/finished/", json=json_body, headers=headers)
        finished_train_res = finished_train_res.json()
        if "finished" not in finished_train_res or finished_train_res["finished"] != True:
            return (f"还未完成训练，请稍后：{finished_train_res}")
        else:
            print("已经训练完成, 正在启动中, 预计需要等待20s...")

        res = requests.post(f"{self.clueai_api_url}/finetune/start/", json=json_body, headers=headers)
        res_dict = res.json()

        return "启动成功" if res_dict["start"] else "启动失败"

    def finetune_generate(
        self,
        engine_key: str,
        prompt: str,
        model_name: str = None,
        return_likelihoods: str = None,
        headers: dict = {},
        generate_config: dict = {}
    ) -> Generations:
        json_body = {
            'engine_key': engine_key,
            'task_type': "generate",
            'model_name': model_name,
            'input_data': [prompt],
            'return_likelihoods': return_likelihoods,
            'generate_config': generate_config
        }
        tmp_headers = {
            'Api-Key': 'BEARER {}'.format(self.api_key),
            'Content-Type': 'application/json',
            'Request-Source': 'python-sdk',
            'Model-name': model_name
        }
        if self.modelfun_version != '':
            tmp_headers['clueai-Version'] = self.modelfun_version
        tmp_headers.update(headers)
        response = requests.post(f"{self.clueai_api_url}/finetune/predict/", json=json_body, headers=headers)
        response = response.json()
        generations: List[Generation] = []
        if "result" not in response:
            raise ClueaiError(f'No result in response, please check or try. error{response}')
        for gen in response['result']:
            likelihood = None
            token_likelihoods = None
            if return_likelihoods == 'GENERATION' or return_likelihoods == 'ALL':
                likelihood = gen['likelihood']
            if 'token_likelihoods' in gen.keys():
                token_likelihoods = []
                for index, likelihoods in gen['token_likelihoods'].items():
                    token_likelihoods.append(
                        TokenLikelihood(likelihoods['token'], likelihoods["prob"]))
            generations.append(Generation(prompt,
                gen['generate_text'], likelihood, token_likelihoods))
        return Generations(generations, return_likelihoods)

    def upload_corpus(
        self,
        file_path: str,
        field: str,
        headers: dict = {},
        model_name: str = None,
        sync: bool = False
        ):
        tmp_headers = {
            'Api-Key': 'BEARER {}'.format(self.api_key),
            'Content-Type': 'application/json',
            'Request-Source': 'python-sdk',
            'Model-name': model_name
        }
        if self.modelfun_version != '':
            tmp_headers['clueai-Version'] = self.modelfun_version
        data_json = {
            "field": field
        }
        files = {'file': open(file_path,'rb')}
        tmp_headers.update(headers)

        is_sync = "sync/" if sync else ""
        res = requests.post(f"{self.clueai_api_url}/search/upload/{is_sync}",
            files=files, data=data_json, headers=headers)
        return res.json()

    def search(
        self, 
        query: str,
        engine_key: str,
        headers: dict = {},
        model_name: str = None
        ):
        tmp_headers = {
            'Api-Key': 'BEARER {}'.format(self.api_key),
            'Content-Type': 'application/json',
            'Request-Source': 'python-sdk',
            'Model-name': model_name
        }
        if self.modelfun_version != '':
            tmp_headers['clueai-Version'] = self.modelfun_version
        tmp_headers.update(headers)
        response = requests.get(f"{self.clueai_api_url}/search/?key={engine_key}&query={query}",
            headers=tmp_headers)
        response = response.json()
        result =  response['result']
        scoreObj = []
        for answer, score in result['answer_score'].items():
            scoreObj.append(Score(
                answer, float(score)
                ))


        match_instance = Match(result['query'], result['best_answer'], scoreObj)
            

        return Matches([match_instance])

    def text2image(
        self,
        prompt: str,
        model_name: str = None,
        style: str="",
        out_file_path: str="test.png", 
        headers: dict = {}
        ) -> None:
        url = f"{self.text_2_image_api_url}?text={prompt}"
        if style:
            url = f"{self.text_2_image_api_url}?text={style}风格，{prompt}"
        
        tmp_headers = {
            'Api-Key': 'BEARER {}'.format(self.api_key),
            'Content-Type': 'application/json',
            'Request-Source': 'python-sdk',
            'Model-name': model_name
        }
        if self.modelfun_version != '':
            tmp_headers['clueai-Version'] = self.modelfun_version
        tmp_headers.update(headers)
        response = requests.get(url, headers=tmp_headers)
        img = response.content
        with open(out_file_path, "wb") as f:
            f.write(img)

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
        return_likelihoods: str = None,
        headers: dict = {},
        generate_config: dict = {}
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
            'return_likelihoods': return_likelihoods,
            'generate_config': generate_config
        }, ensure_ascii=False)
        response = self.__request(json_body, clueai.GENERATE_URL, model_name, headers=headers)
        generations: List[Generation] = []
        if "result" not in response:
            raise ClueaiError(f'No result in response, please check or try. error{response}')
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

    def __request(self, json_body, endpoint, model_name, headers={}) -> Any:
        tmp_headers = {
            'Api-Key': 'BEARER {}'.format(self.api_key),
            'Content-Type': 'application/json',
            'Request-Source': 'python-sdk',
            'Model-name': model_name
        }
        if self.modelfun_version != '':
            tmp_headers['clueai-Version'] = self.modelfun_version
        tmp_headers.update(headers)
        url = urljoin(self.api_url, endpoint)
        #print(json_body)
        if use_xhr_client:
            response = self.__pyfetch(url, tmp_headers, json_body)
            return response
        else:
            response = requests.post(url, json=json.loads(json_body), headers=tmp_headers)
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
