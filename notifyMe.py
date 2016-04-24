#!/userdisk/python/bin/python
# -*- coding:utf-8 -*- 
# fileName : notifyMe.py
# auth : fangchao
# version : 0.0421
import sys,cookielib,urllib2,urllib,json,smtplib
from email.mime.text import MIMEText
from email.header import Header
reload(sys)
sys.setdefaultencoding('utf-8')
def scrapyOa():
	#url
	auth_url="http://oa.tydic.com/ubp_Login_login.action"
	host_url="http://oa.tydic.com/workflow_pending.ProcPending_findPendingList.action"
	#postdata 修改用户名和密码
	data={"user.indexLayout":"","userInfo":"","user.userCode":"","user.password":""}
	post_data=urllib.urlencode(data)
	#headers "Content-Length":"72",
	headers={
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Encoding":"gzip, deflate",
		"Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
		"Cache-Control":"max-age=0",
		"Connection":"keep-alive",
		"Content-Type":"application/x-www-form-urlencoded",
		"Host":"oa.tydic.com",
		"Origin":"http://oa.tydic.com",
		"Referer":"http://oa.tydic.com/login.jsp",
		"Upgrade-Insecure-Requests":"1",
		"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
	}
	#cookie
	cj=cookielib.CookieJar()
	opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	req=urllib2.Request(auth_url,post_data,headers)
	result = opener.open(req)
	result = opener.open(host_url)
	content=result.read()
	jsonObj=json.loads(content)
	nstr=[]
	if jsonObj["Total"]==0:
	 	pass
	else:
		for i in range(0,jsonObj["Total"]):
			nstr.append(jsonObj["Rows"][i]["nodeName"]+"    "+jsonObj["Rows"][i]["pendingDesc"])
	return nstr
def sendNotify(t,h):
	#mail 修改发送邮箱相关配置
	sender=""
	receivers = ['']
	mail_host=""
	mail_user="" 
	mail_pass=""
	mail_content = "<html><body><table>" 
	for s in t:
		mail_content=mail_content+"<tr>"+s+"</tr>"
	mail_content=mail_content+"</table></body></html>"
	message = MIMEText(mail_content, 'html', 'utf-8')
	message['From'] = Header(sender, 'utf-8')
	message['To'] =  Header(receivers[0], 'utf-8')
	message['Subject'] = Header(h, 'utf-8')
	try:
	    #smtpObj = smtplib.SMTP_SSL()
	    smtpObj = smtplib.SMTP() 
	    smtpObj.set_debuglevel(1)
	    smtpObj.connect(mail_host)
	    smtpObj.ehlo(mail_host)
	    smtpObj.login(mail_user,mail_pass)  
	    smtpObj.sendmail(sender, receivers, message.as_string())
	    print "邮件发送成功"
	except smtplib.SMTPException:
		print "Error: 无法发送邮件"

def main():
	text=scrapyOa()
	if len(text)==0 :
		print "暂无待办"
		pass
	else:
		sendNotify(text,"OA待办提醒")
if __name__ == '__main__':
	main()






