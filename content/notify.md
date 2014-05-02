Title: i3 notify
Date: 2013-04-28 23:19
Tags: i3, python
Category: python
Slug: i3-notify
Summary: notify

I've been using [i3](http://i3wm.org) and I wanted a notification thing for
it, so I made one. It's not very beautiful, but it does the job: you run a
shell command

    :::console
    $ scripts/notify.py -c red -l 15 this is a notification

and something like this appears in i3bar:

![this is a notification](http://glin.es/sVFN.png "this is a notification")

External dependencies are [py3status](https://github.com/ultrabug/py3status),
[clize](https://github.com/epsy/clize) and
[webcolors](https://pypi.python.org/pypi/webcolors/1.3).

py3status plugin:

    #!python
    import json
    import os
    import os.path as path
    from time import time

    plugin = None


    class Plugin:
        NOTIFY_PATH = "~/.i3/notify/notify"

        buf = ""

        def __init__(self, config):
            self.config = config
            self.NOTIFY_PATH = path.expanduser(self.NOTIFY_PATH)

            if not path.exists(path.dirname(self.NOTIFY_PATH)):
                os.makedirs(path.dirname(self.NOTIFY_PATH))
            if not path.exists(self.NOTIFY_PATH):
                os.mkfifo(self.NOTIFY_PATH)
            fifofd = os.open(self.NOTIFY_PATH, os.O_ASYNC | os.O_NONBLOCK | os.O_RDONLY)
            self.fifo = os.fdopen(fifofd)
            self.notification = {'deathtime': 0}

        def kill(self):
            self.fifo.close()

        def props(self, d, *a):
            return (str(d[k]) if isinstance(d[k], unicode) else d[k] for k in a)

        def get_notification(self):
            self.buf += self.fifo.read()
            if '\n' in self.buf:
                notif, self.buf = self.buf.split('\n', 1)
                notif = json.loads(notif)
                notif['deathtime'] = time() + notif.get('lifetime', 20)
                self.notification = notif
                return self.props(self.notification, 'text', 'color')
            elif time() <= self.notification['deathtime']:
                return self.props(self.notification, 'text', 'color')
            else:
                return '', None

        def get_text(self):
            text, color = self.get_notification()
            return {
                'cached_until': time(),  # never cache.
                'full_text': text,
                'color': color,
                'name': 'notify'
            }


    class Py3status:
        def notify(self, json, i3status_config):
            global plugin
            if plugin is None:
                plugin = Plugin(i3status_config)
            response = plugin.get_text()
            return (0, response)

executable script:

    #!/usr/bin/python
    from clize import run, clize
    import json
    import os.path as path
    import sys
    import webcolors

    NOTIFY_PATH = "~/.i3/notify/notify"


    @clize(alias={'color': ('c',), 'ttl': ('l',)})
    def main(color='FFFFFF', ttl=20, *text):
        try:
            color = webcolors.name_to_hex(color)
        except:
            color = '#' + color.strip('#')
        obj = {
            'color': color.upper(),
            'lifetime': ttl
        }
        inp = '' if sys.stdin.isatty() else sys.stdin.read()
        if not text:
            notify = inp
        else:
            notify = ' '.join(text)
            if '{}' in notify:
                notify = notify.format(inp)
        obj['text'] = notify
        with open(path.expanduser(NOTIFY_PATH), 'a') as f:
            f.write("{}\n".format(json.dumps(obj)))
        sys.stdout.write(inp)

    if __name__ == '__main__':
        run(main)
