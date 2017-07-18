# coding=utf-8
from datetime import datetime,date,timedelta
from ext import db
class Identity(db.Model):
	pzn_group = [1,1,1]# present group, 1 for mindfulness group, each site corresponding to female (0),male (1),unknown(2)
	__tablename__ = 'Identity'

	id = db.Column(db.Integer, primary_key=True,autoincrement=True)
	gender = db.Column(db.Integer)# 0 for girls, 1 for boys, and 2 for unknown...
	openid = db.Column(db.String(128),unique=True)
	group = db.Column(db.Integer)# randomly assigned according to gender
	pzn_sessn = db.Column(db.Integer)# start from zero
	max_sessn = db.Column(db.Integer)# twelve by default, forty for superior users
	train_state = db.Column(db.Integer)# 0 for not trained
	created_time = db.Column(db.DateTime, nullable=False)
	daily_ratn = db.Column(db.String(1500))# stored in formatted string, one section for each day
	usr_name = db.Column(db.String(80))
	name = db.Column(db.String(28))
	email = db.Column(db.String(120))
	session_key = db.Column(db.String(120))
	fdbck = db.Column(db.String(3000))# stored in formatted string, one section for each day, 10 - 30 characters for each day

	def __init__(self,openid,group=1,gender = 2,pzn_sessn=1,max_sessn=12,putin_data = '',session_key = ''):
		self.session_key = session_key
		self.created_time = str(datetime.now())
		self.openid = openid
		self.group = group
		self.state = 0#not trained
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
	def update_id_unique_record(cls,openid,uploaded_data='',gender=2,pzn_sessn=1,max_sessn=12):
		est_rcd = cls.get_by_openid(openid)#existing records
		if est_rcd:
			est_rcd.max_sessn = max_sessn
			if est_rcd.state and est_rcd.pzn_sessn<=max_sessn:
				t_n = datetime.now()# time of now
				d_n = t_n.date()#date of now
				yr,mt,dy = est_rcd.created_time[0:10].split()#update date and pzn_sessn if necessary
				dt = date(yr,mt,dy)#created date
				if d_n>dt:
					diff = int(str(d_n-dt).split(" ",1)[0])
					if diff>(est.pzn_sessn-1):# not capable of missed more than one day, in codes here, multiple training will be allowed after multiple missed day
						est_rcd.pzn_sessn += 1
						if diff>est.pzn_sessn-1:#if diff of date still >1
							est_rcd.fdbck +=  "<_>pull_strt_from_" + est_rcd.created_time + "<_>"
							est_rcd.created_time = str(d_t + timedelta(days=diff-est.pzn_sessn+1))+ estrcd.created_time[11:]
			est_rcd.fdbck += '<_>Relogin<_>'
			return (est_rcd,0)# set a flag for session.add to be skipped in Main.py
		cls.pzn_group[gender] = 1 - cls.pzn_group[gender]# 
		rst = cls(openid=openid,group = cls.pzn_group[gender],gender=gender,pzn_sessn = pzn_sessn,max_sessn = max_sessn)
		# to satisfy superior editting of changing pzn_sessn or max_sessn
		return (rst,1)
		


class AudioInfo(db.Model):
	__tablename_ = 'AudioInfo'# forty audio files in total

	id = db.Column(db.Integer, primary_key=True)
	sessn_No = db.Column(db.Integer)
	AudioName = db.Column(db.String(80))
	AudioLinks = db.Column(db.String(128))
