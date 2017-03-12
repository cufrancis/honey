import json
from session import email_verified
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

    def send():
        pass
    pass

class VerifiedEmail(Email):
    def __init__(self):
        self.emailVerified = email_verified()

    def send(self, data):
        code = self.generate_code(data)

        # send email primarily
        from_addr = '18551826351@163.com'
        password = '041000lxjwff'

        to_addr = data.get('email')
        smtp_server = 'smtp.163.com'

        content = "welcome to register honey shop! \n please verify you email, this is code: \n<b><center>{code}</center><b> \n click it or  copy that.Thank You!".format(code=code)

        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = from_addr
        msg['Subject'] = Header('text', 'utf8').encode()
        msg['To'] = to_addr

        import smtplib

        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()

        return True

    def generate_code(self, data):
        return self.emailVerified.create(data)
