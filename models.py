# coding=utf-8
from datetime import datetime,date,timedelta
from ext import db
class Identity(db.Model):
	#pzn_group = [1,1,1]# present group, 1 for mindfulness group, each site corresponding to female (0),male (1),unknown(2),this settings is removed since it doen't work so well 
#when app is restarted several times
	__tablename__ = 'Identity'

	id = db.Column(db.Integer, primary_key=True,autoincrement=True)
	gender = db.Column(db.Integer)# 2 for girls, 1 for boys, and 0 for unknown...
	openid = db.Column(db.String(128),unique=True)
	group = db.Column(db.Integer)# randomly assigned according to gender
	pzn_sessn = db.Column(db.Integer)# start from zero
	max_sessn = db.Column(db.Integer)# twelve by default, forty for superior users
	train_state = db.Column(db.Integer)# 0 for not trained
	created_time = db.Column(db.DateTime, nullable=False)
	daily_ratn = db.Column(db.String(1500))# stored in formatted string, one section for each day
	usr_name = db.Column(db.String(200))
	name = db.Column(db.String(28))
	email = db.Column(db.String(120))
	session_key = db.Column(db.String(120))
	fdbck = db.Column(db.String(8000))# stored in formatted string, one section for each day, 10 - 30 characters for each day,also added is user_info_log

	def __init__(self,openid,group=1,gender = 0,pzn_sessn=1,max_sessn=14,putin_data = '',session_key = ''):
		self.session_key = session_key
		self.created_time = str(datetime.now())
		self.openid = openid
		self.group = group
		self.train_state = 0#not trained
		self.pzn_sessn = pzn_sessn
		self.max_sessn = max_sessn
		self.gender = gender
		ptn_data =  putin_data.split('<ptn_>',4)		
		if len(ptn_data)==5:
			self.usr_name,self.name,self.email,self.fdbck,self.daily_ratn =ptn_data
		else:
			self.fdbck = putin_data
			self.usr_name,self.name,self.email,self.daily_ratn = ('Bugs','Is','Nothg','BtChallnge')
			#deal with wrong number of <ptn_> or default parametres for data_checking
	def split_putn(self,putin_data):# since in __init__, self hasn't been created, 
		#so this part of code couldn't replace the similar one in __init__
		ptn_data = putin_data.split('<ptn_>',4)
		if len(ptn_data)==5:
			self.usr_name,self.name,self.email,self.fdbck,self.daily_ratn =ptn_data
		else:
			self.fdbck = ptn_data
			#print(self.fdbck)
			self.usr_name,self.name,self.email,self.daily_ratn = ('Bugs','Is','Nothg','BtChallnge')
			#deal with wrong number of <ptn_> or default parametres for data_checking
		return self
	def ptn_data(self):
		return "<ptn_>".join([self.usr_name,self.name,self.email,self.fdbck,self.daily_ratn])
	def merge_ptn_data(self,short_dt = '',seq = -2):#std_p could be less than zero, -2 by default to add new info to fdbck
		ds1 = list(self.ptn_data().split('<ptn_>',4))
		if len(short_dt):# only insert non-empty string
			ds2 = list(short_dt.split('<ptn_>'))
			if len(ds2)==5:
				seq=0#if all data uploaded, merged from the beginning
			for ii in range(0,len(ds2)):
				#print('ds1: '+ds1[ii+seq] +' ds2: '+ds2[ii] +'ii: ' + str(ii) + 'seq: ' + str(seq))
				ds1[ii+seq] += ds2[ii]
		return self.split_putn('<ptn_>'.join(ds1))
	@classmethod
	def get_by_openid(cls, openid):
		try:
			return cls.query.filter_by(openid=openid).first()
		except:# in case that database doesn't exist
			#print "for in-line debugging"
			return 0
	@classmethod
	def update_id_unique_record(cls,openid,uploaded_data='',gender=0,pzn_sessn=1,max_sessn=14,train_state = 0,merge_seq = -2,session_key=0):
		est_rcd = cls.get_by_openid(openid)#existing records
		if est_rcd:
			if not est_rcd.gender:# After Regist,the gender would be initialized with 0, and group hasn't been set at this time
				try:
					lst_rcd = cls.query.filter_by(gender=gender)[-1]#find last record and make present record in a different group
					err = lst_rcd.gender
				except:# in case that record doesn't exist
					lst_rcd = cls(openid = 'example_for_gender_'+str(gender),gender=gender,group=0)#Create a sample record in control group
				est_rcd.group = 1 - lst_rcd.group#make it in the different group
			if gender:#only updated when gender is not 0(if gender is uploaded, it won't be set zero in Main.py),but group won't be updated
				est_rcd.gender = gender
				est_rcd.fdbck += "<_gender_" + str(gender)#Log the updates of gender
			est_rcd = est_rcd.merge_ptn_data(short_dt = uploaded_data,seq = merge_seq)# by default start merging from  fdbk
			#est_rcd.max_sessn = max_sessn# This Updates has to be commited onto databases, change this so max_sessn could be changed back in the database
			est_rcd.created_time = str(est_rcd.created_time)
			if train_state:
				est_rcd.train_state = train_state# only update train_state into 1, not backward
			if est_rcd.train_state and est_rcd.pzn_sessn<=est_rcd.max_sessn:
				t_n = datetime.now()# time of now
				d_n = t_n.date()#date of now
				yr,mt,dy = est_rcd.created_time[0:10].split('-')#update date and pzn_sessn if necessary
				yr = int(yr)
				mt = int(mt)
				dy = int(dy)
				dt = date(yr,mt,dy)#created date
				if d_n>dt:
					diff = int(str(d_n-dt).split(" ",1)[0])
					if diff>(est_rcd.pzn_sessn-1):# not capable of missed more than one day, in codes here, multiple training will be allowed after multiple missed day
						est_rcd.pzn_sessn += 1# this if is only executed on the second day
						est_rcd.train_state = 0# reset the state to 0
						if diff>est_rcd.pzn_sessn-1:#if diff of date still >1
							est_rcd.fdbck +=  "<_>pull_strt_from_" + est_rcd.created_time + "<_>"
							est_rcd.created_time = datetime.strptime(str(dt + timedelta(days=diff-est_rcd.pzn_sessn+1)).split('.')[0]+ ' ' + \
est_rcd.created_time[11:19],'%Y-%m-%d %H:%M:%S')
			est_rcd.fdbck += '<_>Log:<_>'
			if session_key:
				est_rcd.session_key=session_key
			return (est_rcd,0)# set a flag for session.add to be skipped in Main.py
		rst = cls(openid=openid,group = -1,gender=gender,pzn_sessn = pzn_sessn,max_sessn = max_sessn,putin_data = uploaded_data,session_key=session_key)#group set to -1 to show that it hasn't been set, and the participant thus won't be able to fetch audioInfo
		return (rst,1)
		


class AudioInfo(db.Model):
	__tablename_ = 'AudioInfo'# forty audio files in total

	id = db.Column(db.Integer, primary_key=True)
	sessn_No = db.Column(db.Integer)
	Name = db.Column(db.String(80))
	Links = db.Column(db.String(128))
	group = db.Column(db.Integer)
	@classmethod
	def get_Info(cls,sessn_No=1,group=1):
		a_rcd = cls.query.filter_by(sessn_No = sessn_No,group = group).first()
		audioInfo = {'name':a_rcd.Name,'src':a_rcd.Links}
		return audioInfo
