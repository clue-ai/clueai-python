
<p align="center">
<br>
<br>
<br>
<a href="https://qclue.cn"><img src="https://www.modelfun.cn/assets/logo.57d43a51.png" alt="CLUEAI logo: The data structure for unstructured data" width="200px"></>
<br>
<br>
<br>
<b>使NLP成为每个开发者的工具</b>
</p>


<p align=center>
<a href=""> <img src="https://img.shields.io/badge/language-python3.6+-brightgreen.svg?style=plastic"></a>
<a href="https://pypi.org/project/clueai/"><img alt="PyPI" src="https://img.shields.io/pypi/v/clueai?label=PyPI&logo=pypi&logoColor=white&style=flat-square"></a>
<a href="https://colab.research.google.com/drive/1H5J03ek3kpKschQ32mhX-y0JyRo1mIXN#scrollTo=zMSp1naSL8X9"> <img src="https://colab.research.google.com/assets/colab-badge.svg"></a>
<a href="https://qclue.cn"><img src="https://www.modelfun.cn/assets/logo.57d43a51.png" width="30px"></a>

</p>

*Read this in other languages: [English](docs/README_en.md)

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

* 使用colab一键运行使用
  
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1H5J03ek3kpKschQ32mhX-y0JyRo1mIXN#scrollTo=zMSp1naSL8X9)

### 文本生成图像
<table>
<tr>
<td> python 🔐 </td>
</tr>

<tr>
<td>

```python
import clueai
from PIL import Image
cl = clueai.Client("", check_api_key=False)
response = cl.text2image(
      model_name='clueai-base',
      prompt="秋日的晚霞",
      style="毕加索",
      out_file_path="test.png") 

im = Image.open('test.png')
im.show()
```
</td>

</tr>
</table>

### 文本分类
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
response = cl.classify(
      model_name='clueai-base',
      task_name='产品分类',
      inputs=["强大图片处理器，展现自然美丽的你,,修复部分小错误，提升整体稳定性。", "求闲置买卖，精品购物，上畅易无忧闲置商城，安全可信，优质商品有保障"],
      labels = ["美颜", "二手", "外卖", "办公", "求职"])
print('prediction: {}'.format(response.classifications))
```
</td>
<td>

```python
curl --location --request POST 'https://www.modelfun.cn/modelfun/api/serving_api' \
    --header 'Content-Type: application/json' \
    --header 'Model-name: clueai-base' \
    --data '{
       "task_type": "classify",
       "task_name": "产品分类",
       "input_data": ["强大图片处理器，展现自然美丽的你,,修复部分小错误，提升整体稳定性。", "求闲置买卖，精品购物，上畅易无忧闲置商城，安全可信，优质商品有保障"],
       "labels": ["美颜", "二手", "外卖", "办公", "求职"]
       }'

```
</td>

</tr>
</table>

### 文本生成
<table>
<tr>
<td> python 🔐 </td>
<td> curl 🔐⚡⚡ </td>
</tr>

<tr>
<td>

```python
import clueai

# initialize the Clueai Client with an API Key
cl = clueai.Client("", check_api_key=False)
prompt= '''
摘要：
本文总结了十个可穿戴产品的设计原则，而这些原则，同样也是笔者认为是这个行业最吸引人的地方：1.为人们解决重复性问题；2.从人开始，而不是从机器开始；3.要引起注意，但不要刻意；4.提升用户能力，而不是取代人
答案：
'''
# generate a prediction for a prompt 
prediction = cl.generate(
            model_name='clueai-base',
            prompt=prompt)
            
# print the predicted text          
print('prediction: {}'.format(prediction.generations[0].text))
```
</td>
<td>

```python
curl --location --request POST 'https://www.modelfun.cn/modelfun/api/serving_api' \
    --header 'Content-Type: application/json' \
    --header 'Model-name: clueai-base' \
    --data '{
       "task_type": "generate",
       "task_name": "摘要",
       "input_data": ["摘要：\n本文总结了十个可穿戴产品的设计原则，而这些原则，同样也是笔者认为是这个行业最吸引人的地方：1.为人们解决重复性问题；2.从人开始，而不是从机器开始；3.要引起注意，但不要刻意；4.提升用户能力，而不是取代人\n答案："]
       }'

```
</td>

</tr>
</table>

### 示例输入
#### 新闻分类(classify)
```bash
Input:
新闻分类：
今天（3日）稍早，中时新闻网、联合新闻网等台媒消息称，佩洛西3日上午抵台“立法院”，台湾新党一早8时就到台“立法院”外抗议，高喊：“佩洛西，滚蛋！”台媒报道称，新党主席吴成典表示，佩洛西来台一点道理都没有，“平常都说来者是客，但这次来的是祸！是来祸害台湾的。”他说，佩洛西给台湾带来祸害，“到底还要欢迎什么”。
选项：财经，法律，国际，军事
答案：

Model output::
国际
```

#### 意图分类(classify)
```bash
Input:
意图分类：
帮我定一个周日上海浦东的房间
选项：闹钟，文学，酒店，艺术，体育，健康，天气，其他
答案：

Model output::
酒店
```

#### 情感分析(classify)
```bash
Input:
情感分析：
这个看上去还可以，但其实我不喜欢
选项：积极，消极
答案：

Model output::
消极
```

#### 推理(generate)
```bash
Input:
推理关系判断：
前提：小明今天在北京
假设：小明在深圳旅游
选项：矛盾，蕴含，中立
答案：

Model output::
矛盾
```

#### 阅读理解(generate)
```bash
Input:
阅读理解：
段落：海外网8月2日电据美国《国会山报》8月1日报道，三名美国众议院议员日前致信美国政府问责局（GAO），要求审查联邦政府应对猴痘疫情的措施是否充分。
在信中，三名众议员称美国的公共卫生系统“严重受损”，联邦政府应对猴痘疫情行动迟缓，分发试剂和疫苗的工作出现延误，影响了遏制疫情传播的能力，而数百万剂的猴痘疫苗历经数月才获得批准，从一家丹麦工厂发往美国。
议员们还要求美国政府问责局审查美疾病控制和预防中心、食品和药物管理局、国土安全部，查明这些联邦机构是否为应对猴痘疫情做出了充分准备，是否借鉴了应对新冠疫情的经验教训。
美媒称，几个星期以来，美国国会议员频频就猴痘疫情应对措施向联邦政府施压，呼吁政府宣布进入公共卫生紧急状态。截至目前，美国疾病控制与预防中心已经确认了5000多例猴痘病例。考虑到仍有许多民众无法进行猴痘病毒检测，当前的病例数可能被低估。
问题：联邦政府应对疫情有什么问题？
答案：

Model output::
联邦政府应对猴痘疫情行动迟缓,分发试剂和疫苗的工作出现延误,影响了遏制疫情传播的能力
```
#### 阅读理解-自由式(generate)
```bash
Input:
阅读以下对话并回答问题。
男：今天怎么这么晚才来上班啊？女：昨天工作到很晚，而且我还感冒了。男：那你回去休息吧，我帮你请假。女：谢谢你。
问题：女的怎么样？
选项：正在工作，感冒了，在打电话，要出差。
答案：

Model output::
感冒了
```

#### 摘要(generate)
```bash
Input:
为下面的文章生成摘要：
北京时间9月5日12时52分，四川甘孜藏族自治州泸定县发生6.8级地震。地震发生后，领导高度重视并作出重要指示，要求把抢救生命作为首要任务，全力救援受灾群众，最大限度减少人员伤亡
答案：

Model output::
四川甘孜州泸定县发生6.8级地震
```

#### 翻译-中英(generate)
```bash
Input:
翻译成英文：
议长去了台湾，中国人民很愤怒。
答案：

Model output::
The Speaker went to Taiwan, and the Chinese people were angry.
```

#### 翻译-英中(generate)
```bash
Input:
翻译成中文：
This is a dialogue robot that can talk to people.
答案：

Model output::
这是一个能与人对话的机器人。
```
#### 信息抽取(generate)
```bash
Input:
信息抽取：
据新华社电广东省清远市清城区政府昨日对外发布信息称,日前被实名举报涉嫌勒索企业、说“分分钟可以搞垮一间厂”的清城区环保局局长陈柏,已被免去清城区区委委员
问题：机构名，人名，职位
答案：

Model output::
人名:陈柏 机构名:新华社,广东省清远市清城区政府,清城区环保局,清城区区委 职位:局长
```
### 更大模型更好效果

在用更大模型之前，你需要有个API key， 并且在创建`clueai.Client`对象时需要指定这个API key. API key 可以通过这个[平台](https://www.qclue.cn/)获得，下面是有关分类和生成任务的一个基本的示例

### 文本分类
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
response = cl.classify(
  model_name='clueai-large',
  task_name='情感分析',
  task_name='产品分类',
  inputs=["强大图片处理器，展现自然美丽的你,,修复部分小错误，提升整体稳定性。", "求闲置买卖，精品购物，上畅易无忧闲置商城，安全可信，优质商品有保障"],
  labels = ["美颜", "二手", "外卖", "办公", "求职"])
  
print('prediction: {}'.format(response.classifications))
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
       "task_name": "产品分类",
       "input_data": ["强大图片处理器，展现自然美丽的你,,修复部分小错误，提升整体稳定性。", "求闲置买卖，精品购物，上畅易无忧闲置商城，安全可信，优质商品有保障"],
       "labels": ["美颜", "二手", "外卖", "办公", "求职"]
       }'
```
</td>

</tr>
</table>

### 文本生成
<table>
<tr>
<td> python 🔐 </td>
<td> curl 🔐⚡⚡ </td>
</tr>

<tr>
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
            model_name='clueai-large',
            prompt=prompt)
            
# print the predicted text          
print('prediction: {}'.format(prediction.generations[0].text))
```
</td>
<td>

```python
curl --location --request POST 'https://www.modelfun.cn/modelfun/api/serving_api' \
    --header 'Content-Type: application/json' \
   --header 'Model-name: clueai-large' \
  --header 'Api-Key: BEARER {api_key}' \
    --data '{
       "task_type": "generate",
       "task_name": "摘要",
       "input_data": ["摘要：\n本文总结了十个可穿戴产品的设计原则，而这些原则，同样也是笔者认为是这个行业最吸引人的地方：1.为人们解决重复性问题；2.从人开始，而不是从机器开始；3.要引起注意，但不要刻意；4.提升用户能力，而不是取代人\n答案："]
       }'

```
</td>

</tr>
</table>

## 模型介绍

当您调用clueai的API时，我们为您的用例指定默认模型。 默认模型非常适合您开始使用，但是在生产环境中，我们建议您通过`model_name`参数自己指定特定模型。

## 返回结果

对于不同的任务返回相对应的clueai对象（例如，对于分类，将是“Classification”）。 

ClueAI 被[ClueAI](https://qclue.cn) 支持，并且相关协议可以查看[licensed](./LICENSE).
