(define (sum-list lst)
    (if (null? lst)
        0
        (+ (car lst) (sum-list (cdr lst)))
    )
)

(define (odd-helper n o)
    (if (> o n)
        '()
        (if (= (mod n o) 0)
            (append (list o) (odd-helper n (+ o 2)))
            (odd-helper n (+ o 2))
        )
    )
)

(define (odd-divisors n)
    (sum-list (odd-helper n 1))
)

; ###TESTS###

; basic tests
(display (equal? (odd-divisors 24) 4))	; TEST 1
(newline)
(display (equal? (odd-divisors 17) 18))	; TEST 2
(newline)
(display (equal? (odd-divisors 15) 24))	; TEST 3
(newline)

; power of 2
(display (equal? (odd-divisors 128) 1))	; TEST 4
(newline)

; power of 3
(display (equal? (odd-divisors 81) 121))	; TEST 5
(newline)

; 37 * 3
(display (equal? (odd-divisors 111) 152))	; TEST 6
(newline)

; product of all prime odd digits
(display (equal? (odd-divisors 105) 192))	; TEST 7
(newline)

