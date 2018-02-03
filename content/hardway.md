Title: on "Learn C The Hard Way"
Date: 2015-11-29 07:21
Tags: c, education
Category: c
Slug: hardway
Summary: ...

_Learn C The Hard Way_ is (irritatingly) a frequent subject of debate in `##c` 
on freenode, so I've had several occasions to reflect on its value and what it 
does so wrong.

It boils down to this: apart from being completely wrong in places, it's 
dogmatic and is essentially teaching—if at all—by rote. Most pages begin with an 
introduction with almost no technical content.  They follow with a large sample 
program you are to type into your computer by hand, then a bulleted explanation 
of what is going on.  Finishing up, we have some expected output from the 
program and a list of questions you can think about for "extra credit".

When I read the book it took determination to read anything after the sample 
program; there's no motivation to do so. I don't have evidence for this, but I 
wouldn't be surprised if it's common for readers to copy the sample program, 
run it, see that its output matches Zed's expected output, and move on.

I suspect this is the reason for Zed's good feedback: People just read his 
book, learn roughly what C syntax looks like by repetition, get to the end and 
feel successful.

I mentioned I find LCTHW dogmatic, so let me give a couple of examples of that:

> C gives you power over the false reality of abstraction and liberates you from 
> stupidity.

This sounds like a recruitment pitch from some kind of cult. It's also
objectively wrong—C _is_ an abstraction.

> An IDE, or "Integrated Development Environment" will turn you stupid.

This is ridiculous. I think it's a good idea to learn how to write C without an 
IDE, but dismissing all of a certain kind of tool for all uses is just poor 
engineering.

Finally (almost), and I mention this because it's directly relevant to the 
quality of the book, I don't get the impression Zed is a particularly capable C 
programmer. He makes amateurish mistakes all over the place, and people who 
learn from his book will make those mistakes too. Readers are taught three 
somewhat broken hash functions without any exposition of their weaknesses and 
the situations in which they should be avoided. In Exercise 43, we see an 
implementation of standard deviation:

```c
return sqrt( (st->sumsq - ( st->sum * st->sum / st->n)) / (st->n - 1) );
```

This does _look_ like a reasonable approach for computing standard deviation, 
but in fact suffers from catastrophic loss of precision for certain data 
distributions. This might have been an excellent way to introduce the problems 
with floating-point and strategies for mitigating them; instead, it's ignored 
and readers are left to make this mistake in real programs. I can only assume 
the author simply doesn't realise this kind of problem exists.

To add insult to injury, the book impresses upon the reader the importance of 
"safe" coding what feels like every other page—while teaching practices that 
will leave your programs riddled with errors, including potential 
denial-of-service vulnerabilities.

_Please_ don't read this book. If you do, you will become a worse C 
programmer—even if you didn't know any C when you started. The total value of 
its content is less than nothing. Buy or borrow a copy of K&R2.

Thank you for reading this, and if you decide to ignore me and read LCTHW 
anyway, please at least consider skipping its exercises on hashtables and 
statistics.

---

With these objections covered, I'd also like to address the book's numerous 
technical errors, which don't seem to get much exposure. I don't know if that's 
because it's so boring to list all of them, or because nobody reads enough of 
the words to notice them, but I feel this needs to be done. I don't promise to 
get all the way through the book:


##Exercise 5

> A variable declaration and assignment at the same time. This is how you 
> create a variable, with the syntax `type name = value;`. In C statements 
> (except for logic) end in a `';'` (semicolon) character.

This is initialization, not assignment (§6.7.9). Also, in C, declarations are 
not statements.

##Exercise 6

> Character
> Declared with `char`, written with a `'` (single-quote) character around the 
> char, and then printed with `%c`.

In fact, single-quoted constants in C are `int`, not `char`.

##Exercise 8

The use of `%ld` to print sizes is sloppy. C99—which, given the prevalence of 
`//` comments, I can only assume the book is written in—provides `%zu`, which 
is always the correct format specifier for printing sizes.

##Exercise 9

> There's also two syntaxes for doing a string: `char name[4] = {'a'}` on line 
> 6 vs. `char *another = "name"` on line 44.

The equivalent syntaxes would be `char name[4] = {'a'};` and `char name[4] = 
"a";`. The book claims that the two snippets offered "work out to be the same 
thing", which just isn't true.

> to the C language there's no difference between a string and an array of 
> characters.

This is not true. There is no string type, but not all arrays of characters are 
strings, nor are all strings arrays of characters.

##Exercise 10

> From this you should be able to figure out that in C you make an "array of 
> strings" by combining the `char *str = "blah"` syntax with the `char str[] = 
> {'b','l','a','h'}` syntax to construct a 2-dimensional array.

I'm not entirely sure what "combining" these has to do with the resulting 
syntax the text offers, but in any case it's not a 2-dimensional array. `char 
*states[] = ...` is an array of pointers, which has advantages and disavantages 
compared with actual multidimensional arrays (better termed arrays of arrays).  
But you're not going to find out what those advantages are because the book 
will resolutely pretend they're the same thing.

##Exercise 11

> In C, there's not really a "boolean" type

C has had a boolean type (`_Bool`) for 16 years.

> instead any integer that's 0 is "false" and otherwise it's "true"

Also any floating-point zero and any pointer value that is null, though I
suppose one could argue that this is an omission rather than an error.

##Exercise 12

> Something common in every language is the `if-statement`

This is obviously not true, although it's also so stupid I almost didn't include 
it.

There is no `else if` construction in C; it's an effect of the syntax of `if`.

> You don't need the `{}` braces to enclose the code, but it is _very_ bad form 
> to not use them

I disagree, but this is not an unreasonable position. Why, then, is `if` 
without braces used in subsequent exercises 17, 18, 19, 20, 25, 26, 33, 34, 36, 
37, 43, 46 and 47?

##Exercise 14

The arguments to `is*` are not converted to `(unsigned char)`, potentially 
causing undefined behaviour.

##Exercise 15

> You however need 2 levels, since `names` is 2-dimensional, that means you 
> need `char **` for a "pointer to (a pointer to char)" type

Conflating multidimensional arrays and arrays of pointers again…

> To C `ages` is a location in the computer's memory where all of these 
> integers start. It is _also_ an address, and the C compiler will replace 
> anywhere you type `ages` with the address of the very first integer in 
> `ages`.

This is incorrect. `ages` is an identifier with an array type. In most contexts 
it is converted to a pointer, but this doesn't mean it "is" one. Even if it 
did, in some cases the conversion does not take place (for example, as the 
operand of the `sizeof` operator). Strangely, the book does go on to talk about 
the difference between pointers and arrays later on the same page, warning the 
reader about making mistakes of the kind it just made.

> C thinks your whole computer is one massive array of bytes

No, it doesn't. C makes no assumptions about the meanings of pointer 
representations. C implementations for segmented-memory architectures exist.

> The purpose of a pointer is to let you manually index into blocks or memory 
> when an array won't do it right

Let's just ignore all the other applications of pointers, like the `char *` 
strings the book has been using throughout.

##Exercise 16

> I use `malloc` for "memory allocate" to ask the OS to give me a piece of raw 
> memory.

`malloc` need not "ask the OS" for anything, and frequently doesn't in 
real-world scenarios.

> I use `assert` to make sure that I have a valid piece of memory back from 
> malloc.

Which is pretty stupid, given this is supposed to be an exceptional condition 
check. If `NDEBUG` is defined (as is likely for production builds—that's sort 
of the point of it), `assert` is a no-op.

`strdup` is not part of any C standard. I find myself more and more confused 
about what language we're supposed to be learning.

##Exercise 17

> I use the `atoi` function

This is a bad idea. It's difficult to think of something good to say about 
`atoi`; it should probably never be used, certainly shouldn't be used for 
unvalidated input, and really really should not be presented to new programmers 
as a viable tool they should regularly use.

> From now on when I say "NULL is 0" I mean its value for anyone who is overly 
> pedantic.

**IT'S A FUCKING TECHNICAL BOOK!** Given the "dangerous" nature of C (a point 
which the book does not fail to labour), precision is of utmost importance, and 
dismissing concerns about precision of utmost recklessness. Also, anyone overly 
pedantic would note that `NULL` doesn't have a well-defined value (it could be 
`(void *)0` or `0`), so this doesn't really clarify anything.

> C is different because it's using the real CPU's actual machinery to do its 
> work, and that involves a chunk of ram called the stack and another called 
> the heap.

This is not true. It could use the real CPU's actual machinery, but being 
abstractly specified, it could also do anything your compiler thinks is a 
better idea.

On some modern systems, "the heap" no longer exists, highlighting the perils of 
trying to talk about C by talking about an implementation of C instead.

> The easiest way to keep this straight is with this mantra: If you didn't get 
> it from `malloc` or a function that got it from `malloc`, then it's on the 
> stack.

Not only is this obviously wrong—what about static variables?—it's pretty 
useless, unless you remember exactly which functions call `malloc` in which 
circumstances.

##Exercise 19

> In modern C, the cpp system is so integral to C's function that you might as 
> well just consider it to be part of the language.

In fact, it _is_ part of the language, and has been specified as such in every 
version of the C standard.

##Exerise 20

Defining `__dbg_h__` (or using it at all) is undefined behaviour, as it's a 
reserved identifier in C.

`, ##__VA_ARGS__` is a GNU extension and should if nothing else be labeled as 
such.

The description of how macros are expanded does not appear to cover how macros 
are expanded at all.

##Exercise 21

> Forces the compiler to keep this variable in a register, and the compiler can 
> just ignore you

Which is it!?

##Exercise 22

In C, `const` does not create constants.
