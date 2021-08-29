from genericpath import exists
import os
import re
import requests
import email
from fetchmails import fetch_mails, get_header, get_files, get_contents


def filepath(path, fn, root=""):
    p = os.path.join(path, fn)
    if not p.startswith(root):
        fn = os.path.basename(fn)
        p = os.path.join(path, fn)
    n = 1
    while os.path.exists(p):
        p = os.path.join(path, fn+"(%s)" % n)
        n += 1
    os.makedirs(path, exist_ok=True)
    return p


def trywget(url, path, fn):
    try:
        m = re.match(
            "(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", url.strip())
        if m:
            url = m.group()
            return wget(url, path, fn)
    except Exception as e:
        print(e)
    return False


def wget(url, path, fn):
    res = requests.get(url)
    fn = fn if fn else os.path.basename(url)
    filename = filepath(path, fn)
    print("- URL Found: %s." % url, 'Save it to', filename)
    with open(filename, "wb") as f:
        f.write(res.content)
    return True


def savetofile(data, filename, path, fn):
    fn = fn if fn else filename
    fn = filepath(path, fn)
    f = open(fn, 'wb')
    f.write(data)
    f.close()
    print("- Attachment File Found: %s." % filename, 'Save it to', fn)


def fetch_books(downloaddir="download", **kargs):
    for msg_data in fetch_mails(**kargs):
        msg = email.message_from_bytes(msg_data[0][1])
        header = get_header(msg)
        print("*"*20)
        print(
            "\n".join((a+b for a, b in zip(['* From: ', '* To: ', '* Subject: '], header))))
        print("*"*20)
        subject = header[-1]
        filenames = [""]
        if subject.startswith("filename:"):
            filenames = subject.split(":")[1]
            filenames = [f.strip() for f in filenames.split(",")]
        nf = 0
        maxn = len(filenames) - 1
        if trywget(header[-1], downloaddir, "" if nf > maxn else filenames[nf]):
            nf += 1
        for tp, content in get_contents(msg):
            lines = content.split("\n")
            for l in lines:
                if trywget(l, downloaddir, "" if nf > maxn else filenames[nf]):
                    nf += 1
        for filename, data in get_files(msg):
            fn = "" if nf > maxn else filenames[nf]
            savetofile(data, filename, downloaddir, fn)
            nf += 1
