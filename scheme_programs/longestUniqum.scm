(define (sublistOfN lst n)
    (if (= 0 n)
        '()
        (cons (car lst) (sublistOfN (cdr lst) (- n 1)))
    )
)

(define (generateSublists lst n)
    (if (< (length lst) n)
        '()
        (append (generateSublists (cdr lst) n) (list (sublistOfN lst n)))
    )
)

(define (contains v lst)
    (if (null? lst)
        #f
        (or (= (car lst) v)
            (contains v (cdr lst))
        )
    )
)

(define (isUniqum lst)
    (if (null? lst)
        #t
        (and 
            (not (contains (car lst) (cdr lst)))
            (isUniqum (cdr lst))
        )
    )
)

(define (firstUniqum lsts)
    (if (null? lsts)
        '()
        (if (isUniqum (car lsts))
            (car lsts)
            (firstUniqum (cdr lsts))
        )
    )
)

(define (helperHelper lst l h)
    ;binary search

    (cond ((= l h)
            (firstUniqum (generateSublists lst l))
        )
        ((= (- h l) 1)
            (if (null? (firstUniqum (generateSublists lst h)))
                (firstUniqum (generateSublists lst l))
                (firstUniqum (generateSublists lst h))
            )
        )
        ((null? (firstUniqum (generateSublists lst (quotient (+ l h) 2))))
            (helperHelper lst l (quotient (+ l h -1) 2))   ;მარცხნივ
        )
        (else 
            (helperHelper lst (quotient (+ l h) 2) h)     ;მარჯვნივ
        )
    )
)

(define (uniqumHelper lst n)
    (helperHelper lst 0 n)
)

(define (longestUniqum lst)
    (uniqumHelper lst (length lst))
)

; ###TESTS###

; basic tests
(display (equal? (longestUniqum '(1 2 3 4 2 3 4 1 2)) '(3 4 1 2)))	; TEST 1
(newline)
(display (equal? (longestUniqum '(1 2 4 3 5 6 5 4 3)) '(1 2 4 3 5 6)))	; TEST 2
(newline)

; longer list of digits
(display (equal? (longestUniqum '(3 3 1 2 6 3 6 2 8 2 9 6 9 1 1 2 8 1 2 2)) '(8 2 9 6)))	; TEST 3
(newline)

; longer list of numbers 0-19
(display (equal? (longestUniqum '(8 14 11 3 11 1 4 5 17 12 3 12 15 0 10 10 6 9 9 12 11 6 5 12 7 3 18 4 9 6)) '(11 6 5 12 7 3 18 4 9)))	; TEST 4
(newline)

; even longer list of numbers 0-99
(display (equal? (longestUniqum '(36 52 88 7 6 75 70 4 62 66 13 30 9 90 75 91 35 89 30 88 92 8 32 31 69 15 59 75 92 35 14 30 73 76 43 20 26 25 20 8)) '(8 32 31 69 15 59 75 92 35 14 30 73 76 43 20 26 25)))	; TEST 5
(newline)

; many large numbers over a short interval
(display (equal? (longestUniqum '(3540 3542 3549 3558 3558 3544 3540 3552 3553 3551 3541 3541 3555 3545 3541 3540 3554 3558 3541 3556 3550 3546 3552 3545 3543 3545 3541 3549 3549 3546)) '(3540 3554 3558 3541 3556 3550 3546 3552 3545 3543)))	; TEST 6
(newline)

; less large numbers over a long interval
(display (equal? (longestUniqum '(4885 11222 9861 6411 10372 5329 15021 7720 7992 17480 19910 10163 12589 3255 16114 17874 4956 8146 11078 6399 7477 3822 11111 8716 12345 15043 13096 4544 7779 16409)) '(4885 11222 9861 6411 10372 5329 15021 7720 7992 17480 19910 10163 12589 3255
 16114 17874 4956 8146 11078 6399 7477 3822 11111 8716 12345 15043 13096 4544
 7779 16409)))	; TEST 7
 (newline)

