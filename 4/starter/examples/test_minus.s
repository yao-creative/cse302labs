	.globl a
	.data
a:  .quad -42


	.globl iden
	.text
iden:
	pushq %rbp
	movq %rsp, %rbp
	subq $32, %rsp
	movq %rdi, -8(%rbp)
	/*  %.Lentry: [TAC] */
.iden.Lentry:
	/*   %3 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -16(%rbp)
	/*   %2 = neg %3 [TAC] */
	movq -16(%rbp), %r11
	negq %r11
	movq %r11, -24(%rbp)
	/*   %1 = neg %2 [TAC] */
	movq -24(%rbp), %r11
	negq %r11
	movq %r11, -32(%rbp)
	movq -32(%rbp), %rax
	jmp .iden.Lexit
.iden.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq



	.globl main
	.text
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $32, %rsp
	/*  %.Lentry: [TAC] */
.main.Lentry:
	/*   %0 = const -42 [TAC] */
	movq $-42, -8(%rbp)
	/*   %3 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -16(%rbp)
	movq -16(%rbp), %rdi
	/*   %2 = call @iden, 1 [TAC] */
	callq iden
	movq %rax, -24(%rbp)
	movq -24(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	xorq %rax, %rax
	jmp .main.Lexit
.main.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq
