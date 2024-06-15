# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 19:29:34 2020

@author: kiran
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from variables import reports_path
from datetime import date
from loghandler import logger
import smtplib
import imaplib
import email
import sys
import os

class mailing:

    from nse_stock_load.variables import mail_path

    email_user='kirakira5593@gmail.com'
    email_pass='kirakira5593'
    send_subject="Stock Symbol Not found in Database"
    send_body="New Stock Symbol added in NSE & not found in Database. Insert the respective new company name"

    def send_mail(self,mail_from=email_user,mail_to=email_user,path=mail_path,files=["NSE_New_Symbol.csv"],subject=send_subject,body=send_body,file_type='text',file_format='octet-stream'):

        if 'str' in str(type(mail_to)):
            mail_to=[mail_to]
        if 'str' in str(type(files)):
            files=[files]

        mail = smtplib.SMTP_SSL(host="smtp.gmail.com",port=465)
        mail.login(self.email_user,self.email_pass)

        msg=MIMEMultipart()                                             # multi part indicates mail contains mutiple part i.e., body,subject,attachments
        msg['subject']=subject                                          # mail subject
        msg.attach(MIMEText(body+"\n"))                                 # attach the body (text format)

        if files != None:                                               # check if there are any input files to attach, if yes then attach

                for f in files:

                    if os.path.isfile(path+f):
                        attachment=MIMEBase(file_type,file_format)       # type of attachment
                        attachment.set_charset('utf-16')
                        attachment.set_payload(open(path+f,'rb').read())        # read upload file
                        #encoders.encode_base64(attachment)
                        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(path+f))        # upload filename
                        msg.attach(attachment)                                  # attach
                    else:
                        msg.attach(MIMEText("\n"+path+f+" file doesnot exist\n"))

        msg['To'] = ','.join(mail_to)

        mail.sendmail(mail_from,mail_to,msg=msg.as_string())      # send mail
        logger.INFO("\nmail sent to "+str(mail_to))

        mail.close()                                                    # close connection

    def read_mail(self,email_user=email_user,email_pass=email_pass,path=mail_path,what="Subject",where="Inbox",search="Start",download_attach="Yes",download_body="No",latestonly="YES",download_check="YES",file_check="",unread_mails_only="YES"):

        mail = imaplib.IMAP4_SSL(host="imap.gmail.com",port=993)
        mail.login(email_user,email_pass)
        #print(mail.list())
        mail.select(where)

        if unread_mails_only == "YES":
            ty,msg=mail.search(None,what,search, '(UNSEEN)')                            # search and get mail number
        else:
            ty,msg=mail.search(None,what,search)                                        # search and get mail number

        if latestonly=="YES":
            try:
                msg=[msg[0].split()[-1]]                                    # take the latest mail for given criteria (where,what and search)
            except IndexError:
                sys.exit("No mails exist with given conditions")

        for num in msg[0].split():                                      # get the mail message in raw format from mail number
            typ, data = mail.fetch(num,'(RFC822)' )
            raw_email = data[0][1]
            email_message=email.message_from_bytes(raw_email)           # Convert byte format data to text

        if download_attach.upper()=="YES":                              # Check if download of files is requrired

            for part in email_message.walk():
                if part.get('X-Attachment-Id') is not None:             # search for attachments
                    open(self.mail_path+part.get_filename(),'wb').write(part.get_payload(decode=True))

        if download_body.upper()=="YES":                                # Check if body of mail need to be read

            for part in email_message.walk():
                if part.get_content_type() != 'text/plain':             # check of plain text i.e., mail body and return it as output
                    body=part.strip('\n')
                    return body

        if download_check.upper()=="YES":

            if os.path.isfile(self.mail_path+file_check):
                logger.INFO("\nsuccesfully download attachment to "+self.mail_path+file_check)
            else:
                logger.INFO("\n"+self.mail_path+file_check+" is not in mail attachments")

        mail.close()                                                    # close connection
        
if "__name__" == "__main__":
    
    logger.INFO("Seding any reports if present")
    
    archival_file=["reports_archive_"+date.today().strftime("%Y%m%d")+".zip"]
    report_body="Loading completed for today, Attached the daily reports"
    report_subject="Adhoc Mail for existing reports"
    
    try:
        
        mailing.send_mail(files=archival_file,path=reports_path,body=report_body,subject=report_subject,mail_to=["swathikirannanduri@gmail.com"])
        
    except:
        logger.INFO("No report files present to mail")