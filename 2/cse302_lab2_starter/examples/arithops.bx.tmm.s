	.section .rodata
.lprintfmt:
	.string "%ld\n"
	.text
	.globl main
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $144, %rsp
	movq $42, -8(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -16(%rbp)
	movq $1, -24(%rbp)
	movq -16(%rbp), %r11
	movq -24(%rbp), %rcx
	sarq %cl, %r11
	movq %r11, -32(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -40(%rbp)
	movq -32(%rbp), %r11
	movq %r11, -48(%rbp)
	movq -40(%rbp), %r11
	addq -48(%rbp), %r11
	movq %r11, -56(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -56(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -64(%rbp)
	movq -32(%rbp), %r11
	movq %r11, -72(%rbp)
	movq -64(%rbp), %r11
	subq -72(%rbp), %r11
	movq %r11, -80(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -80(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -88(%rbp)
	movq $3, -96(%rbp)
	movq -88(%rbp), %rax
	imulq -96(%rbp)
	movq %rax, -104(%rbp)
	movq -32(%rbp), %r11
	movq %r11, -112(%rbp)
	movq -104(%rbp), %r11
	addq -112(%rbp), %r11
	movq %r11, -120(%rbp)
	movq -120(%rbp), %r11
	movq %r11, -128(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -136(%rbp)
	movq -128(%rbp), %rax
	cqto
	idivq -136(%rbp)
	movq %rdx, -144(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -144(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq %rbp, %rsp
	popq %rbp
	xorq %rax, %rax
	retq
