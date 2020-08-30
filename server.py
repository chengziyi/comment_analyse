from flask import Flask, request, render_template
import json
import time
import _thread

import fasttext
import jieba
import gensim

import analyzer
import html_generator

app=Flask(__name__)
app.jinja_env.auto_reload=True
app.config['TEMPLATES_AUTO_RELOAD']=True

fasttext_model_path='./train_model/fasttext_ftz_model.ftz'

# 跨域支持
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
app.after_request(after_request)

##start thread for lda analyse
def subthread_lda_analyse(thread_name,comments):
	# print(thread_name)
	##lda get topics
	global lda_model
	global radar_x
	global radar_y
	radar_x,radar_y=analyzer.lda_get_topic(lda_model,comments)
	# print(radar_x,radar_y)
	html_generator.generate_html(comments)

@app.route('/',methods=['GET','POST'])
def test_search():
	pie={'pos':0.000,'neg':0.000}
	bar={'pos':0,'neg':0}

	line_x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov']
	line_y=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	line_name='shop_name'
	line={'x':line_x,'y':line_y,'name':line_name}
	global result
	result={'pie':pie,'bar':bar,'line':line}

	html_generator.empty_html()

	return render_template('dashboard.html', data=json.dumps(result))

@app.route('/get_topic',methods=['GET','POST'])
def get_topic():
	if request.method == 'GET':
		global radar_x
		global radar_y
		radar={'x':radar_x,'y':radar_y}
		return radar

##返回根据评论内容自动生成的网页
@app.route('/get_comments',methods=['GET','POST'])
def get_comments():
	return render_template('comments.html')

##前端ajax请求
@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
	print(request.method)
	global result
	if request.method == 'GET':
		return result

	if request.method == 'POST':
		name = request.form['search_name']
		print(name)
		##根据名字获取数据，分类，统计结果，查询数据库较慢
		comments,timestamps=analyzer.get_comments(name)
		if len(comments)==0:
			return 'no_result'
		##使用预先加载的模型分析数据统计结果
		global fasttext_model
		labels=analyzer.fasttext_classifier_with_model(comments,fasttext_model)
		pos_num=labels.count('1')
		neg_num=labels.count('0')
		total=pos_num+neg_num
		pos_per=float('{:.3f}'.format(pos_num/total))
		##饼图和条形图
		pie={'pos':pos_per,'neg':1-pos_per}
		bar={'pos':pos_num,'neg':neg_num}
		# print(pos_num,neg_num,pos_per)
		##折线图
		line_x,line_y=analyzer.time_process(timestamps)
		line_name=name
		line={'x':line_x,'y':line_y,'name':line_name}
		# print(line_x)
		# print(line_y)
		result={'pie':pie,'bar':bar,'line':line}

		##数据多了主题提取可能比较慢所以用子线程通过全局变量返回结果
		##start subthread for lda analyse
		try:
			_thread.start_new_thread( subthread_lda_analyse, ("Thread-lda", comments, ) )
		except:
			print ("Error: can not start thread")

		return 'result generate success'
	return 'flask not get name'

if __name__=='__main__':
	print('jieba initializing...')
	jieba.initialize()
	print('loading fasttext model...')
	fasttext_model=fasttext.load_model(fasttext_model_path)

	print('loading lda model...')
	model_path='./train_model/lda_model/LDA_model'
	lda_model = gensim.models.ldamodel.LdaModel.load(model_path)
	radar_x=[]
	radar_y=[]

	result={}
	app.run("0.0.0.0",threaded=True)
