import smtplib
from email.message import EmailMessage


def sendEmail(Reciver, Content):
  args = open('bot_mail.txt','r').read().split()
  FROM = args[0]
  PASSWORD = args[1]
  HOST = args[2]
  msg = EmailMessage()
  msg.set_content(Content)
  msg['Subject'] = "A Keyword has been found!"
  msg['From'] = FROM
  msg['To'] = Reciver
  s = smtplib.SMTP(host=HOST, port=587)
  s.starttls()
  s.login(FROM, PASSWORD)
  s.send_message(msg)
  s.quit()


def prepareContent(keyword, threadNo):
  content = "Keyword " + str(keyword) + " has been found!\n"
  content += "https://boards.4channel.org/biz/thread/" + str(threadNo)
  return content
  
def sendEmailToEveryone(emaillist, Content):
  for email in emaillist:
    sendEmail(email,Content)
