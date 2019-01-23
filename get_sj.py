# 根据url获取数据

import global_var
import threading
import requests
import json
import pymysql
import re

question_url = global_var.var.url
question_times = global_var.var.get_times
mysql_ip = global_var.var.mysql_ip
mysql_uname = global_var.var.mysql_uname
mysql_pwd = global_var.var.mysql_pwd
mysql_database = global_var.var.mysql_database
#拼接url
get_url = question_url.replace("question","api/v4/questions")
get_url = get_url + "/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&"
# get_url = "https://www.zhihu.com/api/v4/questions/275359100/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=100&offset=0&platform=desktop&sort_by=default"

#根据次数获取参数
get_time = []
if int(question_times) % 20 == 0:
    get_num = int(question_times)/20
    for i in range(0,int(get_num)):
        get_time.append(0+i*20)
else:
    print("参数错误")
    exit

#print(get_time)

#根据参数获取所有url链接
url = []
for i in get_time:
    url.append(get_url+"limit=20&offset=%s&platform=desktop&sort_by=default"%(i))
# print(url)

# 根据url爬取数据


header = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0",
"Accept-Encoding": "gzip", #指定gzip编码，br编码requests无法识别
"x-requested-with": "fetch"
}
def get_info(info_url):#获取单个url的所有内容
    session = requests.session()
    session.headers = header #添加请求头
    repl = session.get(info_url)
    content = json.loads(repl.content) #以json格式接收传回文件
    info = []
    for c in range(0,19):
        oneinfo = [content['data'][c]['id'],content['data'][c]['content']]
        info.append(oneinfo)
    session.close
    return info
#初步数据清洗，删去标签链接

#根据url插入数据库
def threadone(threadurl):
    db = pymysql.connect(mysql_ip,mysql_uname,mysql_pwd,mysql_database )#链接数据库
    cursor = db.cursor()
    for get_u in threadurl:
        # print(threadurl)
        info = get_info(get_u)
        for one in info:
            sql = 'insert into zhzh(answer_id,content) values("{}","{}")'.format(one[0],pymysql.escape_string(one[1]))
            # print(sql)
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except Exception as e:
                print(e)
                # 如果发生错误则回滚
                db.rollback()
    db.close
#多线程爬取
threads=[]
num = len(url)
num = num/5
for n in range(0,5):
    t = threading.Thread(target=threadone,args=(url[int(n*num):int((n+1)*num)],))
    threads.append(t)

for t_num in range(0,5):
    # threads[t_num].setDaemon(True)
    threads[t_num].start()

for t_num in range(0,5):
    threads[t_num].join()


