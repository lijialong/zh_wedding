# zh_wedding
用于爬取知乎某个征婚问题，并进行数据分析。

# 项目结构
1.get_zhsj.py 测试教学文件（项目爬取核心思想）
2.get_sj.py 爬取数据（采用多线程爬取存入数据库）
3.global_var.py 全局参数
4.zhzh.sql 数据库表文件
5.word_cloud.py 词云分析

# 数据分析

1.词云分析

# 项目进度

2019/1/23：完成数据爬取代码的编写
2019/1/23：词云分析完成

# 项目部署

1.clone
2.先用zhzh.sql创建zhzh表
3.让后修改global_var中的参数
4.运行get_sj获取数据
5.运行word_cloud进行词云分析