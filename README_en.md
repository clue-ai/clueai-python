
<p align="center">
<br>
<br>
<br>
<img src="https://www.modelfun.cn/assets/logo.57d43a51.png" alt="CLUEAI logo: The data structure for unstructured data" width="200px">
<br>
<br>
<br>
<b>Making NLP part of every developer's toolkit. </b>
</p>


<p align=center>
<a href=""> <img src="https://img.shields.io/badge/language-python3.6+-brightgreen.svg?style=plastic"></a>
<a href="https://pypi.org/project/clueai/"><img src="https://img.shields.io/badge/pypi-0.0.0.1-brightgreen.svg?style=plastic"></a>
<a href="https://pypi.org/project/clueai/"><img alt="PyPI" src="https://img.shields.io/pypi/v/clueai?label=PyPI&logo=pypi&logoColor=white&style=flat-square"></a>
<a href="https://clueai.cn"><img src="https://www.modelfun.cn/assets/logo.57d43a51.png" width="30px"></a>
</p>

# Clueai Python SDK

This package provides functionality developed to simplify interfacing with the ClueAI API in Python 3.

## Installation

The package can be installed with `pip`:

```bash
pip install --upgrade clueai
```

Install from source:

```bash
python setup.py install
```
## Quick Start

To use this library, you must have an API key and specify it as a string when creating the `clueai.Client` object. API keys can be created through the [platform](https://www.clueai.cn/). This is a basic example of the creating the client and using the `generate` endpoint.


### Classify & Generate Tasks

<table>
<tr>
<td> classify 🔐 </td>
<td> generate 🔐⚡⚡ </td>
</tr>
<tr>
<td>

```python
import clueai
from clueai.classify import Example
# initialize the Clueai Client with an API Key
cl = clueai.Client('YOUR_API_KEY')
response = cl.classify(model_name='clueai',
  task_name='情感分析',
  inputs=["世界充满了欺骗", "世界和平"],
  examples=[Example("基本都是欺骗", "消极"),
   Example("基本都是惊喜", "积极")],
  labels = ["消极", "积极"])
  
print('prediction: {}'.format(
       response.classifications))
```
</td>
<td>

```python
import clueai

# initialize the Clueai Client with an API Key
cl = clueai.Client('YOUR_API_KEY')
prompt= '''
摘要：
本文总结了十个可穿戴产品的设计原则，而这些原则，同样也是笔者认为是这个行业最吸引人的地方：1.为人们解决重复性问题；2.从人开始，而不是从机器开始；3.要引起注意，但不要刻意；4.提升用户能力，而不是取代人
答案：
'''
# generate a prediction for a prompt 
prediction = cl.generate(
            model_name='clueai',
            prompt=prompt)
            
# print the predicted text          
print('prediction: {}'.format(prediction.generations[0].text))
```
</td>
</tr>
</table>


## Models
When you call Clueai's APIs we decide on a good default model for your use-case behind the scenes. The default model is great to get you started, but in production environments we recommend that you specify the model size yourself via the `model_name` parameter.

## Responses
All of the endpoint functions will return a Clueai object corresponding to the endpoint (e.g. for generation, it would be `Generation`). The responses can be found as instance variables of the object (e.g. generation would be `Generation.text`). Printing the Clueai response object itself will display an organized view of the instance variables.

ClueAI is backed by [Clue AI](https://clueai.cn) and [licensed](./LICENSE).