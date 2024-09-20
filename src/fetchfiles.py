import os
import re
import requests
import email
import shutil
import datetime
from fetchmails import fetch_mails, get_header, get_files, get_contents

Root = ""
def filepath_(fn, path=""):
    p = os.path.join(path, fn)
    if not os.path.abspath(p).startswith(os.path.abspath(Root)):
        print(p, "is out of", Root)
        p = os.path.join(Root, os.path.basename(fn))
    n = 1
    p0 = p
    while os.path.exists(p):
        if os.path.isfile(p):
            bn, ext = os.path.splitext(p0)
        else:
            bn, ext = p0, ""
        p = "%s(%s)%s"%(bn, n, ext)
        n += 1
    p = re.sub(r"[:<>|?*]", "_", p.replace("\\", "/"))
    dn = os.path.dirname(p)
    if dn:
        os.makedirs(dn, exist_ok=True)
    return p

def get_valid_filename(fn):
    d,b = os.path.split(fn)
    return os.path.join(d, re.sub(r"[^-\w.]", "", b.strip().replace(" ", "_")))

def filepath(fn, path=""):
    p1 = None
    e = None
    valid_fn = get_valid_filename(fn)
    P = [(fn, path), (valid_fn, path), (valid_fn, Root), ("mailpush_saved_file", Root)]
    for f_p in P:
        try:
            if e:
                print(e)
            p2 = filepath_(*f_p)
            if p1:
                print(p1, "is illegal. Try filename:", p2)
            p1 = p2
            open(p1, 'wb').close()
            return p1
        except Exception as e_:
            e = e_
            pass
    if e:
        print(e)
        raise e
    raise Exception

def trywget(url, path, fn):
    try:
        m = re.match(
            "(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", url.strip())
        if m:
            url = m.group()
            res = requests.get(url, stream=True)
        else:
            return ""
    except Exception as e:
        print(e)
        return ""
    chunk_size = 1024*1024
    fn = fn.strip()
    if fn == "" or fn.endswith("/") or fn.endswith("\\"):
        fn = os.path.join(fn, os.path.basename(url))
    filename = filepath(fn, path)
    print("- URL Found: %s." % url, 'Save it to', filename)
    with open(filename, "wb") as f:
        for chunk in res.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
    return filename


def savetofile(data, filename, path, fn):
    fn = fn.strip()
    if fn == "" or fn.endswith("/") or fn.endswith("\\"):
        fn = os.path.join(fn, filename)
    fn = filepath(fn, path)
    f = open(fn, 'wb')
    f.write(data)
    f.close()
    print("- Attachment File Found: %s." % filename, 'Save it to', fn)
    return fn


def try_unpack(fn):
    if os.path.splitext(fn)[1][1:] in [f[0] for f in shutil.get_archive_formats()]:
        try:
            dst = filepath(os.path.splitext(fn)[0])
            shutil.unpack_archive(fn, dst)
            print("Unpack", fn, "to", dst)
            os.remove(fn)
            fn = dst
        except Exception as e:
            print(e)
    return fn


def try_append_filenames(filenames, line):
    line = line.strip()
    if line.startswith("saveto"):
        ts = filter(None, re.split('[|<>]', line[7:]))
        filenames.extend(t.strip() for t in ts if t)


def fetch_files(downloaddir="download", root="", **kargs):
    global Root
    Root = root
    files = []
    for msg_data in fetch_mails(**kargs):
        print("\n**", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"**")
        msg = email.message_from_bytes(msg_data[0][1])
        del msg_data
        header = get_header(msg)
        print("*"*25)
        print(
            "\n".join((a+str(b) for a, b in zip(['* From: ', '* To: ', '* Subject: '], header))))
        print("*"*25)
        subject = str(header[-1])
        filenames = []
        try_append_filenames(filenames, subject)
        nf = 0
        file = try_unpack(trywget(subject, downloaddir, filenames[nf] if nf < len(filenames) else ""))
        if file:
            files.append(file)
            nf += 1
        for tp, content in get_contents(msg):
            lines = content.splitlines()
            for l in lines:
                try_append_filenames(filenames, l)
            for l in lines:
                for ll in filter(None, re.split("[<>\s|]", l)):
                    file = try_unpack(trywget(ll, downloaddir, filenames[nf] if nf < len(filenames) else ""))
                    if file:
                        files.append(file)
                        nf += 1
                    else:
                        break
        for filename, data in get_files(msg):
            fn = filenames[nf] if nf < len(filenames) else ""
            file = try_unpack(savetofile(data, filename, downloaddir, fn))
            files.append(file)
            nf += 1
    return files
