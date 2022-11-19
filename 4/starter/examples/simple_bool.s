

	.globl main
	.text
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $16, %rsp
	/*  %.Lentry: [TAC] */
.main.Lentry:
	/*   %2 = const 0 [TAC] */
	movq $0, -8(%rbp)
	/*   %1 = copy %2 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -16(%rbp)
	movq -16(%rbp), %rdi
	/*   call @__bx_print_bool [TAC] */
	callq __bx_print_bool
	xorq %rax, %rax
	jmp .main.Lexit
.main.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq
