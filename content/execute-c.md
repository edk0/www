Title: execute C
Date: 2013-12-23 13:48
Tags: c, sh
Category: c
Slug: execute-c
Summary: ...

Just a quick one, here's a thing I did recently to execute C source
files as scripts. You put this at the top of them:

```sh
#!/bin/sh
F=`mktemp`&&tail -n+3 $0>$F&&gcc -xc -o$F $F&&exec $F "$@"
```

and `chmod +x blah.c`.
