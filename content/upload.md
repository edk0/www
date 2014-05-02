Title: file upload via SSH
Date: 2013-04-29 02:56
Tags: ssh, python
Category: python
Slug: ssh-upload
Summary: ssh

The other day someone mentioned to me that they set something up so they could
upload files by piping data into ssh:

    :::console
    $ cat foo | ssh upload@server
    http://server/wkFP.txt

which seemed like a fun thing to copy. Implementing it is simple enough: you add
an `upload` account on the server, and add an `authorized_keys` entry that looks
like this:

    :::text
    command="/home/upload/bin/upload.py",no-agent-forwarding,no-port-forwarding,no-pty,no-user-rc,no-X11-forwarding ssh-rsa AA…==

`upload.py` is a fairly simply python program that reads stdin and saves it in
a publicly accessible directory. Here's the only hard-ish part: guessing the
file extension of the thing we're uploading. It was determined largely by trial
and error, so more override entries will probably be necessary. Unfortunately,
[mimetypes](http://docs.python.org/2/library/mimetypes.html) doesn't appear to
have a "guess a sensible extension" method; it just picks the first one it
finds that maps to the correct type.

`magic` is [python-magic](https://pypi.python.org/pypi/python-magic/).

    :::python
    import magic
    import mimetypes

    SHEBANG_OVERRIDE = {
        'python': '.py',
        'python2.7': '.py',
    }

    MIME_OVERRIDE = {
        'text/plain': '.txt',
        'image/jpeg': '.jpg',
    }

    def guess_ext(buffer_):
        if buffer_.startswith('#!'):
            shebang = [
                path.basename(s) for s in buffer_[2:buffer_.find('\n')].strip().split(' ')
                if not s.startswith('-')][-1]
        else:
            shebang = False
        ft = magic.from_buffer(buffer_, mime=True)
        return SHEBANG_OVERRIDE.get(shebang, None) or \
            MIME_OVERRIDE.get(ft, None) or \
            mimetypes.guess_extension(ft) or \
            '.txt'

Worthy of note is the fact that when you force a command this way and the client
requests a different command, the requested command will go in the
`SSH_ORIGINAL_COMMAND` environment variable. I used it to implement a `usage`
command that tells me how much space my uploaded files take up:

    :::console
    $ ssh upload@server usage
    105M

Unlike other file hosting services you might use, there's no reason you should
wait for the upload to complete before getting your URL back. Once you have
enough of the file to guess the extension you can return the filename
immediately:

    :::python
    def upload():
        # read the first 1K
        buffer_ = stdin.read(1024)
        # check for empty input
        if buffer_.strip() == '':
            print "empty file, not uploading it."
            return
        # guess file extension
        ext = guess_ext(buffer_)
        # actually write
        with get_unique(ext) as f:
            f.write(buffer_)
            print FILE_URL.format(filename=path.basename(f.name))
            # read the rest of the file
            while buffer_:
                buffer_ = stdin.read(1024)
                f.write(buffer_)

Here's a working implementation of the whole thing. Its only external
dependency is [python-magic](https://pypi.python.org/pypi/python-magic/).
`DATA_DIR` needs to point to a directory your upload user can write to, and
`FILE_URL` is probably wrong.

    #!/usr/bin/python -u
    import magic
    import mimetypes
    import os
    import os.path as path
    import random
    import string
    import subprocess
    from sys import stdin

    FN_LEN = 4
    DATA_DIR = "data"
    FILE_URL = "http://my.server/{filename}"

    ALPHABET = string.lowercase + string.uppercase + string.digits

    SHEBANG_OVERRIDE = {
        'python': '.py',
        'python2.7': '.py',
    }

    MIME_OVERRIDE = {
        'text/plain': '.txt',
        'image/jpeg': '.jpg',
    }


    def guess_ext(buffer_):
        if buffer_.startswith('#!'):
            shebang = [
                path.basename(s) for s in buffer_[2:buffer_.find('\n')].strip().split(' ')
                if not s.startswith('-')][-1]
        else:
            shebang = False
        ft = magic.from_buffer(buffer_, mime=True)
        return SHEBANG_OVERRIDE.get(shebang, None) or \
            MIME_OVERRIDE.get(ft, None) or \
            mimetypes.guess_extension(ft) or \
            '.txt'


    def get_unique(ext, len_=FN_LEN):
        random.seed()
        tries = 0
        while True:
            fn = path.join(DATA_DIR, ''.join(random.choice(ALPHABET) for n in range(len_)) + ext)
            try:
                f = open(fn, 'w')
                return f
            except:
                tries += 1
                if tries > 20:
                    len_ += 1
                    tries = 0
                continue


    def upload():
        # read the first 1K
        buffer_ = stdin.read(1024)
        # check for empty input
        if buffer_.strip() == '':
            print "empty file, not uploading it."
            return
        # guess file extension
        ext = guess_ext(buffer_)
        # actually write
        with get_unique(ext) as f:
            f.write(buffer_)
            print FILE_URL.format(filename=path.basename(f.name))
            # read the rest of the file
            while buffer_:
                buffer_ = stdin.read(1024)
                f.write(buffer_)


    def usage():
        u = subprocess.check_output(["du", "-h", DATA_DIR])
        print "{}".format(u.strip().split()[0])


    def main():
        commands = {
            "upload": upload,
            "usage": usage,
        }
        if "SSH_ORIGINAL_COMMAND" in os.environ:
            cmd = commands.get(os.environ["SSH_ORIGINAL_COMMAND"], None)
            if cmd:
                cmd()
            else:
                print "Unknown command: {}".format(os.environ["SSH_ORIGINAL_COMMAND"])
        else:
            upload()


    if __name__ == '__main__':
        main()
