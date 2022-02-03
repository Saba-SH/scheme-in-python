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

; For the given number, return the sum of all odd divisors of that number.
(define (odd-div n)
    (sum-list (odd-helper n 1))
)

; ###TESTS###

; basic tests
(display (equal? (odd-div 24) 4))	; TEST 1
(newline)
(display (equal? (odd-div 17) 18))	; TEST 2
(newline)
(display (equal? (odd-div 15) 24))	; TEST 3
(newline)

; power of 2
(display (equal? (odd-div 128) 1))	; TEST 4
(newline)

; power of 3
(display (equal? (odd-div 81) 121))	; TEST 5
(newline)

; 37 * 3
(display (equal? (odd-div 111) 152))	; TEST 6
(newline)

; product of all prime odd digits
(display (equal? (odd-div 105) 192))	; TEST 7
(newline)

