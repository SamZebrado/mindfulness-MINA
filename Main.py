# coding=utf-8
import urllib
import urllib2
import json
# flask
#from DeEnc.WXCrypt import WXBizDataCrypt as WXCrypt
from flask import Flask,request,jsonify
from ext import db
from models import Identity
# flask end
# gevent
from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
# gevent end

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

with app.app_context():
	db.create_all()

audioInfo ={
		'name':'Testing title from server',
		'author':'Sammuel Zebradoe',
		'src':	'http://szdatabucket1-1253981734.cossh.myqcloud.com/lxAudio_40_Days/lsn_1.mp3'#'http://dx.sc.chinaz.com/Files/DownLoad/sound1/201707/8934.mp3'
	}

@app.route('/tag/')
def index():
	return "SZ loves Ana"
@app.route('/brothers/')
def brothers():
	return "小熊，兔纸，你们要加油啊，哈哈哈哈哈哈哈哈"
@app.route('/room506/')
def roommate():
	return "山舟，来，周嘉涛，秦王元；\n猴季，Mr.Sulu，大磊，米老"
@app.route('/server/audioInfo/',methods = ['POST'])
def wx_server():
	
	return jsonify({'audioInfo':audioInfo})
@app.route('/UserLog/',methods=['POST'])
def wx_UserLog():
	req_data = json.loads(request.get_data())
	openid = req_data[u'openid']
	(record_anew,flag_anew) = Identity.update_id_unique_record(openid=openid)#fetch the anew flag
	db.session.merge(record_anew)
	db.session.commit()
	app.logger.debug("in UserLog")
	app.logger.debug(record_anew.created_time)
	return jsonify({'pzn_sessn':record_anew.pzn_sessn})#max sessn can also be returned to extend training plans for the participant

@app.route('/UserRegist/',methods=['GET','POST'])
def wx_UserRegist():
	appId = 'wxde4ed04d17675e14'
	if request.method=='POST':
		req_data = json.loads(request.get_data())
		#app.logger.debug('res')
		#app.logger.debug(json.dumps(req_data))
		#return req_data[u'code']
		#encData = req_data.encryptedData
		url = 'https://api.weixin.qq.com/sns/jscode2session?appid=wxde\
4ed04d17675e14&secret=c12283859e80a742ef233b73eafaff33&\
js_code='+req_data[u'code']+'&grant_type=authorization_code'
		app.logger.debug(url)
		f = urllib2.urlopen(url)
		res = json.loads(f.read())
		f.close()
		app.logger.debug(res)		#iv = req_data.iv
		#session_key and openid should be saved, while session_key shouldn't be transed by web
		openid = res[u'openid']
		(record_anew,flag_anew) = Identity.update_id_unique_record(openid=openid)#fetch the anew flag
		app.logger.debug("in UserRegist before commit")
		app.logger.debug(record_anew.created_time)
		db.session.merge(record_anew)
		db.session.commit()
		app.logger.debug("in UserRegist after commit")
		app.logger.debug(record_anew.created_time)
		try:
			return jsonify({'openid':res[u'openid']})
		except:
			return res[u'errmsg']
		
	else:
		return '<h1> you are not allwed to get anything unless post<h1>'

if __name__ =='__main__':
	app.run(host = '0.0.0.0',port = 443,ssl_context=("Crts/214194239870590.pem","Crts/214194239870590.key"))#http_server = WSGIServer(('', 5000), app)
#http_server.serve_forever()

