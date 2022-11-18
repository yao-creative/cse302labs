

	.globl main
	.text
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $16, %rsp
	/*   %2 = const 0 [TAC] */
	movq $0, -8(%rbp)
	/*   jmp %.L1 [TAC] */
	jmp .main.L1
	/*  %.L0: [TAC] */
.main.L0:
	/*   %2 = const 1 [TAC] */
	movq $1, -8(%rbp)
	/*  %.L1: [TAC] */
.main.L1:
	/*   %1 = copy %2 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -16(%rbp)
	movq -16(%rbp), %rdi
	callq __bx_print_bool
	xorq %rax, %rax
	jmp .main.Lexit
.main.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq
