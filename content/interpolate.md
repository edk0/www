Title: string interpolation
Date: 2013-05-31 02:52
Tags: python
Category: python
Slug: interpolate
Summary: ...

I wrote a thing for doing string interpolation in Python, like
`"Hello, {foo}!".format(foo="World")`, except that fields are taken from the calling
scope rather than being explicitly supplied.

Using it is simple:
```pycon
>>> from interpolate import i
>>> foo = "bar"
>>> bar = 123
>>> print i % "{foo} {bar:09}"
bar 000000123
```

The "field name" can be an expression:
```pycon
>>> foo = 5
>>> bar = 8
>>> i % "{foo + bar}"
'13'
```

Compiler flags are preserved:
```pycon
>>> foo = 8
>>> bar = 5
>>> i % "{foo/bar}"
'1'
>>> from __future__ import division
>>> i % "{foo/bar}"
'1.6'
```

It works for functions too (integer keys like `{0}` are positional arguments):
```pycon
>>> def f(a, b):
...     print i % "{a}, {1}!"
... 
>>> f("Hello", "world")
Hello, world!
```

And it *sort of* works for closed-over variables. This works:
```pycon
>>> def foo(bar):
...     def fubar():
...         frobnicate(bar)
...         print i % "frobnicated {bar}"
...     return fubar
... 
>>> foo(12345)()
frobnicated 12345
```

but it only works as long as the variable name `bar` appears somewhere in `fubar`,
or Python won't know to close over `bar`. Apart from that (do you often
interpolate closed-over variables you don't otherwise use?) it's pretty much
like real string interpolation.

<strike>It's [here](/static/interpolate.py) if you want to download it.</strike>
[`pip install interpolate`](https://pypi.python.org/pypi/interpolate)
