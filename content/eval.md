Title: order of evaluation
Date: 2015-07-16 21:20
Tags: c, ramble
Category: c
Slug: eval
Summary: ...

C tutorials and references frequently talk about the “order of evaluation” of 
expressions in C. On the face of it this is not unreasonable; it does make sense 
in algebra, after all. However, in C (and most languages that derive from it), 
the order in which things are evaluated is rarely specified at all. For example, 
in the following expression:

    :::c
    (x = y) + x

the expression in parenthesis is not evaluated first. In fact, the evaluation of 
`(x = y)` relative to the other evaluation of `x` is not ordered at all, and
this expression causes undefined behaviour. Similarly, given an expression like:

    :::c
    a() + b() * c()

`a()`, `b()`, and `c()` must be evaluated in a particular order, but it is
unspecified *which* order, and a strictly conforming program could not depend on
the order being consistent with the grouping of the operands.


## an incomplete guide to the actual order of evaluation

- for the majority of operators, the order in which their operands are evaluated 
  is unspecified
- `&&`, `||`, `?:` and `,` sequence the evaluation of their operands 
  left-to-right
- assignment operators sequence the update of their left operand after the
  evaluation of their operands (so `a = a + 1` is well-defined). This does not
  imply sequencing relative to any other operations, so `a = a++` contains
  unsequenced updates to `a` and hence is undefined.


## <a name="misconceptions"></a>related common misconceptions

- The `,` in the parameter list of a function call is not the comma operator, 
  and does not sequence its operands.
- Operators that prevent their operands being evaluated (`&&` and so on) do so 
  regardless of the precedence of any part of their operand.
