Title: ignoring exceptions in Python
Date: 2014-01-28 02:41
Tags: python
Category: python
Slug: sys.excepthook
Summary: .

Sometimes Python programs have unhandled exceptions. Usually these make your
program exit, but wouldn't it be nice if you could fix your environment in a
Python shell and try again? I thought so, so I've written a very silly
exception hook which gives you the option to retry the current line, or skip
past it and continue executing from the next one.

It's implemented using a bytecode-patcher. Anyway, for an example, given this
broken program:

    :::python
    def do_something(foo):
        z = 1 + 2 +3
        print '1 + 2 + 3 = %d' % z

        return foo + bar

    x = do_something(17)
    print x

After the `NameError` is raised when we try to access `bar`, we see this
prompt:

    :::console
    $ python fail.py
    1 + 2 + 3 = 6
    [reckless] intercepting an exception:
    Traceback (most recent call last):
      File "fail.py", line 8, in <module>
        x = do_something(17)
      File "fail.py", line 6, in do_something
        return foo + bar
    NameError: global name 'bar' is not defined
     c : continue execution (insane)
     d : debugger (bpdb)
     e : exit
    [n]: do nothing
     r : retry (insane)
     s : shell (bpython)
    what now?

We can enter `s` and fix the environment by defining `bar`:

    :::pycon
    >>> bar = 9

`^D` to exit the shell, and then enter `r` at the prompt:

    :::console
    [reckless] resuming execution
    26
    [reckless] reached end of program
    $ 

It's [on PyPI](https://pypi.python.org/pypi/reckless). If you're interested in
the gory details of the bytecode patching, I suggest you download it and have
a look at `execute.py` (it's not pretty).
