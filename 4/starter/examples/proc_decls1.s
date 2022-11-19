

	.globl print_42
	.text
print_42:
	pushq %rbp
	movq %rsp, %rbp
	subq $16, %rsp
	/*  %.Lentry: [TAC] */
.print_42.Lentry:
	/*   %1 = const 42 [TAC] */
	movq $42, -8(%rbp)
	movq -8(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	xorq %rax, %rax
	jmp .print_42.Lexit
.print_42.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq



	.globl print_double
	.text
print_double:
	pushq %rbp
	movq %rsp, %rbp
	subq $32, %rsp
	movq %rdi, -8(%rbp)
	/*  %.Lentry: [TAC] */
.print_double.Lentry:
	/*   %3 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -16(%rbp)
	/*   %4 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -24(%rbp)
	/*   %2 = add %3, %4 [TAC] */
	movq -16(%rbp), %r11
	addq -24(%rbp), %r11
	movq %r11, -32(%rbp)
	movq -32(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	xorq %rax, %rax
	jmp .print_double.Lexit
.print_double.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq



	.globl sum
	.text
sum:
	pushq %rbp
	movq %rsp, %rbp
	subq $48, %rsp
	movq %rdi, -8(%rbp)
	movq %rsi, -16(%rbp)
	/*  %.Lentry: [TAC] */
.sum.Lentry:
	/*   %3 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -24(%rbp)
	/*   %4 = copy %1 [TAC] */
	movq -16(%rbp), %r11
	movq %r11, -32(%rbp)
	/*   %2 = add %3, %4 [TAC] */
	movq -24(%rbp), %r11
	addq -32(%rbp), %r11
	movq %r11, -40(%rbp)
	movq -40(%rbp), %rax
	jmp .sum.Lexit
.sum.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq



	.globl sum_
	.text
sum_:
	pushq %rbp
	movq %rsp, %rbp
	subq $48, %rsp
	movq %rdi, -8(%rbp)
	movq %rsi, -16(%rbp)
	/*  %.Lentry: [TAC] */
.sum_.Lentry:
	/*   %3 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -24(%rbp)
	/*   %4 = copy %1 [TAC] */
	movq -16(%rbp), %r11
	movq %r11, -32(%rbp)
	/*   %2 = add %3, %4 [TAC] */
	movq -24(%rbp), %r11
	addq -32(%rbp), %r11
	movq %r11, -40(%rbp)
	movq -40(%rbp), %rax
	jmp .sum_.Lexit
.sum_.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq



	.globl main
	.text
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $64, %rsp
	/*  %.Lentry: [TAC] */
.main.Lentry:
	/*   call @print_42 [TAC] */
	callq print_42
	/*   %2 = const 4 [TAC] */
	movq $4, -8(%rbp)
	movq -8(%rbp), %rdi
	/*   call @print_double [TAC] */
	callq print_double
	/*   %4 = const 4 [TAC] */
	movq $4, -16(%rbp)
	movq -16(%rbp), %rdi
	/*   %5 = const 5 [TAC] */
	movq $5, -24(%rbp)
	movq -24(%rbp), %rsi
	/*   %3 = call @sum, 2 [TAC] */
	callq sum
	movq %rax, -32(%rbp)
	/*   %7 = copy %3 [TAC] */
	movq -32(%rbp), %r11
	movq %r11, -40(%rbp)
	movq -40(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	/*   %10 = const 4 [TAC] */
	movq $4, -48(%rbp)
	movq -48(%rbp), %rdi
	/*   %11 = const 5 [TAC] */
	movq $5, -56(%rbp)
	movq -56(%rbp), %rsi
	/*   %9 = call @sum_, 2 [TAC] */
	callq sum_
	movq %rax, -64(%rbp)
	movq -64(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	xorq %rax, %rax
	jmp .main.Lexit
.main.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq
