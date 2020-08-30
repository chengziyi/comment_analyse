##根据模板自动生成html文件用于前端展示
##输入：str组成的list
##输出：包含要展示内容的html文件
start="""
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="Mark Otto, Jacob Thornton, and Bootstrap contributors">
    <meta name="generator" content="Jekyll v4.1.1">
    <title>Sentiment Analyse</title>

    <!-- Bootstrap core CSS -->
    <link rel='stylesheet' id='style-css' href="{{ url_for('static',filename='css/bootstrap.min.css') }}"  type='text/css' media='all'>

    <style>
      .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
      }

      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
        }
      }
    </style>
    <!-- Custom styles for this template -->
    <link href="{{ url_for('static',filename='css/dashboard.css') }}" rel="stylesheet">

	<!-- show pie -->
	<script src="http://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>
	<script src="http://code.highcharts.com/highcharts.js"></script>
	<!-- show radar -->
	<script src="/static/js/Chart.js"></script>

  </head>
<body>
	<nav class="navbar navbar-dark sticky-top bg-dark flex-md-nowrap p-0 shadow">
		<a class="navbar-brand col-md-3 col-lg-2 mr-0 px-3">Sentiment Analyse</a>

		<ul class="navbar-nav px-3">

		</ul>
	</nav>

<div class="container-fluid">
  <div class="row">
    <nav id="sidebarMenu" class="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse">
      <div class="sidebar-sticky pt-3">
        <ul class="nav flex-column">
          <li class="nav-item">
            <a class="nav-link" href="/">
              <span data-feather="home"></span>
              Dashboard
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" href="/get_comments">
              <span data-feather="file"></span>
              View comments <span class="sr-only">(current)</span>
            </a>
          </li>
        </ul>
      </div>
    </nav>

<!-- show comments -->
	<main role="main" class="col-md-9 ml-sm-auto col-lg-10 px-md-4">
		<div class="htmleaf-content">
"""

end="""
		</div>
    </main>
  </div>
</div>
</body>
</html>
"""

def empty_html():
  with open("./templates/comments.html",'w',encoding='utf-8') as f:
    message=start+end
    f.write(message)

def generate_html(content_list):
	content_tuple=tuple(content_list)
	mid=''
	for i in range(len(content_list)):
		mid+="""
			<div class="card bg-light text-dark">
				<div class="card-body">%s</div>
			</div>
		"""
	#打开文件，准备写入
	with open("./templates/comments.html",'w',encoding='utf-8') as f:
		message=start+mid+end
		# print(message%content_tuple)
		#写入文件
		f.write(message%content_tuple)

if __name__=='__main__':
  #示例
  str1 = 'my name is :'
  str2 = '--MichaelAn--'
  str3='t1'
  str4='t2'
  contents=[str1,str2,str3,str4]

  generate_html(contents)


