本项目是一个舆情分析项目，通过分析评论的数量变化和隐含情感等信息发掘其商业价值

using data to solve problems	--cy

因爬虫容易被反，所以使用大众点评06年-12年的历史数据作为本项目的数据来源:

https://github.com/SophonPlus/ChineseNlpCorpus/blob/master/datasets/yf_dianping/intro.ipynb

本项目使用fasttext作为文本分类模型，将用户评论分为好评和差评两类

使用LDA模型提取评论的主题分布

fasttext:https://github.com/facebookresearch/fastText

我收集的情感分类训练数据集: https://pan.baidu.com/s/1Hql-zi6LDcUgorOS6J3o3w  提取码：ip1g

我用数据集训练好的fasttext模型: https://pan.baidu.com/s/1Gr7XknPkzpNEdej6wuRDZg  提取码：yjdu

bootstrap前端模板:https://getbootstrap.com/docs/4.5/examples/dashboard/

目录结构: 

static: 前端的静态文件

templates: flask返回的网页

train_model: 用于分析数据的模型(fasttext, LDA)和停用词

server.py: flask程序

analyzer.py: 封装的API调用模型分析数据并返回用于绘制各种图表的结果

html_generator.py: 根据需要的样式自动生成html文件

配置&运行: 

1.安装并启动mongodb数据库 参考:https://www.cnblogs.com/xiaowenwen/p/11876146.html

2.将数据写入mongodb数据库，每一条数据的字段为(name,comment,timestamp)

3.安装requirements.txt里的包

效果: 