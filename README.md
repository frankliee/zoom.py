# <center> Zoom 用户指南 </center>
欢迎阅读Zoom的文档，通过zoom快速，敏捷地实现web需求

## 前言
在使用 Zoom 前请阅读本文。希望本文可以回答您有关 zoom 的用途和目的，以及是 否应当使用 zoom 等问题。

### Zoom有什么用途？
Zoom是一款轻量级的Web开发框架，支持静态网页，动态网页，个人博客，webservice等不同的web服务类型。

### 轻量级是什么意思？

轻量级并不代表整个应用只能塞在一个 Python 文件内，当然塞在单一文件内也是可以的。 轻量级也不代表 Zoom 功能不强。轻量级表示 Zoom 的目标是保持核心既简 单而又可扩展。Zoom 不会替你做出许多决定，比如选用何种数据库。类似的决定，如使用何种模板引擎，是非常容易改变的。 Zoom 可以变成你任何想要的东西，一切恰到 好处，由你做主。

缺省情况下， Zoom 不包含数据库抽象层，模板或者其他已有的库可以处理的东西。 然而， Zoom 通过扩展为你的应用添加这些功能，就如同这些功能是Zoom 原生的一样。 大量的扩展用以支持数据库整合、模板渲染等等。Zoom 可能是 “微小”的，但它已经为满足您的各种生产需要做出了充足的准备。

### 配置和惯例
zoom基于Python开发，并且支持跨平台（Windows/Linux/Mac os X）。
所需的Python版本需为2.7，不支持3.3以上版本。

## 安装
### 免安装方法
zoom 可以支持免安装，将zoom.py文件放入项目所在目录下即可。

### 安装方法

#### python环境配置
请首先确认已经安装python2.7运行环境。推荐安装某种python科学计算发行版，例如Anaconda，
因为这些发行版中包含了大量可用的库，并且会自动配置和Python相关的环境变量。

安装完成之后打开终端或者cmd检查安装是否成功，输入以下命令。

	python -version
	
如果安装正确显示如下：

	Python 2.7.8
	
####安装zoom
 
打开终端或者cmd，移动到安装包所在路径，运行如下命令。

	python setup.py install
		
成功运行之后，所需的zoom.py文件即被复制到Python的系统搜索路径下。
 
## 快速上手

### 创建工程

####手动搭建项目
按照如下所示的工程结果，搭建项目
	
	-zoom.py ---- web框架文件
	-app.py  ---- 工程的主要文件（可以由多个文件组成）
	-template --- 模板文件夹，即所用的html文件
	-static   --- 静态资源文件夹
		-css   --- css文件夹
		-js    --- javasrcipt文件夹
		-pic   --- 图片文件夹
		-fonts --- 字体文件夹
		-file  --- 下载文件的文件夹
		
#### 使用zoom命令创建

使用zoom自带的命令创建工程

	python zoom.py -new app_name

该命令会在当期目录下创建以app_name为名的工程文件夹

### 一个最小的hello world程序
一个最小的zoom 应用如下所示

~~~python
from zoom import *
app=App('my app')
@app.url('/')
def index(request):
	return 'hello world'
	
if __name__=='__main__':
	app.run()
~~~
保存为app.py,之后启动服务器

	python app.py
	
打开浏览器输入
	
	http://localhost:8000

可以观察到结果
	
### URL绑定
现代 web 应用都使用漂亮的 URL ，有助于人们记忆，对于使用网速较慢的移动设备尤其有利。如果用户可以不通过点击首页而直达所需要的页面，那么这个网页会更得到用户的青睐，提高回头率。

zoom支持将特定的函数绑定到对应的URL上，下面的是一些基本例子：

~~~python


#单个URL绑定到一个函数上
@app.url('/'):
def index(request):
	return 'this is index url'
	
#多个URL绑定到同一函数上
@app.url('/'):
@app.url('/index'):
def home(request):
	return 'this is index'
	
~~~

### 模板

在 Python 内部生成 HTML 不好玩，且相当笨拙。因为你必须自己负责 HTML 转义，以确保应用的安全。因此， zoom 提供插件 zoomTemplate 自动为你配置第三方的 Jinja2 模板引擎。
使用该功能需要预装有Jinja2模块，可以使用pip进行模块安装

	pip install Jinja2

模板即包含Jinja2规定的标记的html文件。模板的存放路径为 ./template。模板的默认路径为

	./template

可以通过如下方法进行添加

~~~python
app.append(
	{'path':'your new path'}
	)
~~~

使用 render 方法可以渲染模板，你只要提供模板内容和需要作为参数传递给模板的变量就行了。下面是一个简单的模板渲染例子:

~~~python
@app.url('/')
def index(request):
	return render('Hello {{ name }}!',name="John")
~~~

也可以使用 template_render 方法进行渲染，提供的参数为模板名称，需要作为参数传递给模板的变量。

~~~python
@app.url('/')
def index(request):
	return template_render('index.html',name="John")
~~~

### 静态资源

静态资源包括css脚本，js脚本，图片，字体，普通文件等。
默认的路径(以linux为例)如下所示,并且对应与如下URL

	./static/css  => /static/css/x.css
	./static/fs   => /static/js/x.js
	./static/pic  => /static/pic/(x.png|x.jpg|....)
	./static/fonts=> /static//x.font
	./static/file => /static/css/x

静态资源的路径允许被修改，方法为修改app中的static_path属性

~~~python
	static_path=[
		{'path':os.path.join('.','static','css'),'url':'/static/css/.+'},
		{'path':os.path.join('.','static','js'),'url':'/static/js/.+'},
		{'path':os.path.join('.','static','pic'),'url':'/static/pic/.+'},
		{'path':os.path.join('.','static','file'),'url':'/static/file/.+'},
		{'path':os.path.join('.','static','fonts'),'url':'/static/fonts/.+'}
	]
~~~
	
### URL传参

URL不仅可以用来表达所在用户请求的资源的路径，而且可以用来传达参数。
参数的表示遵守Python的正则表达式规则，并且参数的值保存在request对象中，使用[]操作符访问。
下面是一个用来说明的简单的例子。

~~~python
@app.url('^/home/?P<UID>.+/?P<Name>.+/?P<Time>.+$')
def home(request):
	print "UID = "+request['UID']
	print "Name = "+request['Name']
	print "Time = "+request['Time']
	return 'look at console...'
~~~

如果在浏览器中输入

	http://localhost:8000/home/123456/John/2015-5-20
	
可以在终端中观察到

	UID = 123456
	Name = John
	Time = 2015-5-20

### 表单响应

通常在web开发中常常用到提交表单的功能，例如一个简单的登录框的提交并验证。
通过request中的method参数，我们可以获取某次http请求的是否是post类型，或者是get类型。
如果是post类型，则可以使用[]操作符从request中获取表单的参数。
下面以一个简单的登录功能作为示例

~~~html
前端代码
<html>
<head>
    <title>登录</title>
</head>
<body>
   <form action="/login" method="post">
   		 <input type="text" name="UserName">
        <input type="password" name="Password">
        <input type="submit">
    </form>
</body>
</html>
~~~
~~~python
#后台代码
@app.url('^/login$')
def search(request):
	if request.method=='post':
		print request['UserName']
		print request['Password']
		return "ok"
	else:
		return "error"
~~~
### 上传文件

上传文件类似与表单提交，同样采用post方法，不过需要上传文件的内容需要从request的
*file_name*中获取文件名，从*file_data*中获取文件数据，从*file_len*中获取文件长度。

~~~html
前端代码
<html>
<head>
    <title>文件上传</title>
</head>
<body>
   <form action="/upload" method="post">
   		 <input type="file" name="UploadFile">
       <input type="submit">
    </form>
</body>
</html>
~~~
~~~python
#后台代码
@app.url('^/upload$')
def search(request):
	if request.method=="post":
		try:
			f=open(request.file_name,'w')
			f.write(request.file_data')
			f.close()
		except:
			return 'fail'
		return 'ok'
	else:
		return 'fail'
~~~

### 数据库模式
在当代 Web 应用中，主观逻辑经常牵涉到与数据库的交互。 数据库驱动网站 在后台连接数据库服务器，从中取出一些数据，然后在 Web 页面用漂亮的格式展示这些数据。 这个网站也可能会向访问者提供修改数据库数据的方法。

许多复杂的网站都提供了以上两个功能的某种结合。 例如 Amazon.com 就是一个数据库驱动站点的良好范例。 本质上，每个产品页面都是数据库中数据以 HTML格式进行的展现，而当你发表客户评论时，该评论被插入评论数据库中。

以java语言为例，在传统的的数据库使用方法中，用现有的任何类库执行一条 SQL 查询并对结果进行一些处理。

~~~java
//1.注册驱动  
  try {  
   Class.forName("com.mysql.jdbc.Driver");  
  } catch (ClassNotFoundException e) {  
   e.printStackTrace();  
  }
//2.创建数据库的连接  
java.sql.Connection conn = java.sql.DriverManager.getConnection(  
            "jdbc:mysql://localhost/test?useUnicode=true&characterEncoding=GBK","root", "wxweven4814");</span>  
//3.获取表达式
java.sql.Statement stmt = conn.createStatement();</span>  
//4.执行SQL  
String sql = "select * from test";  
java.sql.ResultSet res = stmt.executeQuery(sql);</span>  
//5.打印结果集里的数据  
while(res.next()) {  
    System.out.print("the id: ");  
    System.out.println(res.getInt(1));  
    System.out.print("the user: ");  
    System.out.println(res.getString("user"));  
    System.out.print("the address: ");  
    System.out.println(res.getString("addr"));  
    System.out.println();  
} 
//6.释放资源，关闭连接（这是一个良好的习惯）  
res.close();  
stmt.close();  
conn.close();
~~~

使用这种方法，往往即使一个简单的操作也需要使用大量的代码，而且在java中编码sql语句是一件非常痛苦的事情。所以通常借助数据库的抽象层ORM间接对数据库进行访问。

zoom中以插件 zoomDB.py 的方式提供数据库抽象层的能力，下面以一个简单的例子简要介绍其用法。

~~~python
from zoomDB import *

@app.plugin()	
@field('id','int','primary key')
@field('user','varchar(50)')
@filed('addr','varchar(50)')
class User(Model): pass
	
for user in app.User.select():
	print user[0],user[1],user[2]
		
~~~
其中 @app.plugin() 是一种修饰器，可以用来将插件User安装到app中，
@field 是zoomDB提供的修饰器，用来声明一个数据库中的列。


### 数据库操作

除了数据模式的基本定义外，zoomDB还提供了一组数据库相关的基本操作，如下所示。

~~~python
# 查询
app.User.select('user like %%zoom%%')

# 过滤列
app.User.select('user like %%zoom%%').filter('user','addr')

#获取单个值（查询结果必须仅有一项，否则抛出异常）
app.User.get('id=1')

#删除元组
app.User.delete('id=1')

#执行sql语句
app.User.execute(sql_str)

#清除数据
app.User.clear()

#更新数据
app.User.update("id=2","user='zoom' ")

~~~

### 异步任务
通常某些占用CPU的操作，需要作为非阻塞的异步任务，以降低用户延迟。
zoom通过插件zoomJob提供异步任务的功能，下面是一个简单的例子。

~~~python
from zoomJob import *
import time
@asy
def loop1():
	while True:
		time.sleep(1)
		print 'loop1'
def loop2():
	while  True:
		time.sleep(1)
		print 'loop2'
loop1()
loop2()
~~~
在控制台下观察到

	loop1
	loop2
	loop2
	lopp1
	......
被 @asy 修饰器修饰的函数，将作为一个线程执行。从终端的输出可以看出
loop1() 函数和 loop2() 函数交替执行，而不是 loop1() 函数阻塞了 loop2() 函数的执行。


### 定时任务
web开发中常常具有某些需要定期执行的函数，例如定期清除无效的图片，数据。
通过 zoom 插件 zoomJob中的定时器可以方便的完成这项需求。

~~~python
from zoom import *
from zoomJob import *
@timer(second=10)
def job():
	print "This is a job"
	job()
~~~

观察终端输出

	This is a job
	This is a job
	This is a job
	.............
每10秒钟输出一次 This is a job
	
### 使用markdown编写博客
Markdown 是一种用来写作的轻量级 **标记语言**，它用简洁的语法代替排版，而不像一般我们用的字处理软件 Word 或 Pages 有大量的排版、字体设置。它使我们专心于码字，用 **标记** 语法，来代替常见的排版格式。

以下面的例子为例，编写test.md，保存在temlpate文件夹下内容如下所示。

~~~markdown
#   标题一
##  标题二
### 标题三
图片![](img.png)
~~~

导入zoomMD插件，如下所示。

~~~python	
from zoom  import *
from zoomMD import *
app=App()
md=MD(app)
app.run()
~~~

zoomMD 会在 md 对象创建时自动将 template 路径下的 md 文件自动翻译，并保存成同名 html 文件。
服务器启动后，在浏览器中输入：

	http://localhost:8000/test.html

即可观察到显示的效果。

zoomMD 插件需要 markdown-python 模块的支持，使用如下 pip 命令安装该模块。

	pip install markdown
	
### 使用多线程模式

通常在web应用中，性能的瓶颈主要网络IO的限制造成，而并非是CPU的限制，
所以并发技术可以大大提高web应用的承载量。
zoom 提供了线程级的并发服务，默认模式下不开启多线程模式（会造成更多的内存消耗）。
下面是开启多线程模式的简单例子。

~~~python

from zoom import *
app=App(multiThread=True)
app.run()
~~~
zoom服务器对每个http请求，产生一个线程去完成响应。

### 缓存模式
为了提高请求访问的速度，zoom 采用了缓存技术，将最近访问的 html，css，js资源保存在内存中，无需二次读取内存，降低了请求响应延迟。缓存模式，默认已经开启，并且可以以显式的方法，开启或者关闭。

~~~python
from zoom import *

#缓存模式开启
app1=App(cache=True)

#缓存模式关闭
app2=App(cahe=False)
~~~


### 调试模式

开发中经常改动html文件和图片等静态资源，在缓存模式下，修改这些资源，无法在浏览器中预览到。
并且多线程模式也会给调试带来不便。zoom提供了调试模式（直接关闭这二种模式），默认情况下不开启调试模式。

~~~python
from zoom import *
app=App(debug=True)
~~~

## zoom拓展
zoom提供插件拓展能力，初试版本中即包含4个插件。

* zoomBD 提供数据库抽象层
* zoomMD 提供markdown博客支持
* zoomJob 提供异步，定时器等功能
* zoomTemplate 提供模板功能

用户可以自行根据需求开发插件

## zoom方案 

### 纯静态网页

### 动态网页

### 个人博客

### WebSerice




