#coding:utf-8
import requests
'''
https://api.weixin.qq.com/cgi-bin/media/upload?access_token=ACCESS_TOKEN&type=TYPE
调用示例（使用curl命令，用FORM表单方式上传一个多媒体文件）：
curl -F media=@test.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=ACCESS_TOKEN&type=TYPE"
'''

#获取微信access_token
def get_token():
    payload_access_token={
        'grant_type':'client_credential',
        'appid':'wxa4847d2b3f7c1d33',
        'secret':'d17e7d1274709972858b3435251ed990'
    }
    token_url='https://api.weixin.qq.com/cgi-bin/token'
    r=requests.get(token_url,params=payload_access_token)
    dict_result= (r.json())
    return dict_result['access_token']


#curl -F media=@test.jpg "https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=ACCESS_TOKEN"

#access_token = get_token()
#print access_token
access_token = "12_pzB6T4Tz4-fL8AYbVozRiohw8BINzLbkXyVFwz52K3t6frFvBnA_b6-cqLWacMcRtwtGDmovYf24HDNMhtQWxc16_IInGwhPfUNQFY6-4L4hVW8uu4iXKDxzD6ENLHdADAWUQ"
def upload_img():
    data = {"media":"@C:\Users\haish\Desktop\shapush\1.jpg"}
    #imgurl = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=TYPE"%access_token
    imgurl = "https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=%s&type=TYPE"%access_token
    r = requests.post(imgurl,data=data)
    result = (r.json())
    return result
    
print upload_img()
    
    
