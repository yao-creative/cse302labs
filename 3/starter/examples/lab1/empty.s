	.text
	.globl main
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $0, %rsp
	movq %rbp, %rsp
	popq %rbp
	movq $0, %rax
	retq
