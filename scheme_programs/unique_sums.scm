(define (all-sums lst)
    (if (null? lst)
        '(0)
        (append
                (map 
                    (lambda (n) (+ n (car lst)))
                    (all-sums (cdr lst))
                )
                (all-sums (cdr lst))
        )
    )
)

(define (contains a lst)
    (cond ((null? lst) #f) 
        ((= a (car lst)) #t)
        (else (contains a (cdr lst)))
    )
)

(define (make-unique lst)
    (cond ((null? lst) '())
        ((contains (car lst) (cdr lst)) (make-unique (cdr lst)))
        (else (cons (car lst) (make-unique (cdr lst))))
    )
)

(define (sums lst)
    (make-unique (all-sums lst))
)

(define (unique-sums lst)
    (length (sums lst))
)

; ###TESTS###

(display (= 4 (unique-sums '(1 2))))
(newline)
(display (= 7 (unique-sums '(1 2 3))))
(newline)
(display (= 5 (unique-sums '(2 2 4))))
(newline)
(display (= 22 (unique-sums '(1 2 3 4 5 6))))
(newline)
(display (= 22 (unique-sums '(1 2 3 5 10))))
(newline)
(display (= 7 (unique-sums '(1 1 1 1 1 1))))
(newline)

