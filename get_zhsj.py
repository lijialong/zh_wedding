# coding=utf-8
# from selenium import webdriver
import json
import requests
# import sys
# sys.getdefaultencoding
# driver = webdriver.Chrome(executable_path=".\scrpylearn\chromedriver.exe")
header = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0",
"Accept-Encoding": "gzip",
"x-requested-with": "fetch"
}
url = "https://www.zhihu.com/api/v4/questions/275359100/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=100&offset=0&platform=desktop&sort_by=default"
session = requests.session()
session.headers = header
repl = session.get(url)
# print(str(repl.content,encoding = "utf-8"))
# rr = bytes.decode(str(repl.content),encoding="utf-8")
content = json.loads(repl.content)
print(content['paging']['next'])
