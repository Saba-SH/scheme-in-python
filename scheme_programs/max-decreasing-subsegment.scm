(define (getMax lst1 lst2)
    (if (null? lst1) 
        lst2
        (cond 
            ((> (car lst1) (car lst2))
                lst1
            )
            ((< (car lst1) (car lst2))
                lst2
            )
            (else
                (cons (car lst1) (getMax (cdr lst1) (cdr lst2)))
            )
        )
    )
)

(define (getMaxStart lsts)
    (if (null? lsts)
        '()
        (if (null? (cdr lsts))
            (car lsts)
            (getMax (car lsts) (getMaxStart (cdr lsts)))
        )
    )
)

(define (firstN lst n)
    (if (= n 0)
        '()
        (cons (car lst) (firstN (cdr lst) (- n 1)))
    )
)

(define (generateSubsegs lst n)
    (if (< (length lst) n)
        '()
        (cons (firstN lst n) (generateSubsegs (cdr lst) n))
    )
)

(define (isDecr lst)
    (apply > lst)
)

(define (exceptFirstN lst n)
    (if (= n 0)
        lst
        (exceptFirstN (cdr lst) (- n 1))
    )
)

(define (chop lst n)
    (if (null? lst)
        '()
        (cons (firstN lst n) (chop (exceptFirstN lst n) n))
    )
)

(define (generateDecrSubsegs lst n)
    (chop (apply append (map (lambda (l) 
                            (if (isDecr l) 
                                l 
                                '()
                            )
                        )
                        (generateSubsegs lst n)
                )
    ) n)
)

(define (getMaxDecr seq n)
    (getMaxStart (generateDecrSubsegs seq n))
)

(define (helper seq l h)
    ;binary search
    
    (cond
        ((= (- h l) 1)
            (if (null? (getMaxDecr seq h))
                (getMaxDecr seq l)
                (getMaxDecr seq h)
            )
        )
        ((= h l)
            (getMaxDecr seq h)
        )
        ((null? (getMaxDecr seq (quotient (+ h l) 2)))
            (helper seq l (- (quotient (+ h l) 2) 1))
        )
        (else
            (helper seq (quotient (+ h l) 2) h)
        )
    )
)

; For the given list, return the longest strictly decreasing subsegment.
; If there are more than one, choose the one with the highest elements(priority goes to early elements).
(define (max-decreasing-subsegment sequence)
    (helper sequence 0 (length sequence))
)

; ###TESTS###

(display (equal? (max-decreasing-subsegment '(1 2 3 4 3 2 1)) '(4 3 2 1)))	; TEST 1
(newline)
(display (equal? (max-decreasing-subsegment '(8 7 9 4 6 5)) '(9 4)))	; TEST 2
(newline)
(display (equal? (max-decreasing-subsegment '(2 2 2 2 1 1 1 1 1 )) '(2 1)))	; TEST 3
(newline)
(display (equal? (max-decreasing-subsegment '(5 4 3 2 4 3 2 1)) '(5 4 3 2)))	; TEST 4
(newline)
(display (equal? (max-decreasing-subsegment '(7 7 6 6 5 5 4 4 3 3)) '(7 6)))	; TEST 5
(newline)
(display (equal? (max-decreasing-subsegment '(1 2 3 4 5 6 7 8 9)) '(9)))	; TEST 6
(newline)
(display (equal? (max-decreasing-subsegment '(9 7 8 6 4 5 2 3 1)) '(8 6 4)))	; TEST 7
(newline)
(display (equal? (max-decreasing-subsegment '(2 2 2 2)) '(2)))	; TEST 8
(newline)
(display (equal? (max-decreasing-subsegment '(9 8 7 6 5 4 3 2 1 0)) '(9 8 7 6 5 4 3 2 1 0)))	; TEST 9
(newline)
(display (equal? (max-decreasing-subsegment '(8 6 4 2 0 9 7 5 3 1)) '(9 7 5 3 1)))	; TEST 10
(newline)
