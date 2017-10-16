import smtplib
from email import encoders
from email import utils
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText
from django.conf import settings
import pdb
import re

class Email(object):
    EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')

 
        
class EmailEx(Email):
    def send_text_email(self,Subject,content,receiver):
        
        if settings.EMAIL_SWITCH:
            sender              = settings.SMTP_SERVER_USER
            themsg              = MIMEMultipart()
            themsg['Subject']   = Subject
            themsg['To']        = receiver
            themsg['From']      = settings.PROJECTNAME
            themsg['Date']      = utils.formatdate(localtime = 1)
            themsg['Message-ID'] = utils.make_msgid()
            msgAlternative      = MIMEMultipart('alternative')
            themsg.attach(msgAlternative)
            content = content + '<br/>www.map2family.com'
            msgText = MIMEText(content,'html', 'utf-8')
            msgAlternative.attach(msgText)
            themsgtest = themsg.as_string()      
            # send the message
            server = smtplib.SMTP()  
            
            server.connect(settings.SMTP_SERVER) 
            
            server.login(settings.SMTP_SERVER_USER, settings.SMTP_SERVER_PWD)
            server.sendmail(sender, receiver, themsgtest)
            
            server.quit()#SMTP.quit()
   
    @staticmethod        
    def send_html_email( Subject,content,receiver):
        if settings.EMAIL_SWITCH:  
            sender              = settings.SMTP_SERVER_USER
            themsg              = MIMEMultipart()
            themsg['Subject']   = Subject
            if isinstance(receiver, list):
                themsg['To']        = ', '.join(receiver)
            else:
                themsg['To']        = receiver
                
            themsg['From']      = settings.PROJECTNAME
            themsg['Date']      = utils.formatdate(localtime = 1)
            themsg['Message-ID'] = utils.make_msgid()
            msgAlternative      = MIMEMultipart('alternative')
            themsg.attach(msgAlternative) 
            msgText = MIMEText(content,'html', 'utf-8')
            msgAlternative.attach(msgText)
            themsgtest = themsg.as_string()     
            # send the message
            server = smtplib.SMTP()  
            server.connect(settings.SMTP_SERVER) 
            server.login(settings.SMTP_SERVER_USER, settings.SMTP_SERVER_PWD)
            server.sendmail(sender, receiver, themsgtest)
            server.quit()#SMTP.quit()