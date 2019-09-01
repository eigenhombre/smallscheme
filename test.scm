
(define (fact n)
  (if (< n 2)
      n
      (* n (fact (- n 1)))))

(define f10 (fact 10))

(display f10)

