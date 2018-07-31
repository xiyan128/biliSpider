#encoding=utf8
import requests
import re
import pymongo # MongoDB
import json
import datetime
import time

# 如被封 IP 可打开代理
# import socks
# import socket

# socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 1086)
# socket.socket = socks.socksocket

def getOnePage(pn, ps=50):
  payload = {'rid': '24', 'pn': pn, 'ps': ps}

  try: 
    reqRaw = requests.get(baseUrl, params=payload, headers=headers).text
  except:
    print("Request error! Now on page %d" % pn)
    return
  

  # print(reqRaw)
  try:
    jsonDatas = json.loads(reqRaw)['data']['archives']
  except:
    print("Parse error! Now on page %d" % pn)
    return

  for jsonData in jsonDatas:


    doc = {
          'aid'       :   jsonData['aid'],
          'title'     :   jsonData['title'],
          'pubDate'   :   datetime.datetime.fromtimestamp(jsonData['pubdate']),
          'view'      :   jsonData['stat']['view'],
          'danmaku'   :   jsonData['stat']['danmaku'],
          'coin'      :   jsonData['stat']['coin'],
          'reply'     :   jsonData['stat']['reply'],
          'favorite'  :   jsonData['stat']['favorite'],
          'like'      :   jsonData['stat']['like'],
          'dislike'   :   jsonData['stat']['dislike'],
          'share'     :   jsonData['stat']['share'],
          'duration'  :   jsonData['duration'],
          'owner'     :   jsonData['owner']['mid'],
          'ownerName'     :   jsonData['owner']['name'],
          # 'tags'      :   re.findall(r'[#](.*?)[#]', jsonData['dynamic'])
          }
    # print(doc)
    madData.insert_one(doc)

if __name__=='__main__':
      
  # 打开数据库连接，mongodb默认端口为27017
  conn = pymongo.MongoClient(host='localhost',port=27017)
  # 创建数据库
  bilibili = conn['bilibili']
  # 创建数据集合
  madData = bilibili['mad']

  headers = {'user-agent':  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36' \
                            ' (KHTML, like Gecko) Chrome/50.0.2661.102 ' \
                            'Safari/537.36 '
            }

  # http://api.bilibili.com/x/web-interface/newlist?rid={rid}&pn={pn}&ps={ps}
  baseUrl = 'http://api.bilibili.com/x/web-interface/newlist' # 24:mad/amv

  N = 4756
  for pn in range(1, N):
    print(' Now on: %d' % pn, end='\r')
    # 尊敬服务器起见，调低了请求速度
    time.sleep(0.3)
    getOnePage(pn=pn)
