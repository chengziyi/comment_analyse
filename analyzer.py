import pandas as pd
import pymongo
import time
# import fasttext
import re
import jieba
import jieba.posseg as pseg
import gensim
from collections import Counter

# 加载停用词
print('loading stop_words...')
stop_words = []
with open(r'./train_model/stopwords.txt', 'r', encoding='utf-8') as f:
	stop_words=f.readlines()
stop_words=list(map(lambda x:x.replace('\n',''),stop_words))

##根据name查找数据库
def get_comments(name):
	comments=[]
	time=[]
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient["comment_db"]
	mycol = mydb["shop_comments"]
	myquery = { "name": name }
	
	mydoc = mycol.find(myquery)
	##此处速度较慢
	for x in mydoc:
		comments.append(x['comment'])
		time.append(x['timestamp'])
	return comments,time

##fasttext分类
def token(string):
    return "".join(re.findall(r'[\u4e00-\u9fa5]+', string))
def cut(string):
	return ' '.join(jieba.lcut(string))
##方法自己加载模型
def fasttext_classifier(comments):
	sentences=list(map(lambda x:cut(token(x)),comments))
	print('loading model...')
	model_path='./train_model/fasttext_ftz_model.ftz'
	model=fasttext.load_model(model_path)
	label,p=model.predict(sentences)
	# print(sentences)
	labels=list(map(lambda x:x[0].replace('__label__',''),label))
	# print(labels)
	# print(labels.count('1'))
	return labels
##调用方法时将模型作为参数传入
def fasttext_classifier_with_model(comments,model):
	sentences=list(map(lambda x:cut(token(x)),comments))
	label,p=model.predict(sentences)
	# print(sentences)
	labels=list(map(lambda x:x[0].replace('__label__',''),label))
	# print(labels)
	# print(labels.count('1'))
	return labels

'''
折线图显示评论数量随时间的变化
取出的每条评论都有对应的timestamp
把timestamp按固定间隔分成时间段
如：delta=(max_time-min_time)/11
时间和评论是对应的，所以统计每个时间段的timestamp数量就是评论数量

input:从mongodb中取出的一组timestamp字符串
return:折线图的x轴,y轴
'''
def time_process(timestamps):
	timestamps=list(map(lambda x:int(x[:-3]),timestamps))

	min_time=min(timestamps)
	max_time=max(timestamps)

	time_x=[]
	times=[]
	#分11个时间段并转化成'年/月'的形式
	delta=int((max_time-min_time)/11)
	for i in range(11):
		item=max_time-i*delta
		times.append(item)
		time_array=time.localtime(item)
		strtime=str(time_array.tm_year)+'/'+str(time_array.tm_mon)
		time_x.append(strtime)
	time_x=time_x[::-1]
	times=times[::-1]
	##计算每个时间段的timestamp数量
	timestamps.sort()

	time_y=[]
	for t in times:
		timestamps_copy=timestamps.copy()
		pre=len(timestamps)
		for i in timestamps_copy:
			if i<=t:timestamps.remove(i)
			else:break
		after=len(timestamps)
		time_y.append(pre-after)

	# time_y[-1]+=after

	line_x=['<'+time_x[0]]
	for i in range(len(time_x)-1):
		line_x.append(time_x[i]+'-'+time_x[i+1])
	# print(line_x)
	# print(time_y)
	return line_x,time_y

##LDA主题分析
def split_text(text):
    return ' '.join(jieba.lcut(token(text)))
##分词去停用词
def get_seg_content(text):
	line=split_text(text)
	words=line.split()
	return [ w for w in words if w not in stop_words ]
# lda_model 为已经训练好的LDA模型
# content 为一条文本内容
def get_topic(lda_model,content,dictionary):
	corpus = dictionary.doc2bow(content)  # 文档转换成bow
	topics = lda_model.get_document_topics(corpus)  # 得到新文档的主题分布
	##取出的主题按相关性高到低排序
	topics=sorted(topics,key=lambda x:x[1],reverse=True)

	##用jieba.pseg取出相关性最高的形容词作为该评论的主题
	# topic=topic[-1][0]
	topic=[dictionary[i] for i,_ in topics]
	topic=' '.join(topic)

	# print(topic)
	words = pseg.cut(topic)
	for word, flag in words:
		if flag=='a':
			return word
	return dictionary[topics[0][0]]

##将评论按主题分成6类，第六类为其它
##input:一组评论
##output:主题及数量，用于显示雷达图
def lda_get_topic(lda_model,comments):
	##use lda to get topics
	comments_cut = [get_seg_content(i) for i in comments]
	id2word = gensim.corpora.Dictionary(comments_cut)
	topics=[]
	for i in range(len(comments_cut)):
		topic=get_topic(lda_model,comments_cut[i],id2word)
		# topics+=topic
		topics.append(topic)
	# print(len(topics))
	# print(topics)
	##统计主题及数量，用于显示雷达图
	word_count=dict(Counter(topics))
	word_count=sorted(word_count.items(),key=lambda x:x[1],reverse=True)
	# print(word_count)
	radar_x=[]
	radar_y=[]
	for k,v in word_count:
		radar_x.append(k)
		radar_y.append(v)
		if len(radar_x)==5:
			break
	radar_x.append('其它')
	radar_y.append(len(topics)-sum(radar_y))
	# print(radar_x)
	# print(radar_y)
	return radar_x,radar_y

##pos_num,neg_num,total_num,各时间段的comment数量
if __name__=='__main__':
	##get comments
	comments,timestamps=get_comments('KFC')
	print(len(comments))

	##LDA主题分析，雷达图
	print('loading lda model...')
	model_path='./train_model/lda_model/LDA_model'
	lda_model = gensim.models.ldamodel.LdaModel.load(model_path)
	x,y=lda_get_topic(lda_model,comments)
	print(x,y)

	##分类并统计
	## classify by fasttext
	labels=fasttext_classifier(comments)
	# print(labels)
	##饼图
	pos_num=labels.count('1')
	neg_num=labels.count('0')
	total=pos_num+neg_num
	pos_per=float('{:.3f}'.format(pos_num/total))
	# neg_per=neg_num/total
	print('pos_per:',pos_per)
	print('neg_per:',1-pos_per)
	##条形图
	print('pos_num:',pos_num)
	print('neg_num:',neg_num)
	##折线图
	line_x,line_y=time_process(timestamps)
	print(line_x)
	print(line_y)








