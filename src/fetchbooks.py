import os
import re
import requests
import email
from fetchmails import fetch_mails, get_header, get_files, get_contents
import shutil

Root = ""
def filepath(path, fn):
    p = os.path.join(path, fn)
    if not p.startswith(Root):
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
    return ""


def wget(url, path, fn):
    chunk_size = 1024*1024
    res = requests.get(url, stream=True)
    fn = fn if fn else os.path.basename(url)
    filename = filepath(path, fn)
    print("- URL Found: %s." % url, 'Save it to', filename)
    with open(filename, "wb") as f:
        for chunk in res.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
    return filename


def savetofile(data, filename, path, fn):
    fn = fn if fn else filename
    fn = filepath(path, fn)
    f = open(fn, 'wb')
    f.write(data)
    f.close()
    print("- Attachment File Found: %s." % filename, 'Save it to', fn)
    return fn

def try_unpack(fn):
    if os.path.splitext(fn)[1][1:] in [f[0] for f in shutil.get_archive_formats()]:
        try:
            shutil.unpack_archive(fn, os.path.dirname(fn))
            print("Unpack", fn)
        except Exception as e:
            print(e)
    return fn

def fetch_books(downloaddir="download", root="", **kargs):
    global Root
    Root = root
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
        if try_unpack(trywget(header[-1], downloaddir, "" if nf > maxn else filenames[nf])):
            nf += 1
        for tp, content in get_contents(msg):
            lines = content.split()
            for l in lines:
                if try_unpack(trywget(l, downloaddir, "" if nf > maxn else filenames[nf])):
                    nf += 1
        for filename, data in get_files(msg):
            fn = "" if nf > maxn else filenames[nf]
            try_unpack(savetofile(data, filename, downloaddir, fn))
            nf += 1
