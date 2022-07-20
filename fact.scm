
(define (fact n)
  (if (< n 2)
      n
      (* n (fact (- n 1)))))

(define f100 (fact 100))

(display f100)
(newline)

