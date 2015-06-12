#_*_ coding: utf8 _*_
import sqlite3,os
import zoom
__doc__=u'''


zoomDB模块-包含zoom对数据库的支持

python 版本需求 2.7以上

无需第三方模块支持	

'''
class QuerySet:
	u'''
	查询的结果集
	'''
	def __init__(self,meta,data):
		u'''
		QuerySet的构造函数如下

		@param meta: 元数据

		@param data: 数据


		'''
		self._meta=meta.keys()
		self._meta.reverse()
		self._data=data
		for i in range(len(self._meta)):
			setattr(self,self._meta[i],[ item[i]  for item in self._data])
	def __str__(self):
		u'''
		返回元组的字符串形式
		'''
		return str(self._data)
	def all(self):
		u'''
		返回全部元组

		 	>>> from zoom import *
 			>>> from zoomDB import *
 			... @app.plugin()
 			... @field("UserName","varchar(50")
 			... class User(Model)	
		'''
		return self._data
	def filter(self,*args):
		u'''
		进行过滤，只保留所需的属性

		 	>>> from zoom import *
 			>>> from zoomDB import *
 			... app=zoom.App()
 			... @app.plugin()
 			... @field("UserName","varchar(50)")
 			... @field("age","int")
 			... class User(Model):
 			... 	pass
 			... print app.User.select('UserName like %%zoom%%').filter('UserName','age')
 			[('zoom1',12),('zoom2',16),('zoom3',19)]
 			... print app.User.select('UserName like %%zoom%%').filter('age')
 			[(12,),(16,),(19,)]
 			.. print app.User.select('UserName like %%zoom%%').filter('UserName')
 			[('zoom1',),('zoom2',),('zoom3',)]

		'''
		arg_list=[]
		for arg in args:
			if arg in dir(self):
				arg_list.append(getattr(self,arg))
		return zip(*arg_list)
	def __len__(self):
		u'''
		返回查询的结果的元祖个数

		>>> from zoom import *
		>>> from zoomDB import *
		... app=zoom.App()
		... @app.plugin()
		... @field("UserName","varchar(50)")
		... class User(Model):
		... 	pass
		... res=app.User.select("UserName like '%%zoom%%'"")
		... print len(res) 
		10
		... res=app.User.get("User='zoom'")
		... print len(res)
		1
		'''
		return len(self._data[0])
meta_store=[]
class Model:
	u'''
	数据模型的基本父类
	'''
	
	u'''
	元数据的字典
	'''
	constraint=''
	u'''
	数据模型的字典
	'''
	conn=None
	u'''
	数据库连接
	'''
	_constraint_=''
	def __init__(self,app):
		#print 'before ',dir(self)
		self.meta={}
		self.attr_list=[]
		self.conn=None
		self.constraint=''
		self._constraint_=''
		u'''
		Model的构造函数。
		通过对Model进行拓展，得到可以使用的数据模型

		示例如下：

 			>>> from zoom import *
 			>>> from zoomDB import *
  			... app=App()
 			... @app.plugin()
 			... class User(zoomDB.Model):
 			... 	pass
		'''
		self.app=app
		self.conn=sqlite3.connect(app.name+".db")
		self.cur=self.conn.cursor()
		meta={}
		#print 'before',self.meta
	 	for attr in dir(self):
	 		if attr.startswith('_field_'):
	 			#print attr
	 			field_name=attr.split('_')[2]
	 			#print field_name
	 			self.meta[field_name]=getattr(self,attr)
	 			#print self.meta
	 	sql="select name from sqlite_master where type='table'"
		if self.__class__.__name__ not in [ table[0]for table in self.cur.execute(sql).fetchall()]:
			sql='create table %s (' % self.__class__.__name__+'\n'
			meta=[m[1] for m in meta_store if m[0] == self.__class__.__name__ ]
			#print 'meta',meta_store
			t=[]
			for attr in meta:
				t.append(attr+' '+self.meta[attr])
			t.reverse()
			sql+=',\n'.join(t)+self._constraint_+");"
			#print sql
			self.cur.execute(sql)
			self.conn.commit()
			#print "yes"

	def select(self,args=None):
		u'''
		从数据模型中选出所需数据

		@param args: 选择的条件，格式类似sql，默认为None，即选出全部数据
 			
 		@return : 包含查询结果元祖的列表

 		示例如下：

 			>>> from zoom import *
 			>>> from zoomDB import *
 			... app=zoom.App()
 			... @app.plugin()
 			... @field("UserName","varchar(50)")
 			... class User(zoomDB.Model):
 			... 	pass
 			... print app.User.select('UserName like %%zoom%%')
 			[('zoom1'),('zoom2'),('zoom3')]
		'''
		if args!=None:
			sql="select * from %s where %s ;" % (self.__class__.__name__,args)
		else:
			sql="select * from %s ;" % self.__class__.__name__
		#print sql
		return QuerySet(self.meta,self.cur.execute(sql).fetchall())

	def get(self,args):
		u'''
		获取单个值，若结果数量唱过离歌则抛出异常

		@param args: 参数风格类似sql语句

			>>> from zoom import *
 			>>> from zoomDB import *
 			... app=zoom.App()
 			... @app.plugin()
 			... @field("UserName","varchar(50)")
 			... class User(zoomDB.Model):
 			... 	pass
 			... print app.User.get('UserName like %%zoom%%')
 			[('zoom1')]

		'''
		sql="select * from %s where %s ;" % (self.__class__.__name__,args)
		res= self.cur.execute(sql).fetchall()
		if len(res) > 1:
			raise Exception(u'元素个数超过1')
		else:
			return QuerySet(self.meta,[res[0]])

	def delete(self,args=None):
		u'''
		删除元祖 

		@param args: 删除的元祖条件           

			>>> from zoom import *
 			>>> from zoomDB import *
 			... app=zoom.App()
 			... @app.plugin()
 			... @field("UserName","varchar(50)")
 			... class User(zoomDB.Model):
 			... 	pass
 			... print app.User.delete('UserName like %%zoom%%')
 			[('zoom1'),('zoom2'),('zoom3')]

		'''
		if args!=None:
			sql="delete from %s where %s ;" % (self.__class__.__name__,args)
		else:
			sql="delete from %s ;" % (self.__class__.__name__)
		self.cur.execute(sql)
		self.conn.commit()

	def execute(self,sql):
		u'''
		执行sql语句

			>>> from zoom import *
 			>>> from zoomDB import *
 			... app=zoom.App()
 			... @app.plugin()
 			... @field("UserName","varchar(50)")
 			... class User(zoomDB.Model):
 			... 	pass
 			... app.User.execute("select * from User;")
 
		'''
		self.cur.execute(sql)
		self.conn.commit()

	def insert(self,*args):
		u'''
		插入输入

		示例如下所示：		

			>>> from zoom import *
 			>>> from zoomDB import *
 			... app=zoom.App()
 			... @app.plugin()
 			... @field("UserName","varchar(50)")
 			... class User(zoomDB.Model):
 			... 	pass
 			... app.User.insert('zoom')
 	 
		'''
		t=[]
		for attr in args:
			if isinstance(attr,str):
				t.append("'"+str(attr)+"'")
			else:
				t.append(str(attr))
 
		sql="insert into %s values(%s);" % (self.__class__.__name__,','.join(t))
		print sql
		self.cur.execute(sql)
		self.conn.commit()

	def clear(self,table=None):
		u'''
		清除数据表

			>>> from zoom import *
 			... from zoomDB import *
 			... app=zoom.App()
 			... @app.plugin()
 			... @ield("UserName","varchar(50)")
 			... class User(zoomDB.Model):
 			... 	pass
 			... app.User.clear()
		'''
		if table==None:
			try:
				os.remove(self.app.name+".db")
				print "clear success"
			except:
				print "clear fail"
		else:
			sql='delete table %s' % table
			self.cur.execute(sql)
			self.conn.commit()

def field(name,type,*constraint):
	u'''
	对数据模型绑定域

	示例如下
		>>> from zoom import *
		... from zoomDB import *
		... @field("UserName","varchar(50)")
		... @field("email","varchar(50)")
		... @field("age","int")
		... class User(model): 
		... 	pass
						
	'''
	def wapper(cls):
		#print 'field',isinstance(cls,Model)
		constraint_str=''
		for item in constraint:
			constraint_str+=' '+item
		setattr(cls,'_field_'+name,type+constraint_str)
		#setattr(cls,name,None)
		meta_store.append((cls.__name__,name))
		return cls	
	return wapper

def constraint(*constraint):
	u'''
	约束条件

	示例如下所示

		>>> from zoom import *
		... from zoomDB import *
		... app=zoom.App()
		... @app.plugin()
		... @field("UserName","varchar(50)")
		... @field("age","int")
		... @constraint("age>10")
		... class User(zoomDB.Model):
		... 	pass
 
	'''
	def wapper(cls):
		constraint_str=''
		for item in constraint:
			constraint_str+='\n'+item
		setattr(cls,'_constraint_',constraint_str)
		return cls
	return wapper
 

