import json
import re
import sys
from datetime import datetime
from imp import reload

from prettytable import PrettyTable

reload(sys)
# sys.setdefaultencoding('utf8')
import requests

session = requests.Session()
print("Abbhb创建于2024/3/6 侵权联系删除！\n")
print("https://gitee.com/abbhb/czbk_auto_script\n")
print("https://gitee.com/abbhb/czbk_auto_script")
print("\n")
print("https://m.ityxb.com/account这个地址是官网登录页，可以打开尝试密码，确认了再来刷!!!\n")
print("请注意，正常登录成功会输出studentId,请先去网站上确认好密码!!!\n")
username = input("请输入注册用的手机号:")
passwords = input("请输入注册时设置的密码:")
print("获取cookie中!\n")
password = {
    "username":username,
    "password":passwords,
    "userType":""
}
cookie_jar = session.post("https://m.ityxb.com/wx-back/wechat/auth/login",password).cookies

cookie = requests.utils.dict_from_cookiejar(cookie_jar)

print(f"cookie为{cookie}!\n")

YuXiUrl = "https://m.ityxb.com/wx-back/preview/student/list"
StudentIdGetUrl = "https://m.ityxb.com/static/js/studentPreview.5c00b02f05177e8af8bb.js"



Xuanke = "https://m.ityxb.com/wx-back/preview/student/info"
Kecheng = "https://m.ityxb.com/wx-back/course/student/list"
ShuaSHichang = "https://m.ityxb.com/wx-back/preview/student/updateProgress"


# 设置自定义的cookie
custom_cookie ={
    'SESSION': '81e97a77-5edc-4836-bea4-1fa0239f1641',
    '_uc_t_': '1%3B1%3B81e97a77-5edc-4836-bea4-1fa0239f1641%3Bbxg%3B1',
    'get-user-url': '126d917d48a3bdaa0d2125d008790ddd63672a0604b66a4d86f20010e90e5f1c556806d5492f3c04712b0581e7904d22',
    'zg_359878badcb44bf88a748ad7859455ea': '%7B%22sid%22%3A%201709700192652%2C%22updated%22%3A%201709700207007%2C%22info%22%3A%201709693055423%2C%22superProperty%22%3A%20%22%7B%5C%22platform%5C%22%3A%20%5C%22WX%5C%22%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22landHref%22%3A%20%22https%3A%2F%2Fm.ityxb.com%2Fteaching%2Fstudent%2Ff0b65db65dc74115bf869f1cebfca06e%2FcourseTab%2Fpreview%22%2C%22cuid%22%3A%20%22fa1adf8ef43b4d1da478633683f762b8%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201709700192652%7D',
    'zg_did': '%7B%22did%22%3A%20%2218e11a5b1b8b5e-085f1fb12d2756-4c657b58-1fa400-18e11a5b1b915c7%22%7D',
}
custom_cookie = cookie

# 设置伪装的头部，模拟正常浏览器的请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}


# 获取studentid
responsea_id = requests.get('https://m.ityxb.com/static/js/studentPreview.5c00b02f05177e8af8bb.js', headers=headers, cookies=custom_cookie)
if responsea_id.status_code == 200:
    # 打印响应内容
    # 解析 JSON 数据
    # 使用正则表达式匹配 studentId 的值
    match = re.search(r'studentId\s*:\s*"([^"]+)"', responsea_id.text)

    # 如果匹配成功，则打印 studentId 的值
    if match:
        student_id = match.group(1)
        print("studentId:", student_id)
    else:
        print("未找到 studentId")
        input(",按下任意键退出!")
        exit(0)

else:
    print('请求失败:', responsea_id.status_code)
    input("，按下任意键退出!")
    exit(0)

# 构造POST请求的数据
data = {
    'pageNum':1,
    'pageSize':3000
}
# 发送POST请求
response = requests.post(Kecheng, headers=headers, cookies=custom_cookie, data=data)

kecheng_data = []
total_kecheng = 0

'''
[
{
                "courseName": "JavaWeb程序设计任务教程 （第2版）",
                "isArchive": false,
                "imageUrl": "https://attachment-center.boxuegu.com/data/picture/univ/2021/09/10/09/579130901383427dadecd8afec7dc0b3.png",
                "active": true,
                "id": "f0b65db65dc74115bf869f1cebfca06e"
            }]
'''

# 检查响应状态码
if response.status_code == 200:
    # 打印响应内容
    # 解析 JSON 数据
    data = json.loads(response.text)
    if(data["success"] is True):
        print()
        kecheng_data =data["resultObject"]["list"]
        total_kecheng = data["resultObject"]["total"]
else:
    print('请求失败:', response.status_code)
    input("没有请求到任何课程，按下任意键退出!")
    exit(0)
# 没有课程提示用户退出
if total_kecheng == 0:
    input("没有请求到任何课程，按下任意键退出!")
    exit(0)
xuanzekechengobject = {}
is_xuanzekecheng = False
while is_xuanzekecheng is False:
    print("当前有如下课程，请输入序号选择:\n")
    tem = 1
    for i in kecheng_data:
        print(f"[{tem}] {i['courseName']}\n")
        tem += 1
    try:
        xuanzexuhao = int(input())
        if xuanzexuhao >0 and xuanzexuhao <= total_kecheng:
            is_xuanzekecheng = True
            xuanzekechengobject = kecheng_data[xuanzexuhao-1]
    except Exception as e:
        print(e+"\n")
        input("按下回车请重新选择")
print(f"当前处于课程 {xuanzekechengobject['courseName']} \n")
while str(input("输入y回车进入预习")) != 'y':
    pass

asdqw = {
    "studentId":student_id,
    "courseId":xuanzekechengobject["id"],
    "pageNum":1,
    "pageSize":3000,
    "type":5
}
response_jechengs = requests.post(YuXiUrl, headers=headers, cookies=custom_cookie, data=asdqw)
yuxi_data = []
yuxi_total = 0
# 检查响应状态码
if response_jechengs.status_code == 200:
    # 打印响应内容
    # 解析 JSON 数据
    dataasd = json.loads(response_jechengs.text)
    if(dataasd["success"] is True):
        yuxi_data =dataasd["resultObject"]["list"]
        yuxi_total = dataasd["resultObject"]["total"]
else:
    print('请求失败:', response_jechengs.status_code)
    input("没有请求到任何课程，按下任意键退出!")
    exit(0)
if yuxi_total == 0:
    input("没有请求到任何预习章节，按下任意键退出!")
    exit(0)

# 预习章节展示
print("预习章节列表如下\n")
table = PrettyTable(['章节名', '完成度', '开始时间', '结束时间'])
Need_Shuake = []
for sd in yuxi_data:
    table.add_row([sd["preview_name"], sd["progress100"], sd["create_time"], sd["end_time"]])
    # 将日期时间字符串转换为 datetime 对象
    date_time_obj = datetime.strptime( sd["end_time"], '%Y-%m-%d %H:%M:%S')

    # 获取当前时间
    current_time = datetime.now()

    # 判断给定日期时间是否已经过去
    if date_time_obj >= current_time:
        if int(sd["progress100"])<100:
            Need_Shuake.append(sd)

print(table)
print("\n")
input("按任意开始刷课，会自动刷结束时间内完成度没到100%的章节的视频部分！\n")

for shu in Need_Shuake:
    sdfa = {
        "previewId":shu["id"]
    }

    try:
        tempke = []
        response_info = requests.post(Xuanke, headers=headers, cookies=custom_cookie, data=sdfa)
        if response_info.status_code == 200:
            # 打印响应内容
            # 解析 JSON 数据
            dataasasd = json.loads(response_info.text)
            if (dataasasd["success"] is True):
                tempke = dataasasd["resultObject"]["chapters"][0]["points"]

        for ke_item in tempke:
            if int(ke_item["progress100"])>=100:
                continue
            gouzao = {
                "previewId":shu["id"],
                "pointId":ke_item["point_id"],
                "watchedDuration":ke_item["video_duration"]
            }
            response_s = requests.post(ShuaSHichang, headers=headers, cookies=custom_cookie, data=gouzao)
            if response_jechengs.status_code == 200:
                # 打印响应内容
                # 解析 JSON 数据
                print(f"恭喜你，{shu['preview_name']}-{ke_item['point_name']} 刷满了!\n")

    except Exception as e:
        print(e)
        print("\n")
        print(f"课程 {shu['preview_name']}刷失败了\n")