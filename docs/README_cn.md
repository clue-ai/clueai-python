
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

在用这个库之前，你需要有个API key， 并且在创建`clueai.Client`对象时需要指定这个API key. API key 可以通过这个[平台](https://www.clueai.cn/)获得，下面是有关分类和生成任务的一个基本的示例



### 分类和生成任务

<table>
<tr>
<td> 分类任务 🔐 </td>
<td> 生成任务 🔐⚡⚡ </td>
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


## 模型介绍

当您调用clueai的API时，我们为您的用例指定默认模型。 默认模型非常适合您开始使用，但是在生产环境中，我们建议您通过`model_name`参数自己指定特定模型。

## 返回结果

对于不同的任务返回相对应的clueai对象（例如，对于生成，将是“Generation”）。 


