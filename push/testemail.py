#coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import re
import datetime
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler

handler = logging.FileHandler('/home/www/push/emailtest.log')
handler.setLevel(logging.INFO)

# create a logging format

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger

logger.addHandler(handler)

_user = '1107760775@qq.com'
_pwd  = "wyimepwevqalgefe"
#_to   = 'zhaoep@sinolines.com'
recipients = ['28310231@qq.com', 'chenq@sinolines.com','zhouyn@sinolines.com']
bcc = ["1107760775@qq.com"]

msg = MIMEMultipart('related')
# content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>','html','utf-8')
# msg.attach(content)

msg['Subject'] = Header(u"船期图片", 'utf-8')

name = str(datetime.date.today())

with open("/home/www/push/"+name+".png","rb")as f:
    # 设置附件的MIME和文件名，这里是png类型:
    mime = MIMEBase('image', 'png', filename=name+'.png')
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename=name+'.png')
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
    msg['From'] = _user
    msg['To'] = ", ".join(recipients)
    #s.sendmail(_user, _to, msg.as_string())
    msg['Cc'] = ", ".join(bcc)
    receive = recipients
    receive.extend(bcc)
    s.sendmail(_user, receive, msg.as_string())
    s.quit()
    logger.info('success')
except smtplib.SMTPException,e:
    logger.exception("Exception Logged")