	.section .rodata
.lprintfmt:
	.string "%ld\n"
	.text
	.globl main
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $208, %rsp
	movq $0, -8(%rbp)
	movq $0, -16(%rbp)
	movq $0, -24(%rbp)
	movq $10, -8(%rbp)
	movq $42, -16(%rbp)
	movq $100, -32(%rbp)
	movq -32(%rbp), %r11
	negq %r11
	movq %r11, -24(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -40(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -48(%rbp)
	movq -40(%rbp), %r11
	andq -48(%rbp), %r11
	movq %r11, -56(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -56(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -64(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -72(%rbp)
	movq -64(%rbp), %r11
	andq -72(%rbp), %r11
	movq %r11, -80(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -80(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -88(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -96(%rbp)
	movq -88(%rbp), %r11
	orq -96(%rbp), %r11
	movq %r11, -104(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -104(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -112(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -120(%rbp)
	movq -112(%rbp), %r11
	orq -120(%rbp), %r11
	movq %r11, -128(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -128(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -136(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -144(%rbp)
	movq -136(%rbp), %r11
	xorq -144(%rbp), %r11
	movq %r11, -152(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -152(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -160(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -168(%rbp)
	movq -160(%rbp), %r11
	xorq -168(%rbp), %r11
	movq %r11, -176(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -176(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -184(%rbp)
	movq -184(%rbp), %r11
	notq %r11
	movq %r11, -192(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -192(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -24(%rbp), %r11
	movq %r11, -200(%rbp)
	movq -200(%rbp), %r11
	notq %r11
	movq %r11, -208(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -208(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq %rbp, %rsp
	popq %rbp
	xorq %rax, %rax
	retq
