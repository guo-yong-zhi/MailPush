import imaplib
import datetime
from email.header import decode_header
from email.utils import parseaddr


def fetch_mails(host,
                user,
                password,
                mailbox='INBOX',
                criteria=('UNSEEN',),
                days=7,
                maxnum=10
                ):

    if isinstance(criteria, str):
        criteria = [] if criteria.strip() == "" else [criteria]
    days = int(days)
    maxnum = int(maxnum)
    connection = imaplib.IMAP4_SSL(host)
    connection.login(user, password)
    typ, data = connection.select(mailbox)
    num_msgs = int(data[0])
    print('{}, There are {} emails in {}'.format(typ, num_msgs, mailbox))
    sincedate = (datetime.date.today() -
                 datetime.timedelta(days)).strftime("%d-%b-%Y")
    typ, data = connection.search(None, 'SINCE', sincedate, *criteria)
    ids = data[0].split()
    print("{}, There are {} {} emails in the past {} days".format(
        typ, len(ids), " ".join(criteria), days))
    if len(ids) > maxnum:
        print("keep", maxnum, 'emails')
        ids = ids[-maxnum:]
    for i in ids:
        typ, msg_data = connection.fetch(i, '(RFC822)')
        yield msg_data

# https://www.jianshu.com/p/544a35bc8c92
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def get_header(msg):
    H = []
    for header in ['From', 'To', 'Subject']:
        value = msg.get(header, '')
        if value:
            # 文章的标题有专门的处理方法
            if header == 'Subject':
                value = decode_str(value)
            elif header in ['From', 'To']:
                # 地址也有专门的处理方法
                hdr, addr = parseaddr(value)
                value = decode_str(addr)
        H.append(value)
    return H

# 邮件正文部分
# 取附件
# 邮件的正文部分在生成器中，msg.walk()
# 如果存在附件，则可以通过.get_filename()的方式获取文件名称
def get_files(msg):
    for part in msg.walk():
        filename = part.get_filename()
        if filename != None:  # 如果存在附件
            filename = decode_str(filename)  # 获取的文件是乱码名称，通过之前定义的函数解码
            data = part.get_payload(decode=True)  # 取出文件正文内容
            yield filename, data


# 接下来取正文信息
# 获取邮件的字符编码，首先在message中寻找编码，如果没有，就在header的Content-Type中寻找
def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos+8:].strip()
    return charset

def get_contents(msg):
    for part in msg.walk():
        content_type = part.get_content_type()
        charset = guess_charset(part)
        # 如果有附件，则直接跳过
        if part.get_filename() != None:
            continue
        email_content_type = ''
        content = ''
        if content_type == 'text/plain':
            email_content_type = 'text'
        elif content_type == 'text/html':
            print('skip HTML-formatted content')
            continue  # 不要html格式的邮件
            email_content_type = 'html'
        if charset:
            try:
                content = part.get_payload(decode=True).decode(charset)
            # 这里遇到了几种由广告等不满足需求的邮件遇到的错误，直接跳过了
            except AttributeError:
                print('type error')
            except LookupError:
                print("unknown encoding: utf-8")
        if email_content_type == '':
            continue
            # 如果内容为空，也跳过
        # 邮件的正文内容就在content中
        yield (email_content_type, content)
