Title: the “inline” keyword
Date: 2014-05-02 14:50
Tags: c, ramble
Category: c
Slug: inline
Summary: ...

C has a keyword called `inline`. It's a source of considerable grief among
people who don't understand what it does—which, as I've discovered recently,
includes people who have an otherwise understand C very well.

It's common to see people make assertions like “you should only ever use
inline with static,” which turns out to be reasonable advice. I don't think
advice without explanation is very useful, though, so what follows is my
attempt to explain `inline`'s strange behaviour.

Let's say you have a program, and, like all good programs, it looks like this:

    :::c
    #include <stdio.h>

    inline void foo(void) {
        puts("hi");
    }

    int main(void) {
        foo();
        return 0;
    }

It looks good! Let's compile it:

    :::console
    $ gcc -otest -std=c99 test.c
    /tmp/ccBRwXBz.o: In function `main':
    test.c:(.text+0x5): undefined reference to `foo'
    collect2: ld returned 1 exit status

Of those I've spoken to, most people's reaction is that this is a compiler
bug. I'm no gcc evangelist, but in this instance it is actually behaving
correctly; the standard doesn't require this program to work.

The definition of `foo` in my example has the `inline` keyword and no `extern`
keyword—this is true for every declaration of `foo`, since it's the only one.
[N1570 §6.7.4p7](http://iso-9899.info/n1570.html#6.7.4p7) stipulates that when
this is the case, the identifier `foo` is declared with external linkage, but
that *no external definition is provided*.

In other words, `foo` refers to an external function that we haven't defined.
An inline definition of `foo` has been provided, and is available to the
compiler as a substitute for the external definition, but the compiler isn't
required to use it.

The upshot of this is that when a function is declared as inline without also
being declared static or extern, programs commonly get into a state where they
depend on an unspecified compiler decision in order to link. This isn't always
the case—the behaviour could be used to provide an inline alternative to an
external function defiend in another translation unit, which is presumably why
it's still a part of C.

If I were a writer, this is where I would finish with some clever and
final-sounding remark.

