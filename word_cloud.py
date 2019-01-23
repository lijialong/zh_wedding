# 数据词云分析

import pymysql
import global_var
import re
import matplotlib.pyplot as plt
from wordcloud import wordcloud
from wordcloud import ImageColorGenerator
import jieba
import collections

mysql_ip = global_var.var.mysql_ip
mysql_uname = global_var.var.mysql_uname
mysql_pwd = global_var.var.mysql_pwd
mysql_database = global_var.var.mysql_database

def wash_info(one_info):#初步清洗数据
    septone = str(one_info).replace(" ","").replace("   ","").replace("\n","")
    restr = r'<[^\s]*?>'
    recom = re.compile(restr)
    stop_list = re.findall(recom,septone)
    stop_list = list(set(stop_list))
    for stop_word in stop_list:
        septone = septone.replace(stop_word,"")
    return septone


db = pymysql.connect(mysql_ip,mysql_uname,mysql_pwd,mysql_database )#链接数据库
cursor = db.cursor()
sql = "select * from zhzh"
info = []
try:
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        info.append(wash_info(row[2]))
except Exception as e:
    raise e
finally:
    db.close

# 将数据储存成一段str
n = 0
txt = ''
for i in info:
    txt = txt + i
    n = n+1
    print(n)

#设置过滤池
resl = jieba.cut(txt)
word_list = []
for sent in resl:
    word_list.append(sent)
stop_list = []
stop = collections.Counter(word_list)
for x in stop.keys():
    if stop[x] > 200:
        stop_list.append(x)
    elif stop[x] <10:
        stop_list.append(x)
for st in stop_list:
    stop.pop(st)

#生产词云
cloud = wordcloud.WordCloud(font_path="./q.ttf",
background_color='black', 
max_words=400, #最大号字体，如果不指定则为图像高度 
max_font_size=100, #画布宽度和高度，如果设置了msak则不会生效 
width=600, 
height = 400, 
margin = 2, #词语水平摆放的频率，默认为0.9.即竖直摆放的频率为0.1 
prefer_horizontal = 0.8)
wc = cloud.generate_from_frequencies(stop)
# news = ts.guba_sina(show_content=True)
# print(news.ix[3])
plt.imshow(wc) #不现实坐标轴 
plt.axis('off') #绘制词云 #plt.figure(dpi = 600) image_colors = ImageColorGenerator(color_mask) #plt.imshow(wc.recolor(color_func=image_colors)) 重新上色， 
plt.show()