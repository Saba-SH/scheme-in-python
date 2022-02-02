(define (sum lst)
    (if (null? lst)
        0
        (+ (car lst) (sum (cdr lst)))
    )
)

(define (all-subseqs lst)
    (if (null? lst)
        '(())
        (append 
            (all-subseqs (cdr lst))
            (map 
                (lambda (l) (cons (car lst) l))
                (all-subseqs (cdr lst))
            )
        )
    )
)

(define (firstN lst n)
    (if (= n 0)
        '()
        (cons (car lst) (firstN (cdr lst) (- n 1)))
    )
)

(define (exceptN lst n)
    (if (= n 0)
        lst
        (exceptN (cdr lst) (- n 1))
    )
)

(define (chop lst n)
    (if (null? lst)
        '()
        (cons (firstN lst n) (chop (exceptN lst n) n))
    )
)

(define (sticked lst k s)
    (apply append 
        (map 
            (lambda (l) 
                (if (not (and (= (length l) k) (= (sum l) s)))
                    '()
                    l
                )
            )
            (all-subseqs lst)
        )
    )
)

(define (contains lst l)
    (if (null? lst)
        #f
        (if (equal? l (car lst))
            #t
            (contains (cdr lst) l)
        )
    )
)

(define (make-unique lst)
    (if (null? lst)
        lst
        (if (contains (cdr lst) (car lst))
            (make-unique (cdr lst))
            (cons (car lst) (make-unique (cdr lst)))
        )
    )
)

(define (sum-set lst k s)
    (make-unique (chop (sticked lst k s) k))
)

; ###TESTS###
(display (equal? (sum-set '(1 2 3 4) 2 5) '('(2 3) '(1 4))))	; TEST 1
(newline)
(display (equal? (sum-set '(2 2 1 5 6) 3 9) '('(2 1 6) '(2 2 5))))	; TEST 2
(newline)
(display (equal? (sum-set '(1 1 1 1 1 1) 4 5) '()))	; TEST 3
(newline)
