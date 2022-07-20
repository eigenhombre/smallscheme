from smallscheme.scheme import *
from smallscheme.test_util import teq

def test_evalu():
    """
    Thin, lower-level smoke test of `evalu` function.  Much more
    testing of evaluation is done below.
    """
    def t(a, b):
        teq(evalu(a, {}), b)
    t(int_(1234), int_(1234))
    t(int_(1234), int_(1234))
    t(bool_(True), bool_(True))
    t(bool_(False), bool_(False))
    t(atom('+'), ('intproc', '+'))
    t(list_([atom('quote'),
             int_(3)]),
      int_(3))
    t(list_([atom('quote'),
             list_([atom('a'),
                    atom('b'),
                    atom('c')])]),
      list_([atom('a'),
             atom('b'),
             atom('c')]))

def single_eval_check(s1, s2, env):
    teq(printable_value(evalu(parse_str(s1)[0],
                              env)),
        s2)

def multiple_eval_check(s1, env, *s2):
    ret = None
    for p in parse_str(s1):
        ret = evalu(p, env)
    if s2:
        teq(printable_value(ret), s2[0])

def test_printable_value():
    def t(s1, *s2):
        multiple_eval_check(s1, {}, *s2)

    t("1234", "1234")
    t("#f", "#f")
    t("#t", "#t")
    t("+", "Internal procedure '+'")
    t("/", "Internal procedure '/'")
    t("(quote a)", "a")
    t("()", "()")
    t("(quote 0)", "0")
    t("(quote (1 2 3))", "(1 2 3)")
    t("(quote (a b c))", "(a b c)")
    t("(+ 1 1)", "2")
    t("(+ 1 2 3)", "6")
    t("(+ 1 2 (+ 1 1 1))", "6")
    t("(* 1 1)", "1")
    t("(* 1 2 3 4 5)", "120")
    t("""(+ 1
            2
            3)""", "6")
    t("(- 10 7)", "3")
    t("(- 10)", "-10")
    t("(/ 10 5)", "2")
    t("(/ 16 2 2 2)", "2")
    t("(+ 3 5)", "8")
    t("(* 2 4)", "8")
    t("(+ (* 2 4) (+ 3 5))", "16")
    t("""(+ (* 3
               (+ (* 2 4)
                  (+ 3 5)))
            (+ (- 10 7)
               6))""", "57")
    t("(= 1 1)", "#t")
    t("(= 1 2)", "#f")
    t("(= 1 (quote notone))", "#f")
    t("(= #t #t)", "#t")
    t("(not #t)", "#f")
    t("(not #f)", "#t")
    t("(not 1)", "#f")
    t("(> 2 1)", "#t")
    t("(> 1 2)", "#f")
    t("(< 2 1)", "#f")
    t("(< 1 2)", "#t")
    # FIXME: higher arities of < and >.
    t("(cond (#t #t))", "#t")
    t("(cond (#t 3))", "3")
    t("(cond (#t #f))", "#f")
    t("(cond (#f #f) (#t #f))", "#f")
    t("(cond (#f #f) (#t #t))", "#t")
    t("(cond (#f #f) (else #t))", "#t")
    t("(if #t 1 2)", "1")
    t("(if #f 1 2)", "2")
    t("(or)", "#f")
    t("(or 1)", "1")
    t("(or #f 1)", "1")
    t("(or 1 1)", "1")
    t("(and)", "#t")
    t("(and #t)", "#t")
    t("(and 1 #t)", "#t")
    t("(and #t 1)", "1")
    t("(and #t #f)", "#f")
    t("(and #f #f)", "#f")

def test_define():
    def t(a, b, env1):
        env = {}
        teq(printable_value(evalu(parse_str(a)[0],
                                  env)), b)
        assert env == env1, (
            "Environment mismatch: '%s' vs '%s'" %
            (env, env1))

    t("(define size 2)", "", {'size': int_(2)})

def test_multiple_defines():
    env = {}
    def t(s1, *s2):
        multiple_eval_check(s1, env, *s2)
    # Adapted from SICP p. 8:
    t("(define pi 3.14159)")
    t("(define radius 10)")
    t("(* pi (* radius radius))", "314.159")
    t("(define circumference (* 2 pi radius))")
    t("circumference", "62.8318")
    # p. 19:
    t("(define x 7)")
    t("(and (> x 5) (< x 10))", "#t")
    t("(car (quote (1 2 3)))", "1")
    t("(car (quote (a b c)))", "a")
    t("(cdr (quote (1 2 3)))", "(2 3)")
    t("(cdr (quote (a b c)))", "(b c)")

def test_random():
    for _ in range(50):
        t, v = evalu(parse_str("(random 10)")[0], {})
        assert t == 'int'
        assert 0 <= v < 10

def test_compound_expressions_with_env():
    """
    Define test cases in groups with state / environments
    accumulating/evolving within but not across the groups.
    """
    def c(s1, s2=""):
        return [s1, s2]

    def cases(*cases):
        env = {}
        # Functions used a lot, we'll add to "global" state:
        setup_cases = ["(define (square x) (* x x))"]
        for s1 in setup_cases:
            single_eval_check(s1, "", env)

        for s1, s2 in cases:
            single_eval_check(s1, s2, env)
        # Helpful for debugging:
        # print(env)

    cases(c("(+ 1 1)", "2"))
    cases(c("(define b 4)"),
          c("(define a 3)"),
          c("(+ 1 (* a b))", "13"))
    cases(c("square", "Function-'square'"),
          c("(square 21)", "441"),
          c("(square (+ 2 5))", "49"),
          c("(square (square 3))", "81"),
          c("""(define (sum-of-squares x y)
                 (+ (square x) (square y)))"""),
          c("(sum-of-squares 3 4)", "25"),
          c("(define (f a) (sum-of-squares (+ a 1) (* a 2)))"),
          c("(f 5)", "136"))
    cases(c("(define (f x y) (+ x y))"))
    cases(c("(define z 33)"))

# FIXME: Migrate to test_compound_expressions_with_env:
def test_compound_expressions():
    env = {}
    def t(s1, *s2):
        multiple_eval_check(s1, env, *s2)

    t("(define (square x) (* x x))")
    t("""(define (abs x)
           (cond ((> x 0) x)
                 ((= x 0) 0)
                 ((< x 0) (- x))))
         (abs 10)""",
      "10")
    t("(abs -10)", "10")

    t("""(define (abs x)
           (cond ((< x 0) (- x))
                 (else x)))""")
    t("(abs 10)", "10")
    t("(abs -10)", "10")

    t("""(define (abs x)
           (if (< x 0)
               (- x)
               x))""")
    t("(abs 10)", "10")
    t("(abs -10)", "10")

    t("""(define (factorial n)
           (if (= n 1)
               1
               (* n (factorial (- n 1)))))""")
    t("(factorial 1)", "1")
    t("(factorial 2)", "2")
    t("(factorial 3)", "6")
    t("(factorial 10)", "3628800")
    t("(factorial 20)", "2432902008176640000")

    # P. 23-24:
    t("""(define (sqrt-iter guess x)
           (if (good-enough? guess x)
               guess
               (sqrt-iter (improve guess x)
                          x)))""")
    t("""(define (improve guess x)
           (average guess (/ x guess)))""")
    t("""(define (average x y)
           (/ (+ x y) 2))""")
    t("""(define (good-enough? guess x)
           (< (abs (- (square guess) x)) 0.001))""")
    t("""(define (sqrt x)
           (sqrt-iter 1.0 x))""")
    # These may or may not pass; they do on my
    # Macbook Pro:
    # t("(sqrt 9)", "3.0")
    # t("(square (sqrt 100))", "100.0")
    t("""(define (a) 3)""")
    t("(a)", "3")
    t("""(define (a) (+ 1 2))""")
    t("(a)", "3")
    t("""(define (a) 1 666)""")
    t("(a)", "666")
    t("""(define (a)
           (define b 3)
           b)""")
    t("(a)", "3")
    t("""(define (a)
           (define (f) 4)
           (f))""")
    t("(a)", "4")

    t("+", "Internal procedure '+'")
    t("(define round square)")
    t("(round 5)", "25")

    # p. 30
    t("""(define (sqrt x)
           (define (good-enough? guess)
             (< (abs (- (square guess) x)) 0.001))
           (define (improve guess)
             (average guess (/ x guess)))
           (define (sqrt-iter guess)
             (if (good-enough? guess)
               guess
               (sqrt-iter (improve guess))))
           (sqrt-iter 1.0))""")
    t("(sqrt 9)", "3.0")

    # p. 37
    t("""(define (fib n)
           (cond ((= n 0) 0)
                 ((= n 1) 1)
                 (else (+ (fib (- n 1))
                          (fib (- n 2))))))""")
    t("(fib 5)", "5")

    # empty list and cons
    t("(quote ())", "()")
    t("(cons 3 (quote ()))", "(3)")
    t("(cons (quote a) (quote ()))", "(a)")
    t("(cons (quote b) (quote (1 2 3)))", "(b 1 2 3)")

    # lambdas and higher-order functions
    t("(define fn-list (cons square (quote ())))")
    t("((car fn-list) 3)", "9")

    t("(lambda (x) 3)", "Anonymous-function")
    t("((lambda (x) 3) 1)", "3")
    t("((lambda (x) 6) 1 2 3)", "6")

    # p. 45
    t("(remainder 10 3)", "1")
