import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
import json
import redis


class login(object):
	__url__      = 'http://passport.jikexueyuan.com/sso/verify'
	__login__    = 'http://passport.jikexueyuan.com/submit/login?is_ajax=1&client=www'
	__username__ = 'username'
	__password__ = 'password'
	__redis__    = 'python_cookies'
	
	def __init__(self):
		self.r = redis.Redis(host='127.0.0.1',port='6379',db=0)
	
	def getCookies(self):
		cookies = self.r.get(self.__redis__)
		if not cookies:
			return self.login()
		cookies = json.loads(cookies.decode())
		return cookies
	
	def login(self):
		timestamp = str(int(datetime.now().timestamp()*1000))
		self.__url__ = self.__url__+'?'+timestamp
		
		s = requests.Session()
		r = s.get(self.__url__)
		file = BytesIO(r.content)
		img = Image.open(file)
		img.show()

		verify = input('input captch:')
		login_data = {
			'expire':7,
			'referer':'http://www.jikexueyuan.com/',
			'uname':self.__username__,
			'password':self.__password__,
			'verify':verify
		}
	
		response = s.post(self.__login__,params=login_data,cookies = r.cookies)
		result = json.loads(response.text)
		if result['status'] == 1:
			cookies = response.cookies.get_dict()
			self.r.set(self.__redis__,json.dumps(cookies))
			return cookies
		raise ValueError(result['msg'])
