section .data
    text db "hello world!",10

section .text
    global _start

_start:
    call _print

_exit:
    mov rax, 60
    mov rdi, 0
    syscall

_print:
    mov rax, 1 
    mov rdi, 1
    mov rsi, text
    mov rdx, 13
    syscall
    ret