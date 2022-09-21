	.section .rodata
.lprintfmt:
	.string "%ld\n"
	.text
	.globl main
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $64, %rsp
	movq $0, -8(%rbp)
	movq $0, -16(%rbp)
	movq $10, -24(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -8(%rbp)
	movq $2, -32(%rbp)
	movq -32(%rbp), %rax
	imulq -8(%rbp)
	movq %rax, -40(%rbp)
	movq -40(%rbp), %r11
	movq %r11, -16(%rbp)
	movq -16(%rbp), %rax
	imulq -16(%rbp)
	movq %rax, -48(%rbp)
	movq $2, -56(%rbp)
	movq -48(%rbp), %rax
	cqto
	idivq -56(%rbp)
	movq %rax, -64(%rbp)
	movq -64(%rbp), %r11
	movq %r11, -8(%rbp)
	movq %rbp, %rsp
	popq %rbp
	xorq %rax, %rax
	retq
