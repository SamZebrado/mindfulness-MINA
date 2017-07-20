from models import *
i1,r = Identity.update_id_unique_record(openid = 'xyszkd',uploaded_data="abc<ptn_>bcd<ptn_>email<ptn_>Old feedback<ptn_>\
old Rating")
i2 = i1.merge_ptn_data(short_dt="New feedback<ptn_>~~~new B")
print i2.fdbck

