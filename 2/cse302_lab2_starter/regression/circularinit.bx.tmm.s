	.section .rodata
.lprintfmt:
	.string "%ld\n"
	.text
	.globl main
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $48, %rsp
	movq $42, -8(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -16(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -32(%rbp)
	movq -16(%rbp), %r11
	addq -32(%rbp), %r11
	movq %r11, -24(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -40(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -40(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq %rbp, %rsp
	popq %rbp
	xorq %rax, %rax
	retq
