import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
from pytrends.request import TrendReq
rc('font', family = 'AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

"""
hl => Host Language의 약자로, Google 트렌드의 언어를 설정하는 파라미터(한국어는 'ko-KR'이다.)
tz =>  Timezone Offset의 약자로 UTCF부터의 시차를 분 단위로 표시(한국은 '540'이다.)
pn => south_korea 대한민국으로 설정
"""
def live_rank():
    pytrends = TrendReq(hl='ko-KR', tz=540)
    live_rank_list = pytrends.trending_searches(pn='south_korea')
    return(live_rank_list)


def trand(keywords: list):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list = keywords, timeframe = 'today 5-y')
    trenddf = pytrend.interest_over_time()
    return trenddf

"""
live_rank() ex:
print(live_rank())
trand() ex:
keywords = ["더위","에어컨"]
print(trand(keywords))
"""
