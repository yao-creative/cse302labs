	.section .rodata
.lprintfmt:
	.string "%ld\n"
	.text
	.globl main
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $128, %rsp
	movq $0, -8(%rbp)
	movq $0, -16(%rbp)
	movq $0, -24(%rbp)
	movq $10, -32(%rbp)
	movq -32(%rbp), %r11
	movq %r11, -8(%rbp)
	movq $42, -40(%rbp)
	movq -40(%rbp), %r11
	movq %r11, -16(%rbp)
	movq $100, -48(%rbp)
	movq -48(%rbp), %r11
	negq %r11
	movq %r11, -56(%rbp)
	movq -56(%rbp), %r11
	movq %r11, -24(%rbp)
	movq -8(%rbp), %r11
	andq -16(%rbp), %r11
	movq %r11, -64(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -64(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	andq -24(%rbp), %r11
	movq %r11, -72(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -72(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	orq -16(%rbp), %r11
	movq %r11, -80(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -80(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	orq -24(%rbp), %r11
	movq %r11, -88(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -88(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	xorq -16(%rbp), %r11
	movq %r11, -96(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -96(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	xorq -24(%rbp), %r11
	movq %r11, -104(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -104(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	notq %r11
	movq %r11, -112(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -112(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -24(%rbp), %r11
	notq %r11
	movq %r11, -120(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -120(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq %rbp, %rsp
	popq %rbp
	xorq %rax, %rax
	retq
