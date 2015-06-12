#_*_ coding: utf8 _*_
import sqlite3,os
import zoom
import markdown
import sys,time
__doc__=u'''
zoomMD.py 提供markdown文档转换能力

python版本需求 2.7以上

第三方库需求 markdown （python 的markdown库）

'''
class MD:
	u'''
	提供markdown文档转换能力

	将所需转换的md文件存放在模板路径下，并绑定插件

		>>> from zoom import *
		... from zoomMD import *
		... app=App()
		... md=MD(app)

	'''
	def __init__(self,app):
		self.app=app
		self.path=app.template_path[0]['path']
		for item in os.listdir(self.path):
			if item.endswith('.md'):
				file=open(os.path.join(self.path,item),'r')
				string=file.read()
				md=markdown.Markdown(encoding="utf-8")
				html=md.convert(string.decode('utf-8')).encode('utf-8');
				head='''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
				'''
				end='''
</body>
</html>
				'''
				html=head+html+end
				file.close()
				file=open(os.path.join(self.path,item.replace(".md",".html")),'w')
				file.write(html)
				file.close()
				#time.sleep(1000)

if __name__=="__main__":
	app=zoom.App()
	md=MD(app)
	app.run()


