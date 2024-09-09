import requests
import json
import os
import time
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; E6883 Build/32.4.A.1.54; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36',   
    'Referer':'https://www.t00ls.com/members-profile-12894.html'
}

username = os.environ.get("T00LS_USERNAME")
password = os.environ.get("T00LS_PASSWORD")
questionid = os.environ.get("T00LS_QUESTIONID")
answer = os.environ.get("T00LS_ANSWER")
msg = []
logindata={
"action" :"login",
"username":username,  #填你的用户名，不要填ID
"password":password,   #密码的MD5值
"questionid":questionid, #问题编号，对照下面注释填写，若没有设置提问则此处随便填写
"answer":answer  #输入回答，若没有设置提问则此处随便填写，或不填
}


# questionid
# 1 母亲的名字
# 2 爷爷的名字
# 3 父亲出生的城市
# 4 您其中一位老师的名字
# 5 您个人计算机的型号
# 6 您最喜欢的餐馆名称
# 7 驾驶执照的最后四位数字

def login(session):
    loginurl="https://www.t00ls.com/login.json"
    response=session.post(url=loginurl,data=logindata,headers=headers)
    responsejson=json.loads(response.text)
    # cookies=response.cookies
    # with open("cookiefile","wb") as fn:
    #     pickle.dump(session.cookies,fn)
    try:
         status = responsejson["status"]
         formhash = responsejson["formhash"]
         global msg
         if status == "success":
             msg += [{"name": "登录信息", "value": "登录成功"}]
         else:
             msg += [{"name": "登录信息", "value": "登录失败"}]

         return status, formhash
    except:
        return "login_error"

def signin(session,formhash):
    singurl="https://www.t00ls.com/ajax-sign.json"
    signdata={
    "formhash":"",
    "signsubmit":"true"
    }

    # print(formhash)
    signdata["formhash"]=formhash
    response=session.post(url=singurl,data=signdata,headers=headers)
    #print(response.text)
    try:
        global msg
        result=json.loads(response.text)["message"]
        # 出现success为签到成功，alreadysign为已经签到过
        if result == "alreadysign":
            msg += [{"name": "签到信息", "value": "已经签到了"}]
        elif result == "success":
            msg += [{"name": "签到信息", "value": "签到成功"}]
        else:
            msg += [{"name": "签到信息", "value": "签到失败"}]

        return result
    except:
        print("Error,please give me issue")
        return "Error,please give me issue"

def webhook(result):
    webhookurl = "http://sc.ftqq.com/"
    sckey = ""#替换成自己的sckey
    requests.get(url=webhookurl + sckey + ".send?text=t00ls_signin_result&desp=" + result)

def main():
    session = requests.session()
    for i in range(3):
        try:
            result,formhash=login(session)
            if result == "success":
                signin(session, formhash)
            # if success:
            #     query_balance()
        except AttributeError:
            if i < 3:
                time.sleep(3)
                print("checkin failed, try #{}".format(i + 1))
                continue
            else:
                raise
        break

    global msg
    return "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])


if __name__ == '__main__':
    print(" T00ls 签到开始 ".center(60, "="))
    print(main())
    print(" T00ls 签到结束 ".center(60, "="), "\n")