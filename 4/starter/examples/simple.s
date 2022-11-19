

	.globl main
	.text
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $16, %rsp
	/*  %.Lentry: [TAC] */
.main.Lentry:
	/*   %1 = const 42 [TAC] */
	movq $42, -8(%rbp)
	movq -8(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	xorq %rax, %rax
	jmp .main.Lexit
.main.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq
