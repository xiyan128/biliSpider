import datetime
import pprint

import pandas as pd

import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as pt
import pymongo

# pt.set_credentials_file(username='shaoxiyan', api_key='Eyva2U1xQqyApKD6aGQ3')
py.sign_in('shaoxiyan', 'Eyva2U1xQqyApKD6aGQ3')

conn = pymongo.MongoClient(host='localhost',port=27017)
  # 创建数据库
bilibili = conn['bilibili']
  # 创建数据集合
madData = bilibili['mad']

for by in ["view", "favorite", "coin", "danmaku", "share", "like", "dislike"]:
  print(by)
  df = pd.DataFrame(list(madData.distinct(key="_id").sort(by, pymongo.DESCENDING).limit(10)))
  pprint.pprint(df)
