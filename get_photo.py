# 用于获取问题图片

import pymysql
import global_var
import re
import threading
from urllib import parse
from urllib import request
import requests
import json
import base64
import random

mysql_ip = global_var.var.mysql_ip
mysql_uname = global_var.var.mysql_uname
mysql_pwd = global_var.var.mysql_pwd
mysql_database = global_var.var.mysql_database
access_token = global_var.var.access_token
thraed_num = global_var.var.thread_num

def get_photo_url(text):
    re_str = r"https://[^\s]*?\.jpg"
    replay = re.compile(re_str).findall(text)
    return replay

#获取图片url
db = pymysql.connect(mysql_ip,mysql_uname,mysql_pwd,mysql_database )#链接数据库
cursor = db.cursor()
sql = "select * from zhzh"
info = []
try:
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        for url in get_photo_url(row[2]):
            info.append(url)
except Exception as e:
    raise e
finally:
    db.close
info = list(set(info))
print('>>>>>>总共有%s条url<<<<<<'%(len(info)))
#借助百度ai人像识别清洗图片，并将图片数据存入数据库
request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
request_url = request_url + "?access_token=" + access_token
headers = {'Content-Type': 'application/json'}

def wash_ptoto(url_list):
    db = pymysql.connect(mysql_ip,mysql_uname,mysql_pwd,mysql_database )#链接数据库
    cursor = db.cursor()
    for img_url in url_list:
        try:
            response = request.urlopen(img_url)
            imgtxt = response.read()
            base64_data = base64.b64encode(imgtxt)
            params = {"image":base64_data,"image_type":"BASE64","face_field":"age,faceshape,face_probability,beauty,facetype,gender,race"}
            response = requests.post(request_url,data=params,headers=headers)
            # print(response.text)
            content = json.loads(response.text)
            age = str(content['result']['face_list'][0]['age'])
            beauty = str(content['result']['face_list'][0]['beauty'])
            gender = content['result']['face_list'][0]['gender']['type']
            race = content['result']['face_list'][0]['race']['type']
            sql = 'insert into img(img_url,age,beauty,gender,race) values("{}","{}","{}","{}","{}")'.format(img_url,age,beauty,gender,race)
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except Exception as e:
                print(e)
                # 如果发生错误则回滚
                db.rollback()
            print(">>>>>>提交%s成功"%(img_url))
        except Exception:
            pass
    db.close
#多线程处理

threads=[]

for i in range(0,thraed_num):
    exec("temp%s = []"%(str(i)))

for ur in info:
    exec("temp%s.append('%s')"%(str(random.randint(0,thraed_num-1)),ur))

for i in range(0,thraed_num):
    exec("t%s = threading.Thread(target=wash_ptoto,args=(temp%s,))"%(str(i),str(i)))
    exec("threads.append(t%s)"%(str(i)))

for thraed in threads:
    thraed.start()

for thraed in threads:
    thraed.join

