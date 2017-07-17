# coding=utf-8
from datetime import datetime
from ext import db
class Identity(db.Model):
	pzn_group = [1,1,1]# present group, 1 for mindfulness group, each site corresponding to female (0),male (1),unknown(2)
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True,autoincrement=True)
	gender = db.Column(db.Integer)# 0 for girls, 1 for boys, and 2 for unknown...
	openid = db.Column(db.String(128),unique=True)
	group = db.Column(db.Integer)# randomly assigned according to gender
	pzn_sessn = db.Column(db.Integer)# start from zero
	max_sessn = db.Column(db.Integer)# twelve by default, forty for superior users
	created_time = db.Column(db.DateTime, nullable=False)
	daily_ratn = db.Column(db.String())# stored in formatted string, one section for each day
	usr_name = db.Column(db.String(80))
	name = db.Column(db.String(28))
	email = db.Column(db.String(120))
	session_key = db.Column(db.String(120))
	fdbck = db.Column(db.String(3000))# stored in formatted string, one section for each day, 10 - 30 characters for each day

	def __init__(self,openid,group=1,gender = 2,pzn_sessn=0,max_sessn=12,putin_data = ''):
		self.created_time = datetime.now()
		self.openid = openid
		self.group = group
		self.pzn_sessn = pzn_sessn
		self.max_sessn = max_sessn
		trsd_data =  putin_data.split('<ptn_>')
		if len(trsd_data)==5:
			self.daily_ratn,self.usr_name,self.name,self.email,self.fdbck =trsd_data
		else:
			self.fdbck = putin_data
			self.daily_ratn,self.usr_name,self.name,self.email = ('Bugs','Is','Nothg','BtChallnge')
			#deal with wrong number of <ptn_> or default parametres for data_checking
	@classmethod
	def get_by_openid(cls, openid):
		try:
			return cls.query.filter_by(openid=openid).first()
		except:# in case that database doesn't exist
			return 0
	@classmethod
	def create_id_unique_record(cls,openid,uploaded_data,gender=2,pzn_sessn=0,max_sessn=12):
		exst_record = cls.get_by_openid(openid)
		if exst_record:
			return exst_record
		self.pzn_group[gender] = 1 - self.pzn_group[gender]# 
		rst = cls(openid=openid,group = cls.pzn_group,gender=gender,pzn_sessn = pzn_sessn,max_sessn = max_sessn)
		# to satisfy superior editting of changing pzn_sessn or max_sessn
		return rst
		


class AudioInfo(db.Model):
	__tablename_ = 'AudioInfo'# forty audio files in total

	id = db.Column(db.Integer, primary_key=True)
	sessn_No = db.Column(db.Integer)
	AudioName = db.Column(db.String(80))
	AudioLinks = db.Column(db.String(128))
