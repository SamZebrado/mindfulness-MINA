from models import *
i1,r = Identity.update_id_unique_record(openid = 'xyszkd',uploaded_data="I'm feedback<ptn_\
I'm d r<ptn_>")
i2 = i1.merge_ptn_data(short_dt="I'm B feedback<ptn_>I'm new B<ptn_>")
print i2.fdbck

