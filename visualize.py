import datetime
import pymongo
import pprint
import plotly.plotly as py
import plotly.tools as pt
import plotly.graph_objs as go
import pandas as pd

py.sign_in('*****', '*****') # api key 请自行获取

conn = pymongo.MongoClient(host='localhost',port=27017)
  # 创建数据库
bilibili = conn['bilibili']
  # 创建数据集合
madData = bilibili['mad']

pipeline = [
  {"$group": {
    "_id": {
      "$dateToString": {
        "format": "%Y-%m-%d",
        "date": "$pubDate"
      }
    },
    "totalFavorite": {"$sum": "$favorite"},
    "totalView": {"$sum": "$view"},
    "totalCoin": {"$sum": "$coin"},
    "count": {"$sum": 1}
  }
  },
  {"$sort": { "_id" : -1}}
]

lt = list(madData.aggregate(pipeline))
df = pd.DataFrame(lt)

pprint.pprint(df[:5])

count = go.Scatter(
          x=df['_id'],
          y=df['count'])

# view = go.Scatter(
#           x=df['_id'],
#           y=df['totalView'])

# coin = go.Scatter(
#           x=df['_id'],
#           y=df['totalCoin'])

# favorite = go.Scatter(
#           x=df['_id'],
#           y=df['totalFavorite'])

data = [count]

layout = dict(
    title = "投稿量变化(精确到日)"
)

fig = dict(data=data, layout=layout)

py.plot(fig, filename = "fig")
# py.image.save_as(fig, filename='a-simple-plot.png')