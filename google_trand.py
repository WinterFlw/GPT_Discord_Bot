import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
from pytrends.request import TrendReq
rc('font', family = 'AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

def trand(keywords: list):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list = keywords, timeframe = 'today 5-y')
    trenddf = pytrend.interest_over_time()
    return trenddf

"""
keywords = ["더위","에어컨"]
print(trand(keywords))
"""