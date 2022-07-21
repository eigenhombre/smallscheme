(test
 ;; basic truthy / equality stuff
 (is #t)
 (is (not #f))
 (is 0)
 (is ())
 (is (quote nothingness))
 (is (= 1 1))
 (is (not (= 1 2)))
 (is (= 2 (+ 1 1))))

(test
 ;; basic state / defines
 (define b 4)
 (define a 3)
 (is (= 13 (+ 1 (* a b)))))

(define (square x)
  (* x x))

(test
 (is (= 441 (square 21)))
 (is (= 49 (square (+ 2 5))))
 (is (= 81 (square (square 3))))
 (define (sum-of-squares x y)
   (+ (square x) (square y)))
 (is (= 25 (sum-of-squares 3 4)))
 (define (f a)
   (sum-of-squares (+ a 1) (* a 2)))
 (is (= 136 (f 5)))
 (define round square)
 (is (= 25 (round 5))))

(test
 (define (f x y)
   (+ x y))
 (is (= 3 (f 1 2))))

(test
 (define (abs x)
   (cond ((> x 0) x)
         ((= x 0) 0)
         ((< x 0) (- x))))
 (is (= 10 (abs 10)))
 (is (= 10 (abs -10)))

 (define (abs x)
   (if (< x 0)
       (- x)
       x))
 (is (= 10 (abs 10)))
 (is (= 10 (abs -10)))

 (define (abs x)
   (cond ((< x 0) (- x))
         (else x)))

 (is (= 10 (abs 10)))
 (is (= 10 (abs -10))))

(test
 (define (factorial n)
   (if (= n 1)
       1
       (* n (factorial (- n 1)))))
 (is (= 1 (factorial 1)))
 (is (= 2 (factorial 2)))
 (is (= 6 (factorial 3)))
 (is (= 3628800 (factorial 10)))
 (is (= 2432902008176640000 (factorial 20))))


;; # P. 23-24:
(test
 (define (sqrt-iter guess x)
   (if (good-enough? guess x)
       guess
       (sqrt-iter (improve guess x)
                  x)))
 (define (improve guess x)
    (average guess (/ x guess)))
 (define (average x y)
    (/ (+ x y) 2))
 (define (good-enough? guess x)
    (< (abs (- (square guess) x)) 0.001))
 (define (sqrt x)
    (sqrt-iter 1.0 x))

 ;; These may or may not pass; they do on my
 ;; Macbook Pro:
 ;; (is (= 3.0 (sqrt 9))
 ;; (is (= 100.0 (square (sqrt 100))))
)

(test
 ;; p. 30
 (define (sqrt x)
   (define (good-enough? guess)
     (< (abs (- (square guess) x)) 0.001))
   (define (improve guess)
     (average guess (/ x guess)))
   (define (sqrt-iter guess)
     (if (good-enough? guess)
         guess
         (sqrt-iter (improve guess))))
   (sqrt-iter 1.0))
 (is (= 3.0 (sqrt 9))))

(test
 ;; scope, nested or otherwise
 (define (a) 3)
 (is (= 3 (a)))
 (define (a) (+ 1 2))
 (is (= 3 (a)))
 (define (a) 1 666)
 (is (= 666 (a)))
 (define (a)
   (define b 3)
   b)
 (is (= 3 (a)))
 (define (a)
   (define (f) 4)
   (f))
 (is (= 4 (a)))

 ;; This looks weird to me, but it's also how Racket
 ;; does it.  See set! tests, below.
 (define a 3)
 (define (f) (+ 1 a))
 (is (= 4 (f)))
 (define a 4)
 (is (= 5 (f))))

(test
 ;; # p. 37
 (define (fib n)
   (cond ((= n 0) 0)
         ((= n 1) 1)
         (else (+ (fib (- n 1))
                  (fib (- n 2))))))
 (is (= 5 (fib 5))))

(test
 ;; empty list and cons
 (is (= () (quote ())))
 (is (= (quote (3)) (cons 3 (quote ()))))
 (is (= (quote (a)) (cons (quote a) ())))
 (is (= (quote (b 1 2 3)) (cons (quote b) (quote (1 2 3))))))

(test
 ;; lambdas and higher-order functions
 (define fn-list (cons square (quote ())))
 (is (= 9 ((car fn-list) 3)))
 (is (= 3 ((lambda (x) 3) 1)))
 ;; Hmmm.... arity??
 (is (= 6 ((lambda (x) 6) 1 2 3))))

(test
 ;; p. 45
 (is (= 1 (remainder 10 3))))

(test
 ;; p. 50 -- most of this is copied from SICP directly:
 (define (smallest-divisor n)
   (find-divisor n 2))
 (define (find-divisor n test-divisor)
   (cond ((> (square test-divisor) n) n)
         ((divides? test-divisor n) test-divisor)
         (else (find-divisor n (+ test-divisor 1)))))
 (define (divides? a b)
   (= (remainder b a) 0))
 (define (prime? n)
   (= n (smallest-divisor n)))
 (is (prime? 1))
 (is (prime? 2))
 (is (prime? 3))
 (is (not (prime? 4)))
 (is (prime? 5))
 (is (not (prime? 6)))
 (is (prime? 7))
 (is (not (prime? 8)))
 (is (not (prime? 9)))
 (is (not (prime? 10))))

(test
 ;; p. 59
 (define (sum term a next b)
  (if (> a b)
      0
      (+ (term a)
         (sum term (next a) next b))))
 (define (inc n) (+ n 1))
 (define (cube x) (* x x x))
 (define (sum-cubes a b)
   (sum cube a inc b))
 (is (= 3025 (sum-cubes 1 10))))

(test
 ;; begin and set!
 (begin)
 (is (= 1 (begin 1)))
 (is (= 2 (begin 1 2)))
 (test
  ;; From https://stackoverflow.com/questions/526082:
  (define x 3)

  (define (foo)
    (define x 4)
    x)

  (define (bar)
    (set! x 4)
    x)

  (is (= 4 (foo)))
  (is (= 3 x))
  ;; Failing test: YOU ARE HERE (implement set!)
  ;; (is (= 4 (bar)))
  ))
