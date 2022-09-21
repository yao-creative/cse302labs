	.section .rodata
.lprintfmt:
	.string "%ld\n"
	.text
	.globl main
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $272, %rsp
	movq $0, -8(%rbp)
	movq $0, -16(%rbp)
	movq $0, -24(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -40(%rbp)
	movq -32(%rbp), %r11
	addq -40(%rbp), %r11
	movq %r11, -8(%rbp)
	movq $42, -8(%rbp)
	movq $21, -16(%rbp)
	movq $5, -24(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -48(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -56(%rbp)
	movq -48(%rbp), %r11
	addq -56(%rbp), %r11
	movq %r11, -64(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -64(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -72(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -80(%rbp)
	movq -72(%rbp), %r11
	subq -80(%rbp), %r11
	movq %r11, -88(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -88(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -96(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -104(%rbp)
	movq -96(%rbp), %rax
	imulq -104(%rbp)
	movq %rax, -112(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -112(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -120(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -128(%rbp)
	movq -120(%rbp), %rax
	cqto
	idivq -128(%rbp)
	movq %rax, -136(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -136(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -144(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -152(%rbp)
	movq -144(%rbp), %rax
	cqto
	idivq -152(%rbp)
	movq %rax, -160(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -160(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -168(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -176(%rbp)
	movq -168(%rbp), %rax
	cqto
	idivq -176(%rbp)
	movq %rdx, -184(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -184(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -192(%rbp)
	movq -192(%rbp), %r11
	negq %r11
	movq %r11, -200(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -200(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -208(%rbp)
	movq -208(%rbp), %r11
	negq %r11
	movq %r11, -216(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -224(%rbp)
	movq -208(%rbp), %rax
	cqto
	idivq -224(%rbp)
	movq %rax, -232(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -232(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -240(%rbp)
	movq -240(%rbp), %r11
	negq %r11
	movq %r11, -248(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -256(%rbp)
	movq -240(%rbp), %rax
	cqto
	idivq -256(%rbp)
	movq %rdx, -264(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -264(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq %rbp, %rsp
	popq %rbp
	xorq %rax, %rax
	retq
