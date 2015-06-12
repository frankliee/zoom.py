#_*_ coding: utf8 _*_
import sqlite3,os
import zoom
from threading import Thread
from functools import wraps
from time import sleep
__doc__=u''''
zoomJob.py 实现简单的对任务的定制

python 版本需求 2.7以上

无第三方模块需求

'''
def asy(func):
	u'''
	修饰器，异步函数

	被修饰的函数单独作为一个线程，可以异步执行

	示例如下所示：

		>>>	@asy
		...	def loop1():
		...		while True:
		...			time.sleep(1)
		...			print 'loop1'
		...	def loop2():
		...		while  True:
		...			time.sleep(1)
		...			print 'loop2'
		...	loop1()
		...	loop2()
		loop1
		loop2
		loop2
		lopp1
		...
	'''
	@wraps(func)
	def wrapper(*args,**kwargs):
		t=Thread(target=func,args=args,kwargs=kwargs)
		t.start()
		return t
	return wrapper


def timer(second=1,minute=0,hour=0,day=0):
	u'''
	修饰器，提供定时功能

	示例如下所示：

		>>> from zoom import *
		... from zoomJob import *
		... @timer
		... def job():
		... 	print "This is a job"
		... job()
		This is a job
		This is a job
		...

	'''
	time=second*1+minute*60+hour*3600+day*3600*24
	def real_wrapper(func):
		@wraps(func)
		@asy
		def wrapper(*args,**kwargs):
			while(True):
				sleep(time)
				func(*args,**kwargs)
		return wrapper
	return real_wrapper

if __name__=='__main__':
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

	
