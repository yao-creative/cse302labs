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
	movq -8(%rbp), %r11
	movq %r11, -16(%rbp)
	movq $0, -24(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -32(%rbp)
	movq $0, -40(%rbp)
	movq -40(%rbp), %r11
	movq %r11, -48(%rbp)
	movq $10, -56(%rbp)
	movq -56(%rbp), %r11
	movq %r11, -16(%rbp)
	movq $42, -64(%rbp)
	movq -64(%rbp), %r11
	movq %r11, -32(%rbp)
	movq $100, -72(%rbp)
	movq -72(%rbp), %r11
	negq %r11
	movq %r11, -80(%rbp)
	movq -80(%rbp), %r11
	movq %r11, -48(%rbp)
	movq -16(%rbp), %r11
	andq -32(%rbp), %r11
	movq %r11, -88(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -88(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -16(%rbp), %r11
	andq -48(%rbp), %r11
	movq %r11, -96(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -96(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -16(%rbp), %r11
	orq -32(%rbp), %r11
	movq %r11, -104(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -104(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -16(%rbp), %r11
	orq -48(%rbp), %r11
	movq %r11, -112(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -112(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -16(%rbp), %r11
	xorq -32(%rbp), %r11
	movq %r11, -120(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -120(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -16(%rbp), %r11
	xorq -48(%rbp), %r11
	movq %r11, -128(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -128(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -16(%rbp), %r11
	notq %r11
	movq %r11, -136(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -136(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -48(%rbp), %r11
	notq %r11
	movq %r11, -144(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -144(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq %rbp, %rsp
	popq %rbp
	xorq %rax, %rax
	retq
