	.section .rodata
.lprintfmt:
	.string "%ld\n"
	.text
	.globl main
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $16, %rsp
	movq $9223372036854775808, -8(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -16(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -16(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq %rbp, %rsp
	popq %rbp
	xorq %rax, %rax
	retq
