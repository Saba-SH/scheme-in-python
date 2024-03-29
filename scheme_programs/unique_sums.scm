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

; For the given list, return the amount of unique sums existing among all the subsequences of the list.
; Subsequence means not necessarily continuous. Empty subsequence is included.
(define (unique-sums lst)
    (length (sums lst))
)

; ###TESTS###

(display (= 4 (unique-sums '(1 2))))    ; TEST 1
(newline)
(display (= 7 (unique-sums '(1 2 3))))  ; TEST 2
(newline)
(display (= 5 (unique-sums '(2 2 4))))  ; TEST 3
(newline)
(display (= 22 (unique-sums '(1 2 3 4 5 6))))   ; TEST 4
(newline)
(display (= 22 (unique-sums '(1 2 3 5 10))))    ; TEST 5
(newline)
(display (= 7 (unique-sums '(1 1 1 1 1 1))))    ; TEST 6
(newline)
(display (= 1 (unique-sums '())))   ; TEST 7
(newline)
