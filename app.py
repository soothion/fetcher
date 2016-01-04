from login import login
from lxml import etree,html
import requests
import time

class fetcher(object):
	
	__path__ = 'http://www.jikexueyuan.com/path/'
	
	def __init__(self):
		self.cookies = login().getCookies()
		self.s = requests.Session()
		
	def get(self,url):
		print('正在爬取'+url)
		try:
			content = self.s.get(url,cookies=self.cookies).text
		except Exception as e:
			print('error:',e)
			time.sleep(10)
			content = self.s.get(url,cookies=self.cookies).text
			
		em = '<em style="padding: 0px 10px">|</em><span><a href="http://passport.jikexueyuan.com/sso/login" postion="index_index_header" rel="nofollow" jktag="&posGP=112001&posOper=900002">登录</a></span>'
		if not content.find(em)==-1:
			cookies = login().login()
			content = self.s.get(url,cookies=cookies).text
			self.cookies = cookies
		return content
		
	def getMp4(self,url):
		content = self.get(url)
		root = etree.HTML(content)
		video = root.xpath('//source/@src')[0]
		return video
	
	def getPath(self):
		content = self.get(self.__path__)	
		root = etree.HTML(content)
		nodes = root.xpath('//a[@class="pathlist-one cf"]')
		paths = []
		for node in nodes:
			path = {}
			path['title'] = node.find('div/h2').text
			path['description'] = node.find('div/p').text
			path['url'] = node.get('href')
			path['chapter'] = self.getChapter(path['url'])
			paths.append(path)
		return paths
		
	def getChapter(self,url):
		content = self.get(url)
		root = etree.HTML(content)
		nodes = root.xpath('//div[@class="pathstage mar-t30"]')
		chapters = []
		for node in nodes:
			chapter = {}
			chapter['title'] = node.find('div[@class="pathstage-txt"]/h2').text
			chapter['description'] = node.find('div[@class="pathstage-txt"]/p').text
			chapter['courses'] = self.getCourse(node)
			chapters.append(chapter)
		return chapters
		
	def getCourse(self,node):
		nodes = node.xpath('.//ul[@class="cf"]/li')
		courses = []
		for node in nodes:
			course = {}
			n = node.xpath('.//h2[@class="lesson-info-h2"]/a')[0]
			course['title'] = n.text
			course['url'] = n.get('href')
			course['lessons'] = self.getLesson(course['url'])
			courses.append(course)
		return courses
			
	def getLesson(self,url):
		content = self.get(url)
		root = etree.HTML(content)
		nodes = root.xpath('div[@class="lesson-box"]/li')
		lessons = []
		for node in nodes:
			lesson = {}
			lesson['title'] = node.xpath('.//h2/a')[0].text
			lesson['description'] = node.xpath('.//p')[0].text
			lesson['url'] = node.xpath('.//h2/a')[0].get('href')
			lesson['mp4'] = self.getMp4(lesson['url'])
			lessons.append(lesson)
		return lessons
		
		
fetcher = fetcher()
paths = fetcher.getPath()
print(paths)

	