	.section .rodata
.lprintfmt:
	.string "%ld\n"
	.text
	.globl main
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $160, %rsp
	movq $0, -8(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -16(%rbp)
	movq $0, -24(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -32(%rbp)
	movq $0, -40(%rbp)
	movq -40(%rbp), %r11
	movq %r11, -48(%rbp)
	movq $42, -56(%rbp)
	movq -56(%rbp), %r11
	movq %r11, -16(%rbp)
	movq $21, -64(%rbp)
	movq -64(%rbp), %r11
	movq %r11, -32(%rbp)
	movq $5, -72(%rbp)
	movq -72(%rbp), %r11
	movq %r11, -48(%rbp)
	movq -16(%rbp), %r11
	addq -32(%rbp), %r11
	movq %r11, -80(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -80(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -16(%rbp), %r11
	subq -32(%rbp), %r11
	movq %r11, -88(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -88(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -16(%rbp), %rax
	imulq -32(%rbp)
	movq %rax, -96(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -96(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -16(%rbp), %rax
	cqto
	idivq -32(%rbp)
	movq %rax, -104(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -104(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -16(%rbp), %rax
	cqto
	idivq -48(%rbp)
	movq %rax, -112(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -112(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -16(%rbp), %rax
	cqto
	idivq -48(%rbp)
	movq %rdx, -120(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -120(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -16(%rbp), %r11
	negq %r11
	movq %r11, -128(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -128(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -16(%rbp), %r11
	negq %r11
	movq %r11, -136(%rbp)
	movq -136(%rbp), %rax
	cqto
	idivq -48(%rbp)
	movq %rax, -144(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -144(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -16(%rbp), %r11
	negq %r11
	movq %r11, -152(%rbp)
	movq -152(%rbp), %rax
	cqto
	idivq -48(%rbp)
	movq %rdx, -160(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -160(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq %rbp, %rsp
	popq %rbp
	xorq %rax, %rax
	retq
