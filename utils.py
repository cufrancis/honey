import json
from session import email_verified, reset_password
from email.header import Header
from email.mime.text import MIMEText


def body_decode(string):
    """
    解析body_arguments 到json
    """
    if isinstance(string, bytes):
        string = bytes.decode(string)

    if isinstance(string, str):
        # "".join(string.split())
        data = json.loads(string)
    return data

def json_convert(o):
    if isinstance(o, ObjectId):
        return str(o)
    if isinstance(o, datetime.datetime):
        return o.__str__()

class Email(object):

    def send_email(self, content, subject='text', to_addr=''):
        # send email primarily
        from_addr = '18551826351@163.com'
        password = '041000lxjwff'

        smtp_server = 'smtp.163.com'

        msg = MIMEText(content, 'html', 'utf-8')
        msg['From'] = from_addr
        msg['Subject'] = Header(subject, 'utf8').encode()
        msg['To'] = to_addr

        import smtplib

        try:
            server = smtplib.SMTP(smtp_server, 25)
            server.set_debuglevel(1)
            server.login(from_addr, password)
            server.sendmail(from_addr, [to_addr], msg.as_string())
            server.quit()
            return True
        except Exception:
            return False

class VerifiedEmail(Email):
    def __init__(self):
        self.email_verified = email_verified()

    def send(self, data):

        code = self.generate_code(data)
        content = '<h2 style="margin:20px 0;font-size:16px;font-weight:normal">Hi, {username}</h2> \
                    <p style="line-height:1.5"> \
                        您需要验证应用 {appname} 里的账号邮箱地址 {email} <br /> \
                        请点击下列链接进行确认:<br/> \
                        <a href="{link}" style="color:#2375ac" target="_blank">{link}</a> \
                    </p>'.format(username=data.get('username', 'Null'),appname='honey',email=data.get('email'), link = code)

        return self.send_email(content, subject="验证{appname}的账号邮箱".format(appname='honey'), to_addr=data.get('email'))

    def generate_code(self, data):
        return self.email_verified.create(data)

class emailResetPassword(Email):

    def __init__(self):
        self.reset_password = reset_password()

    def send(self, data):
        code = self.generate_code(data)
        # print(code)
        # return
        content = '<h2 style="margin:20px 0;font-size:16px;font-weight:normal">Hi, {username}</h2> \
                    <p style="line-height:1.5"> \
                        您请求重设应用 {appname} 的密码.<br /> \
                        点击下列链接来重设您的账号密码: <br /> \
                        <a href="{link}" style="color:#2375ac" target="_blank">{link}</a> \
                        链接在 24 小时内有效. \
                    </p>'.format(username=data.get('username'), appname='honey', link=code)

        return self.send_email(content, subject="重设{username}的密码".format(username=data.get('username', '')), to_addr=data.get('email'))

    def generate_code(self, data):
        return self.reset_password.create(data)
