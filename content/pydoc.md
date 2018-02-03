Title: search keyword-ing
Date: 2018-01-31T20:31Z
Tags: python
Category: python
Slug: search-keywords
Summary: ...

I was recently writing some Python. That happens a lot, but it's been a while,
and I was looking at the Python documentation quite a bit. I realised that the
way I normally do this is to type some of `docs.python.org` into Firefox until
a likely URL appears, select it, and then manually change the URL to what I
guess it should be.

For whatever reason, today was the day I got tired of doing that, and I
decided that today was the day I was going to add a [keyword bookmark][1] that
just did the right thing—like the following easy ones everyone should have:

```
wp:  https://en.wikipedia.org/wiki/%s
wk:  https://en.wiktionary.org/wiki/%s
rfc: https://tools.ietf.org/html/%s
```

Only with Python it's not so easy, as far as I know. The only search function
on [the python docs][2] is a javascript-based full-text search, which is
already horrible, and as far as I know there's no straightforward way to make
it redirect.

I decided instead to try to use [intersphinx][3], which pretty reliably solves
the exact problem I want to, but for writing documentation. You refer to some
object by name, and intersphinx finds and links to the documentation for it.

The API for this isn't exactly documented, but it seems pretty clean, and I'm
not going to go over the process of using it. I hacked up [a flask app][4],
and now I can type `py dict.update` into my address bar and get exactly what
I wanted.

It's fairly easy to get running. Feel free to get in touch if you have any
questions or if you're lazy and just want to use my instance.

[1]: <https://www-archive.mozilla.org/docs/end-user/keywords.html>
[2]: <https://docs.python.org/3/>
[3]: <http://www.sphinx-doc.org/en/stable/ext/intersphinx.html>
[4]: <https://gist.github.com/edk0/968184ee9688d95c5a26446b5b951014>
