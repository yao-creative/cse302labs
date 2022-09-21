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
	movq $10, -8(%rbp)
	movq $2, -24(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	movq -24(%rbp), %rax
	imulq -32(%rbp)
	movq %rax, -16(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -40(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -48(%rbp)
	movq -40(%rbp), %rax
	imulq -48(%rbp)
	movq %rax, -56(%rbp)
	movq $2, -64(%rbp)
	movq -56(%rbp), %rax
	cqto
	idivq -64(%rbp)
	movq %rax, -8(%rbp)
	movq %rbp, %rsp
	popq %rbp
	xorq %rax, %rax
	retq
