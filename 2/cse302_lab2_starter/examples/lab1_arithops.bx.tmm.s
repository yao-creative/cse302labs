	.section .rodata
.lprintfmt:
	.string "%ld\n"
	.text
	.globl main
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $256, %rsp
	movq $0, -8(%rbp)
	movq $0, -16(%rbp)
	movq $0, -24(%rbp)
	movq $42, -8(%rbp)
	movq $21, -16(%rbp)
	movq $5, -24(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -40(%rbp)
	movq -32(%rbp), %r11
	addq -40(%rbp), %r11
	movq %r11, -48(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -48(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -56(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -64(%rbp)
	movq -56(%rbp), %r11
	subq -64(%rbp), %r11
	movq %r11, -72(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -72(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -80(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -88(%rbp)
	movq -80(%rbp), %rax
	imulq -88(%rbp)
	movq %rax, -96(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -96(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -104(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -112(%rbp)
	movq -104(%rbp), %rax
	cqto
	idivq -112(%rbp)
	movq %rax, -120(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -120(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -128(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -136(%rbp)
	movq -128(%rbp), %rax
	cqto
	idivq -136(%rbp)
	movq %rax, -144(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -144(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -152(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -160(%rbp)
	movq -152(%rbp), %rax
	cqto
	idivq -160(%rbp)
	movq %rdx, -168(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -168(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -176(%rbp)
	movq -176(%rbp), %r11
	negq %r11
	movq %r11, -184(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -184(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -192(%rbp)
	movq -192(%rbp), %r11
	negq %r11
	movq %r11, -200(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -208(%rbp)
	movq -200(%rbp), %rax
	cqto
	idivq -208(%rbp)
	movq %rax, -216(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -216(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -224(%rbp)
	movq -224(%rbp), %r11
	negq %r11
	movq %r11, -232(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -240(%rbp)
	movq -232(%rbp), %rax
	cqto
	idivq -240(%rbp)
	movq %rdx, -248(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -248(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq %rbp, %rsp
	popq %rbp
	xorq %rax, %rax
	retq
