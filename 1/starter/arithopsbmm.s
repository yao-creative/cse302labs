	.section .rodata
.lprintfmt:
	.string "%ld\n"
	.text
	.globl main
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $144, %rsp
	movq $0, -8(%rbp)
	movq $0, -16(%rbp)
	movq $0, -24(%rbp)
	movq -8(%rbp), %r11
	addq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	movq -32(%rbp), %r11
	movq %r11, -8(%rbp)
	movq $42, -40(%rbp)
	movq -40(%rbp), %r11
	movq %r11, -8(%rbp)
	movq $21, -48(%rbp)
	movq -48(%rbp), %r11
	movq %r11, -16(%rbp)
	movq $5, -56(%rbp)
	movq -56(%rbp), %r11
	movq %r11, -24(%rbp)
	movq -8(%rbp), %r11
	addq -16(%rbp), %r11
	movq %r11, -64(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -64(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	subq -16(%rbp), %r11
	movq %r11, -72(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -72(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %rax
	imulq -16(%rbp)
	movq %rax, -80(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -80(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %rax
	cqto
	idivq -16(%rbp)
	movq %rax, -88(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -88(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %rax
	cqto
	idivq -24(%rbp)
	movq %rax, -96(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -96(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %rax
	cqto
	idivq -24(%rbp)
	movq %rdx, -104(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -104(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	negq %r11
	movq %r11, -112(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -112(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	negq %r11
	movq %r11, -120(%rbp)
	movq -120(%rbp), %rax
	cqto
	idivq -24(%rbp)
	movq %rax, -128(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -128(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	negq %r11
	movq %r11, -136(%rbp)
	movq -136(%rbp), %rax
	cqto
	idivq -24(%rbp)
	movq %rdx, -144(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -144(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq %rbp, %rsp
	popq %rbp
	xorq %rax, %rax
	retq
