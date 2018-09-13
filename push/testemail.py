#coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

_user = '1107760775@qq.com'
_pwd  = "wyimepwevqalgefe"
_to   = 'zhaoep@sinolines.com'

msg = MIMEMultipart('related')
# content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>','html','utf-8')
# msg.attach(content)

msg['Subject'] = Header(u"图片", 'utf-8')


with open("1.png","rb")as f:
    # 设置附件的MIME和文件名，这里是png类型:
    mime = MIMEBase('image', 'png', filename='1.png')
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename='1.png')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)
    
    # mime.add_header('Content-ID', "imageid")
    # msg.attach(mime)
    

try:
    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
    s.login(_user, _pwd)
    s.sendmail(_user, _to, msg.as_string())
    s.quit()
    print "Success!"
except smtplib.SMTPException,e:
    print "Falied,%s"%e 