	.section .rodata
.lprintfmt:
	.string "%ld\n"
	.text
	.globl main
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $96, %rsp
	movq $42, -8(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -16(%rbp)
	movq $1, -24(%rbp)
	movq -16(%rbp), %r11
	movq -24(%rbp), %rcx
	sarq %cl, %r11
	movq %r11, -32(%rbp)
	movq -32(%rbp), %r11
	movq %r11, -40(%rbp)
	movq -16(%rbp), %r11
	addq -40(%rbp), %r11
	movq %r11, -48(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -48(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -16(%rbp), %r11
	subq -40(%rbp), %r11
	movq %r11, -56(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -56(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq $3, -64(%rbp)
	movq -16(%rbp), %rax
	imulq -64(%rbp)
	movq %rax, -72(%rbp)
	movq -72(%rbp), %r11
	addq -40(%rbp), %r11
	movq %r11, -80(%rbp)
	movq -80(%rbp), %r11
	movq %r11, -88(%rbp)
	movq -88(%rbp), %rax
	cqto
	idivq -16(%rbp)
	movq %rdx, -96(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -96(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq %rbp, %rsp
	popq %rbp
	xorq %rax, %rax
	retq
