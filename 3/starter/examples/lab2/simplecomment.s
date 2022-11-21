	.text
	.globl main
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $16, %rsp
	/*   %0 = const 42 [TAC] */
	movq $42, -8(%rbp)
	/*   print %0 [TAC] */
	movq -8(%rbp), %rdi
	callq bx_print_int
	movq %rbp, %rsp
	popq %rbp
	movq $0, %rax
	retq
