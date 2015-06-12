#_*_ coding: utf8 _*_ 
import os,sys,time
import functools
import re
import web
__doc__=u'''
zoom.py 模块中包含 zoom框架中基本功能

python版本要求 2.7以上，不支持3.3

无需第三方模块支持
'''
class FileNotExsit(Exception):
	u'''
	文件不存在,系统抛出的异常
	'''
	pass
class OptionNotExsit(Exception):
	u'''
	选项不存在所抛出的异常，
	通常是使用了未经定义的函数或者构造函数参数
	'''
	pass
class FileLoadFail(Exception):
	u'''
	文件加载失败所抛出的异常
	'''
	pass
class UrlNotExsit(Exception):
	u'''
	所使用的URL不存在导致抛出的异常
	'''
	pass
class PluginLoadFail(Exception):
	u'''
	插件加载失败抛出的异常
	'''
	pass

current_app=1
class App():
	u'''
	App类，zoom框架的核心类，主要功能由此实现。
	'''
 	cache_buffer={}
 	u'''
 	这是一个存放缓存文件的字典。
 	@note: 仅仅当cache为True时，启用该缓存策略。 
 	'''
	cache=False
	u'''
	缓存模式启用标志，默认为True，即启用缓存模式，当为False时关闭。
	缓存模式下当读取html或者静态资源时，
 	首先在其中查找，如果存在该资源，则直接可以从字典中读取。
 	否则，从磁盘中加载该资源，并存入cache_buffer。
 	@note: 考虑关闭缓存模式的情况

 	1.缓存模式下将消耗额外内存,如果静态资源较多时，可能造成资源紧张.

 	2.此外在缓存模式下，当修改html文件时，内存中的资源不会刷新，可能给调试造成不必要的麻烦。

	'''
	url_handler={}
	u'''
	全部URL处理函数的字典
	@note: 默认,自动加载如下若干项：
	
	1.^/static/css/.+$   =>  static_handler(request)  

	2.^/static/js/.+$    =>  static_handler(request) 

	3.^/static/pic/.+$   =>  static_handler(request) 

	4.^/static/file/.+$  =>  static_handler(request) 

	5.^/static/fonts/.+$ =>  static_handler(request) 

	6.^.+[.]html$        =>  template_handler(request) 

	7.^.+[.]htm$         =>  template_handler(request) 

	8.^.+/404.html$      =>  default404_handler(request) 

	'''
	url_pattern={}
	u'''
	预编译的URL正则表达式

	@note: 为了加快正则表达式的解析速度，URL正则表达式进行预编译，并存储在内存中，
	以供使用。
	'''
	port=8000
	u'''
	服务器默认的端口号，可以进行设置，默认为8000.

	@note: 如果端口号已经被占用，则启动失败。
	'''

	name="ZoomApp"
	u'''
	所开发的APP的名称
	@note: 默认名称为ZoomApp
	'''

	debug=False
	u'''
	调试模式启用的标志
	@note: 默认为False(调试模式下，禁用缓存和多线程)
	'''

	multiThread=False
	u'''
	多线程模式启用的标志
	@note: 默认为False
	'''

	installed_plugin=[]
	u'''
	已安装的插件

	@note: 默认为空，可以使用append进行添加
	'''

	installed_job=[]
	u'''
	初始化APP时进行的任务。
	@note: 默认为空，可是使用append进行添加
	'''

	static_path=[
		{'path':os.path.join('.','static','css'),'url':'/static/css/.+'},
		{'path':os.path.join('.','static','js'),'url':'/static/js/.+'},
		{'path':os.path.join('.','static','pic'),'url':'/static/pic/.+'},
		{'path':os.path.join('.','static','file'),'url':'/static/file/.+'},
		{'path':os.path.join('.','static','fonts'),'url':'/static/fonts/.+'}
	]
	u'''
	静态资源的搜索路径的地址

	@note:
	默认路径如下所示:

	I{windows:}

	.\\static\\css\\...

	.\\static\\js\\...

	.\\static\\pic\\...

	.\\static\\file\\...

	.\\static\\fonts\\...

	I{Linix/Mac os X:}

	./static/css/...

	./static/js/...

	./static/pic/...

	./static/file/...

	./static/fonts/...

	'''

	template_path=[
		{'path':os.path.join('.','template')}
	]
	u'''
	模板搜索路径：

	I{Window：}

	.\\template\...

	I{Linux/Mac os X}

	./template/...

	'''

	def add_Job(self,job): 
		u'''
		添加系统初始化的任务

		@note: 

		1.从self.installed_job中可以搜索已安装的插件。

		2.所添加的任务，在APP调用run()时，执行。
		
		'''
		self.installed_job(job)
		pass
			

	def init(self):
		u'''
		APP启动时进行的初始化设置

		@note:

		1.绑定默认URL处理函数

		2.完成提前设置的

		'''
		self.add_url('^/static/css/.+$',static_handler)
		self.add_url('^/static/js/.+$',static_handler)
		self.add_url('^/static/pic/.+$',static_handler)
		self.add_url('^/static/images/.+$',static_handler)
		self.add_url('^/static/file/.+$',static_handler)
		self.add_url('^/static/fonts/.+$',static_handler)

		self.add_url('^/css/.+$',static_handler)
		self.add_url('^/js/.+$',static_handler)
		self.add_url('^/pic/.+$',static_handler)
		self.add_url('^/file/.+$',static_handler)
		self.add_url('^/fonts/.+$',static_handler)
		self.add_url('^/images/.+$',static_handler)

		self.add_url('^/.+[.]html$',template_handler)
		self.add_url('^/.+[.]htm$',template_handler)
		self.add_url('^/404.html$',default404_handler)
		for job in self.installed_job:
			job()
		#for p in self.installed_plugin:
			#print "ss"+p.__name__
			#setattr(self,p.__name__,p(self))
			
	def add_url(self,url,handler):
		u'''
		绑定默认URL和对应的处理函数

		@param url:所指定的URL，并进行预编译。URL使用python正则表达式表示，支持带参数的表达形式。

			例如 (?P<name>.+)

		'''
		self.url_handler[url]=handler
		self.url_pattern[url]=re.compile(url)

	def url(self,route):
		u'''
		修饰器，将相应函数绑定在特定的URL上

		@param route:所绑定的路由

		@note:  URL为绑定的路由,例子如下所示

			>>> import zoom
			... app=zoom.App()
			... @app.url() 
			... def index(request):
			... 	return "hello world"
 		'''
		def wapper(func):
			self.add_url(route,func)
			return func
		return wapper

	def template(self,template):
		u'''
		修饰器，将相应模板绑定在特定的响应函数上，
		使之返回模板在所相应函数给出的字典上渲染的值。

		@param template: 模板名称

		@note:  URL为绑定的路由,例子如下所示

			>>> import zoom
			... app=zoom.App()
			... @app.template('index.html') 
			... @url('/')
			... def index(request):
			... 	return {'Username':'zoom'}
 		'''

		def wapper(func):
			@functools.wraps(func)
			def template_render(request):
				return render(template,func(request))
			return template_render	
		return wapper

	def plugin(self):
		u'''
		修饰器，将插件绑定在对于的app上

		@note:  URL为绑定的路由,例子如下所示

			>>> import zoom, zoomDB
			... app=zoom.App()
			... @app.plugin()
			... class User(zoomDB.Model):
			... 	pass
 		'''

		def wapper(cls):

			setattr(self,cls.__name__,cls(self))
			self.installed_plugin.append(cls)
			#print getattr(self,cls.__name__
			return cls
		return wapper

	def __init__(self,** option):
		u'''
		App的构造函数，参数如下所示:

		@param name: App的名称，默认为zoomApp

		@param port: App的端口号, 默认为8000

		@param debug: 调试模式是否启动，默认为False

		@param cache: 缓存模式是否启动，默认为True

		@param multiThread: 多线程模式是否启动，默认为False

		'''
		global current_app
		if 'name' in option:
			self.name=option['name']
		if 'port' in option:
			self.port=option['port']
		if 'debug' in option:
			self.debug=option['debug']
		if 'cache' in option:
			self.cache=option['cache']
		if 'multiThread' in option:
			self.multiTread=option['multiThread']
		if self.debug==True:
			self.multiThread=False
			self.cache=False

		current_app=self
		#self.initPlugin()
		print "App %s has launched..." % self.name
		

	def run(self):
		u'''
		服务器启动。

		@note: 默认开启单线程模式，在multiThread为True时，开启多线程模式，可以同时接受多个用户请求。

		'''
		self.init()
		if self.multiThread==False:
			server=Server()
		else:
			server=MultiServer()
		#print self.url_handler
		server.serve_forever()

def html(URL):
	u'''
	得到html文件的内容

	@param url: html文件对应的URl

	@return: 该url对应的html文件的内容

	例子如下所示:
		>>> from zoom import *
		... app=App()
		... @app.url('/')
		... def index(request):
		... 	return html('index.html')

	'''
	return template_handler(Request(url=URL))

def render(template,**dict):
	u'''
	模板渲染

	@param template: 模板的URL

	@param dict: 渲染的字典

	例子如下所示:
		>>> from zoom import *
		... app=App()
		... @app.url('/')
		... def index(request):
		... 	return render('Hello {{ name }}!',UserName='zoom'})

	'''
	return template

def default404_handler(request):

	u'''
	返回出现404错误的网页内容

	默认为 error 404
	用户可以改写这部分，使用新的404错误页面

	'''

	return "error 404"

def static_handler(request):
	u'''
	默认静态资源请求处理函数

	@note : 函数从默认的搜索路径下寻找并返回内容

	'''
	global current_app
	url=request.url
	for path,urlpattern in [ (i['path'],i['url']) for i in current_app.static_path]:
		if url.split('/')[-1] in os.listdir(path):
			
			if url in current_app.cache_buffer:
				return current_app.cache_buffer[url]
			else:
				try:
					#print os.path.join(path,url.split('/')[-1])
					f=open(os.path.join(path,url.split('/')[-1]),'rb')
					if current_app.cache==True:
						current_app.cache_buffer[url]=f.read()
						f.close()
						#print  'csslen'+len(current_app.cache_buffer[url])
						return current_app.cache_buffer[url]
					else:
						s=f.read()
						f.close()
						return s
				except:
					raise FileNotExsit
					
	print 'fail '+url.split('/')[-1] 

	return current_app.url_handler['^/404.html$'](request)

def template_handler(request):
	u'''
	默认模板资源

	@note : 函数从默认的搜索路径下寻找并返回内容

	'''
	#print request.url
	global current_app
	url=request.url
	template_name=url.split('/')[-1]
	#print 'url'+url
	for path in [i['path'] for i in current_app.template_path]:
		if template_name in os.listdir(path):
			if url in current_app.cache_buffer:
				return current_app.cache_buffer[url]
			else:
				try:
					
					if current_app.cache==True:
						print 'cache'
						f=open(os.path.join(path,template_name),'rb')
						current_app.cache_buffer[url]=f.read()
						f.close()
						return current_app.cache_buffer[url]
					else:
						print 'no cahce'
						f=open(os.path.join(path,template_name),'rb')
						s= f.read()
						f.close()
						return s
				except:
				#	print os.path.join(path,template_name)
					raise FileNotExsit
	#print "template_handler"
	return current_app.url_handler['^/404.html$'](request)

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import cgi
import urlparse
from SocketServer import ThreadingMixIn
import threading 

class RequestHandler(BaseHTTPRequestHandler):
	u'''
	解析URL,派发任务

	分别处理 get和post二类不同的请求

	'''
	def do_GET(self):
		'''
		处理get请求
		'''
		self.send_response(200)
		self.end_headers()
		request=Request(method="get",url=self.path)
		resp=dispatch(request)
		if not isinstance(resp,Redirect):
			self.wfile.write(resp)	
		else:
			raise web.seeother(resp.url)
	 
		return 

	def do_POST(self):
		u'''
		处理post请求
		'''
	
		request=Request(method="post",url=self.path)
		
		form=cgi.FieldStorage(
			fp=self.rfile,
			headers=self.headers,
			environ={
				'REQUEST_METHOD':'POST',
				'CONTENT_TYPE':self.headers['Content-Type']
				}
			)
		
		#print form.keys()
		for field in form.keys():
			field_item=form[field]
			if field_item.filename:
				request.file_name=field_item.filename
				request.file_data=field_item.file.read()
				request.file_len=len(file_data)
			else:	
				request.add_attr(field,form[field].value)
		resp=dispatch(request)
		if not isinstance(resp,Redirect):
			self.send_response(200)
			self.end_headers()
			self.wfile.write(resp)
		else:
			self.send_response(303)
			self.send_header('location',resp.url)
			self.end_headers()
	 
		return 

class Server(HTTPServer):
	u'''
	单线程web服务器，每次可以处理单个http请求。
	'''
	def __init__(self):
		host='0.0.0.0'
		u'''
		主机名 默认为0.0.0.0， 响应全部来源的http请求
		'''
		#print _current_app
		port=current_app.port
		HTTPServer.__init__(self,(host,port),RequestHandler)

class MultiServer(ThreadingMixIn,Server):
	u'''
	多线程web服务器，每次可以处理多个http请求，通过继承Server类实现
	'''
	pass

class Request:
	u'''
	http请求的封装
	'''
	method='get'
	u'''
	http请求类型

	包括 "get" 和 "post"

	默认为 "get"
	'''
	para={}
	u'''
	http请求包括的get参数
	'''
	url=""
	u'''
	http请求的url参数
	'''
	file_name=None
	u'''
	上传的文件名
	'''
	file_data=None
	u'''
	上传的文件数据
	'''
	file_len=None
	u'''
	上传的文件长度
	'''
	def __init__(self,**args):
		u'''
		Request的构造函数，参数如下

		@param method: http请求的方法

		@param url: http请求的url

		@param file_name: 上传的文件名

		@param file_data: 上传的文件类型

		@param file_len:  上传的文件长度

		'''
		if 'method' in args:
			self.method=args['method']
		if 'url' in args:
			self.url=args['url']
		if 'file_name' in args:
			self.filename=args['file_name']
		if 'file_data' in args:
			self.file_data=args['file_data']
		if 'file_len' in args:
			self.file_len=args['file_len']

	def add_attr(self,key,value):
		u'''
		为Request增加属性

		@param key: 健

		@param value: 值

		例如对于如下URL参数可以有
		
			>>> string="/home/?P<UserName>zoom/?P<ID>1234567"
			... request=Request(url=string)
			... request.add_attr("UserName","zoom")
			... request.add_attr("ID","1234567")

		'''
		self.para[key]=value

	def __getitem__(self,key):
		u'''
		获取属性

		@param key: 键

			>>> string="/home/?P<UserName>zoom/?P<ID>1234567"
			... request=Request(url=string)
			... request.add_attr("UserName","zoom")
			... request.add_attr("ID","1234567")		
			... print request["UserName"]
			zoom
			... print request["ID"]
			1234567

		'''
		return self.para[key]

	def __setitem__(self,key,value):
		u'''
		设置属性

		@param key: 键

		@param value: 值

			>>> string="/home/?P<UserName>zoom/?P<ID>1234567"
			... request=Request(url=string)
			... request["UserName"]="zoom"
			... request["ID"]="1234567"		
			... print request["UserName"]
			zoom
			... print request["ID"]
			1234567
			... request["UserName"]="mooz"
			... request["ID"]="7654321"
			... print request["UserName"]
			mooz
			... print request["ID"] 
			7654321
		'''
		self.para[key]=value

	def __delitem__(self,key):
		u'''
		删除属性

		@param key: 键
 
			>>> string="/home/?P<UserName>zoom/?P<ID>1234567"
			... request=Request(url=string)
			... request.add_attr("UserName","zoom")
			... request.add_attr("ID","1234567")		
			... print request["UserName"]
			zoom
			... print request["ID"]
			1234567
			... del request["UserName"]
			... del request["ID"]
			... print request["UserName"]
			None
			... print request["ID"] 
			None
		'''
		del self.para[key]

	def __iter__(self):
		u'''
		对于request属性的遍历器

		示例如下：
			>>> string="/home/?P<UserName>zoom/?P<ID>1234567"
			... request=Request(url=string)
			... request["UserName"]="zoom"
			... request["ID"]="1234567"
			... for attr in request:
			... 	print attr
			zoom
			1234567
		'''
		return iter(self.para)

	def __contains__(self,target):
		u'''
		request是否存在某个属性

		@param targe: 属性名称
		
		示例如下所示
			>>> string="/home/?P<UserName>zoom/?P<ID>1234567"
			... request=Request(url=string)
			... request['UserName']=='zoom'
			... print 'UserName' in request
			True
			... print 'username' in request 
			False
		'''
		return target in self.para
class Redirect:
	url=""
	def __init__(self,url):
		self.url=url
	pass

def dispatch(request):
	u'''
	处理url请求的派发任务

	@return: 返回处理的内容

	'''
	global current_app
	for urlpattern in current_app.url_handler:
		match=current_app.url_pattern[urlpattern].match(request.url)
		if match :
			kv=match.groupdict()
			for key in kv:
				request.para[key]=kv[key]
			#print urlpattern,request.url
			return current_app.url_handler[urlpattern](request)
	return current_app.url_handler['^/404.html$'](request)
	

if __name__=='__main__':

	if sys.argv[1]=='-new':
		app_name=sys.argv[2]
		os.mkdir(app_name)
		os.mkdir(os.path.join(app_name,'template'))
		os.mkdir(os.path.join(app_name,'static'))
		os.mkdir(os.path.join(app_name,'static','css'))
		os.mkdir(os.path.join(app_name,'static','js'))
		os.mkdir(os.path.join(app_name,'static','pic'))
		os.mkdir(os.path.join(app_name,'static','fonts'))
		os.mkdir(os.path.join(app_name,'static','file'))
		try:
			f=open(os.path.join(app_name,app_name+".py"),'w')
			code="""#_*_ coding: utf8 _*_
import sys
sys.path.append('..')
from zoom import *
app=App(name='%s')

@app.url('/')
def index(request):
	return 'hello world'

if __name__=='__main__':
	app.run()

			""" % (sys.argv[2])
			f.write(code)
			f.close()
			print "create app  successfully !"
		except:
			print "create fail "
			pass

	elif syste.argv[1]=='-help':

		pass
	elif sys.argv[1]=='-version':

		pass
	elif sys.argv[1]=='-run':

	#app=App(port=8001)	
	#@app.url('^/$')
	#def index(request):
	#	return "hello world"
	#app.run()

		pass
