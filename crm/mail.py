import email
import imaplib
import smtplib
import datetime
import email.mime.multipart
import base64

imap_server = "outlook.office365.com"
imap_port = 993
smtp_server = "smtp.office365.com"
smtp_port = 587

class Outlook():
    def __init__(self):
        mydate = datetime.datetime.now()-datetime.timedelta(1)
        self.today = mydate.strftime("%d-%b-%Y")
        # self.imap = imaplib.IMAP4_SSL('imap-mail.outlook.com')
        # self.smtp = smtplib.SMTP('smtp-mail.outlook.com')

    def login(self, username, password):
        self.username = username
        self.password = password
        while True:
            try:
                self.imap = imaplib.IMAP4_SSL(imap_server,imap_port)
                r, d = self.imap.login(username, password)
                assert r == 'OK', 'login failed'
                print(" > Sign as ", d)
            except:
                print(" > Sign In ...")
                continue
            # self.imap.logout()
            break
            
    def sendEmail(self, recipient, subject, message):
        headers = "\r\n".join([
            "from: " + self.username,
            "subject: " + subject,
            "to: " + recipient,
            "mime-version: 1.0",
            "content-type: text/html"
        ])
        content = headers + "\r\n\r\n" + message
        while True:
            try:
                self.smtp = smtplib.SMTP(smtp_server, smtp_port)
                self.smtp.ehlo()
                self.smtp.starttls()
                self.smtp.login(self.username, self.password)
                self.smtp.sendmail(self.username, recipient, content)
                print("   email replied")
            except:
                print("   Sending email...")
                continue
            break


if __name__ == "__main__":
    mail_pass = input('passma: ')
    sender = "bingo163@outlook.com"
    receivers = ['2314723148@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱 #可群发
    mail = Outlook()
    mail.login(sender, mail_pass)
    mail.sendEmail('2314723148@qq.com','subject','message body')
