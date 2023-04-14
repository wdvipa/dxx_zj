# -*- coding: utf-8 -*-
"""
//支持青龙和actions定时执行
//使用方法：创建变量 名字：dxx 内容的写法：
//openid(抓包获得), 名字(cardNo) ,区域(nid)
//每个账号用回车键隔开
//例如: 
o****1, 123 ,1684
o****2, 66 ,1546
//如需推送将需要的推送写入变量dxx_fs即可多个用&隔开
如:变量内输入push需再添加dxx_push变量 内容是push的token即可
"""
import requests
import os
import time
import re
import json

requests.urllib3.disable_warnings()

#初始化环境变量开头
ttoken = ""
tuserid = ""
push_token = ""
SKey = ""
QKey = ""
ktkey = ""
msgs = ""
datas = ""
msg = ""
#检测推送
if "dxx_fs" in os.environ:
    fs = os.environ.get('dxx_fs')
    fss = fs.split("&")
    if("tel" in fss):
        if "dxx_telkey" in os.environ:
            telekey = os.environ.get("dxx_telkey")
            telekeys = telekey.split('\n')
            ttoken = telekeys[0]
            tuserid = telekeys[1]
    if("qm" in fss):
        if "dxx_qkey" in os.environ:
            QKey = os.environ.get("dxx_qkey")
    if("stb" in fss):
        if "dxx_skey" in os.environ:
            SKey = os.environ.get("dxx_skey")
    if("push" in fss):
        if "dxx_push" in os.environ:
            push_token = os.environ.get("dxx_push")
    if("kt" in fss):
        if "dxx_ktkey" in os.environ:
            ktkey = os.environ.get("dxx_ktkey")
if "dxx" in os.environ:
    datas = os.environ.get("dxx")
else:
    print('您没有输入任何信息')
    exit
groups = datas.split('\n')
#初始化环境变量结尾

class dxxanelQd(object):
    def __init__(self,openid,cardNo,nid):
        #地区
        self.nid = nid
        #名字
        self.cardNo = cardNo
        # openid
        self.openid = openid
        ##############推送渠道配置区###############
        # 酷推qq推送
        #self.ktkey = ktkey
        # Pushplus私聊推送(废弃,顶上定义变量即可)
        #self.push_token = push_token
        # ServerTurbo推送(废弃,顶上定义变量即可)
        #self.SendKey = SKey
        # Qmsg私聊推送(废弃,顶上定义变量即可)
        #self.QmsgKey = QKey
        # Telegram私聊推送
        self.tele_api_url = 'https://api.telegram.org'
        self.tele_bot_token = ttoken
        self.tele_user_id = tuserid
        ##########################################


    def getAccessToken(self,openid):
        time_stamp = str(int(time.time()))  #获取时间戳
        url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/login/we-chat/callback?callback=https%3A%2F%2Fqczj.h5yunban.com%2Fqczj-youth-learning%2Findex.php&scope=snsapi_userinfo&appid=wx56b888a1409a2920&openid=" + openid + "&nickname=空城&headimg=&time=" + time_stamp + "&source=common&sign=&t=" + time_stamp
        res = session.get(url)
        access_token = res.text[45:81]
        print("获取到AccessToken:", access_token)
        return access_token


    def getCurrentCourse(self,access_token,msg):
        url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/current?accessToken=" + access_token
        res = session.get(url)
        res_json = json.loads(res.text)
        if (res_json["status"] == 200):
            msg = msg + "获取到最新课程代号:" + res_json["result"]["id"]
            print("获取到最新课程代号:", res_json["result"]["id"])
            return res_json["result"]["id"]
        else:
            msg = msg + "获取最新课程失败！"
            print("获取最新课程失败！")
            return msg


    def getJoin(self,access_token, current_course, nid, cardNo,msg):
        data = {
            "course": current_course,  # 大学习期次的代码，如C0046，本脚本已经帮你获取啦
            "subOrg": None,
            "nid": nid,  # 团组织编号，形如N003************
            "cardNo": cardNo  # 打卡昵称
        }
        url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/user-api/course/join?accessToken=" + access_token
        res = session.post(url, json=data)
        print("打卡结果:", res.text)
        res_json = json.loads(res.text)
        if (res_json["status"] == 200):
            msg = msg + "打卡成功"
            print("打卡成功")
            return msg , res.text
        else:
            msg = msg + "打卡失败！"
            print("打卡失败！")
            return msg


    def getsign(self,access_token,msg):
        data = {}
        url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/user-api/sign-in?accessToken=" + access_token
        res = session.post(url, json=data)
        print("签到结果:", res.text)
        res_json = json.loads(res.text)
        if (res_json["status"] == 200):
            msg = msg + "签到成功"
            print("签到成功")
            return msg
        else:
            msg = msg + "签到失败！"
            print("签到失败！")
            return msg


    def getTasks(self,access_token,msg):
        a = 0
        b = 0
        c = 0
        while a < 4 :
            data = {}
            url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/user-api/course/study?accessToken=" + access_token + "&id=C00470021 "
            res = session.post(url, json=data)
            #print("任务结果:", res.text)
            res_json = json.loads(res.text)
            if (res_json["status"] == 200):
                a += 1
                b += 1
                print("任务第"+ str(a) +"次成功")
            else:
                a += 1
                c += 1
                print("任务第"+ str(a) +"次失败")
        msg = msg + "签到" + str(b) + "次成功," + str(c) + "次失败"
        print("签到" + str(b) + "次成功," + str(c) + "次失败")
        return msg
    


    def getinfo(self,access_token,msg):
        url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/user-api/info?accessToken=" + access_token
        res = session.get(url)
        res_json = json.loads(res.text)
        if (res_json["status"] == 200):
            msg = msg + "获取到积分数:" + str(res_json["result"]["score"])
            print("获取到积分数:", str(res_json["result"]["score"]))
            return msg
        else:
            msg = msg + "获取积分数失败！"
            print("获取积分数失败！")
            return msg 
    
    # Qmsg私聊推送
    def Qmsg_send(msg):
        if QKey == '':
            return
        qmsg_url = 'https://qmsg.zendee.cn/send/' + str(QKey)
        data = {
            'msg': msg,
        }
        requests.post(qmsg_url, data=data)

    # Server酱推送
    def server_send(self, msg):
        if SKey == '':
            return
        server_url = "https://sctapi.ftqq.com/" + str(SKey) + ".send"
        data = {
            'text': self.name + "大学习通知",
            'desp': msg
        }
        requests.post(server_url, data=data)

    # 酷推QQ推送
    def kt_send(msg):
        if ktkey == '':
            return
        kt_url = 'https://push.xuthus.cc/send/' + str(ktkey)
        data = ('大学习完成，点击查看详细信息~\n' + str(msg)).encode("utf-8")
        requests.post(kt_url, data=data)

    #Telegram私聊推送
    def tele_send(self, msg: str):
        if self.tele_bot_token == '':
            return
        tele_url = f"{self.tele_api_url}/bot{self.tele_bot_token}/sendMessage"
        data = {
            'chat_id': self.tele_user_id,
            'parse_mode': "Markdown",
            'text': msg
        }
        requests.post(tele_url, data=data)
        
    # Pushplus推送
    def pushplus_send(msg):
        if push_token == '':
            return
        token = push_token
        title= '大学习通知'
        content = msg
        url = 'http://www.pushplus.plus/send'
        data = {
            "token":token,
            "title":title,
            "content":content
            }
        body=json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type':'application/json'}
        re = requests.post(url,data=body,headers=headers)
        print(re.status_code)


    def main(self):
        global msgs
        # 获取token
        access_token = self.getAccessToken(openid)
        # 获取最新的章节
        current_course = self.getCurrentCourse(access_token,msg)
        # 打卡任务
        res = self.getJoin(access_token, current_course, nid,cardNo,msg)
        #每日签到
        self.sign = self.getsign(access_token,msg)
        #每日任务
        self.Tasks = self.getTasks(access_token,msg)
        #积分查询
        self.info = self.getinfo(access_token,msg)
        #"大学习签到结果",
        #"大学习签到成功：\n" + "状态码：" + str(res["status"]) + "\n课程ID: " +
        #current_course + "\n签到学号: " + res["result"]["cardNo"] +
        #"\n签到时间: " + res["result"]["lastUpdTime"], "", DD_BOT_TOKEN,
        #DD_BOT_SECRET)
        msgs = msgs + '\n' + msg

i = 0
n = 0
print("已设置不显示账号密码等信息")
while i < len(groups):
  n = n + 1
  group = groups[i]
  profile = group.split(',')
  openid = profile[0]
  cardNo = profile[1]
  nid = profile[2]
  msgs = msgs + '\n' + "用户 " + cardNo + " 的签到结果"
  print("第" + str(n) + "个用户 " + cardNo + " 开始签到")

  session = requests.session()
  session.headers = {
    'User-Agent':
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4'
  }
  run = dxxanelQd(openid, cardNo ,nid)
  run.main()
  time.sleep(5)
  i += 1
else:
    #dxxanelQd.server_send( msgs )
    dxxanelQd.kt_send( msgs )
    #dxxanelQd.Qmsg_send(dxxanelQd.name+"\n"+dxxanelQd.email+"\n"+ msgs)
    #dxxanelQd.tele_send(dxxanelQd.name+"\n"+dxxanelQd.email+"\n"+ msgs)
    dxxanelQd.pushplus_send( msgs )
