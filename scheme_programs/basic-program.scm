; ლამბდა ფუნქციები, მაგალითად (lambda (x y) (+ x y))
; ლამბდა ფუნქციების ადგილზე გამოძახება, მაგალითად ((lambda (x y) (+ x y)) 1 2)
(display (equal? ((lambda (x y) (+ x y)) 1 2) 3))   ; TEST 1
(newline)
(display (equal? ((lambda (x y) (mod x (quotient y 2))) 10 11) 0))  ; TEST 2
(newline)

; define მაგალითად (define pi 3.14) ან (define (sum x y) (+ x y))
(define pi 3.14)
(display (equal? (if (= pi 3.14) 5 1) 5))   ; TEST 3
(newline)
(define (sum x y) (+ x y))
(display (equal? (sum pi pi) (* pi 2))) ; TEST 4
(newline)

; არითმეტიკული + - * / ოპერაციები
(display (equal? (+ 10 9) 19))  ; TEST 5
(newline)
(display (equal? (- 20 9) 11))  ; TEST 6
(newline)
(display (equal? (* 12 0) 0))   ; TEST 7
(newline)
(display (equal? (* 4 2 3) 24)) ; TEST 8
(newline)
(display (equal? (/ 36 4 2 5) 0.9)) ; TEST 9
(newline)

; ლოგიკური ოპერაციები and და or
(display (equal? (or (and #t #f) (or #f #t)) #t))   ; TEST 10
(newline)
(display (equal? (and (>= 3 3) (= (* 2 2) 5)) #f))  ; TEST 11
(newline)
(display (equal? (or (>= 3 3) (= (* 2 2) 5)) #t))   ; TEST 12
(newline)

; if/else
; უნდა შეეძლოს რეკურსიული ფუნქციების შესრულება
(define (factorial x)
    (if
        (= x 0) 1
        (* (factorial (- x 1)) x)
    )
)
(display (equal? (factorial 5) 120))    ; TEST 13
(newline)

; სიებთან სამუშაო ფუნქციები: car, cdr, cons, map, append
; სიის აღწერა შესრულების გარეშე: ‘(1 2 3)
(display (equal? (car '(1 2 3)) 1)) ; TEST 14
(newline)
(display (equal? (cdr '(1 2 3)) '(2 3)))    ; TEST 15
(newline)
(display (equal? (cons '(1 2 3) '(1 2 3)) '('(1 2 3) 1 2 3)))   ; TEST 16
(newline)
(display (equal? (map + '(1 2 3) '(10 20 30)) '(11 22 33))) ; TEST 17
(newline)
(display (equal? (append '(1 2 3) '(4 5 6)) '(1 2 3 4 5 6)))    ; TEST 18
(newline)

; შემსრულებელი ფუნქციები: apply, eval
(display (equal? (apply > '(5 4 3)) #t))    ; TEST 19
(newline)
(display (equal? (eval '(<= 5 4 3)) #f))    ; TEST 20
(newline)

; დამხმარე ფუნქციები: null?, length
(display (equal? (null? '()) #t))   ; TEST 21
(newline)
(display (equal? (null? '(1 2 3)) #f))  ; TEST 22
(newline)
(display (equal? (length '('(1 2 3) 1 2 3)) 4)) ; TEST 23
(newline)
(display (equal? (length '('())) 1)) ; TEST 24
(newline)
(display (equal? (length '()) 0))    ; TEST 25
(newline)

; cond
(display (equal? (cond 
                    ((< pi 3) 0) 
                    ((> pi 10) 1) 
                    ((<= pi 6) 2) 
                    ((>= pi 3) 3) 
                    (else 4)
                ) 
            2
        )
) ; TEST 26
(newline)
