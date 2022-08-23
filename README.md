
<p align="center">
<br>
<br>
<br>
<img src="https://www.modelfun.cn/assets/logo.57d43a51.png" alt="CLUEAI logo: The data structure for unstructured data" width="200px">
<br>
<br>
<br>
<b>使NLP成为每个开发者的工具</b>
</p>


<p align=center>
<a href=""> <img src="https://img.shields.io/badge/language-python3.6+-brightgreen.svg?style=plastic"></a>
<a href="https://pypi.org/project/clueai/"><img alt="PyPI" src="https://img.shields.io/pypi/v/clueai?label=PyPI&logo=pypi&logoColor=white&style=flat-square"></a>
<a href="https://clueai.cn"><img src="https://www.modelfun.cn/assets/logo.57d43a51.png" width="30px"></a>

</p>

*Read this in other languages: [English](README_en.md)

# Python 软件包

该软件包提供了开发的功能，以简化在python3中与clueai API的接口。

## 安装

可以使用 `pip`命令安装:

```bash
pip install --upgrade clueai
```

也可以通过源码:

```bash
python setup.py install
```
## 快速开始

### 免费试玩


<table>
<tr>
<td> python 🔐 </td>
<td> curl 🔐⚡⚡ </td>
</tr>

<tr>
<td>

```python
import clueai
from clueai.classify import Example
cl = clueai.Client("", check_api_key=False)
response = cl.classify(model_name='clueai-base',
  task_name='情感分析',
  inputs=["今天天气很好", "我不喜欢这个产品"],
  examples=[Example("基本都是欺骗", "消极"),
   Example("基本都是惊喜", "积极")],
  labels = ["消极", "积极"])
  
print('prediction: {}'.format(
       response.classifications))
```
</td>
<td>

```python
curl --location --request POST 'https://www.modelfun.cn/modelfun/api/serving_api' \
  --header 'Content-Type: application/json' \
  --header 'Model-name: clueai-base' \
  --data '{
    "task_type": "classify",
    "task_name": "情感分析",
    "input_data": ["今天天气很好", "我不喜欢这个产品"],
    "labels": ["消极", "积极"]
  }'
```
</td>

</tr>
</table>

### 更大模型更好效果

在用更大模型之前，你需要有个API key， 并且在创建`clueai.Client`对象时需要指定这个API key. API key 可以通过这个[平台](https://www.qclue.cn/)获得，下面是有关分类和生成任务的一个基本的示例


<table>
<tr>
<td> python 🔐 </td>
<td> curl 🔐⚡⚡ </td>
</tr>

<tr>
<td>

```python
import clueai
from clueai.classify import Example
# initialize the Clueai Client with an API Key
cl = clueai.Client('YOUR_API_KEY')
response = cl.classify(model_name='clueai-large',
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
curl --location --request POST 'https://www.modelfun.cn/modelfun/api/serving_api' \
  --header 'Content-Type: application/json' \
  --header 'Model-name: clueai-large' \
  --header 'Api-Key: BEARER {api_key}' \
  --data '{
    "task_type": "classify",
    "task_name": "情感分析",
    "input_data": ["今天天气很好", "我不喜欢这个产品"],
    "labels": ["消极", "积极"]
  }'
```
</td>

</tr>
</table>


## 模型介绍

当您调用clueai的API时，我们为您的用例指定默认模型。 默认模型非常适合您开始使用，但是在生产环境中，我们建议您通过`model_name`参数自己指定特定模型。

## 返回结果

对于不同的任务返回相对应的clueai对象（例如，对于分类，将是“Classification”）。 

ClueAI 被[Clue AI](https://qclue.cn) 支持，并且相关协议可以查看[licensed](./LICENSE).
