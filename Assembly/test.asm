section .data
    text db "name? "
    text2 db "hey "

section .bss
    name resb 16

section .text
    global _start

_start:
    call _hello
    call _get
    call _hey
    call _name
    call _exit

_hello:
    mov rax, 1
    mov rdi, 1
    mov rsi, text
    mov rdx, 6
    syscall
    ret

_hey:
    mov rax, 1
    mov rdi, 1
    mov rsi, text2
    mov rdx, 5
    syscall
    ret

_get:
    mov rax, 0
    mov rdi, 0
    mov rsi, name
    mov rdx, 16
    syscall
    ret

_name:
    mov rax, 1
    mov rdi, 1
    mov rsi, name
    mov rdx, 16
    syscall
    ret

_exit:
    mov rax, 60
    mov rdi, 0
    syscall
