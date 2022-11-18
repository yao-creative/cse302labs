

	.globl print_42
	.text
print_42:
	pushq %rbp
	movq %rsp, %rbp
	subq $16, %rsp
	/*   %0 = const 42 [TAC] */
	movq $42, -8(%rbp)
	movq -8(%rbp), %rdi
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
	/*   %3 = copy %0 [TAC] */
	movq %rdi, %r11
	movq %r11, -16(%rbp)
	/*   %4 = copy %0 [TAC] */
	movq %rdi, %r11
	movq %r11, -24(%rbp)
	/*   %1 = add %3, %4 [TAC] */
	movq -16(%rbp), %r11
	addq -24(%rbp), %r11
	movq %r11, -32(%rbp)
	movq -32(%rbp), %rdi
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
	/*   %3 = copy %0 [TAC] */
	movq %rdi, %r11
	movq %r11, -24(%rbp)
	/*   %4 = copy %1 [TAC] */
	movq %rsi, %r11
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
	/*   %3 = copy %0 [TAC] */
	movq %rdi, %r11
	movq %r11, -24(%rbp)
	/*   %4 = copy %1 [TAC] */
	movq %rsi, %r11
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
	subq $32, %rsp
	callq print_42
	/*   %1 = const 4 [TAC] */
	movq $4, -8(%rbp)
	movq -8(%rbp), %rdi
	callq print_double
	/*   %3 = const 4 [TAC] */
	movq $4, -16(%rbp)
	movq -16(%rbp), %rdi
	/*   %3 = const 5 [TAC] */
	movq $5, -16(%rbp)
	movq -16(%rbp), %rsi
	/*   %3 = call @sum, 2 [TAC] */
	callq sum
	movq -24(%rbp), %rdi
	callq __bx_print_int
	/*   %7 = const 4 [TAC] */
	movq $4, -32(%rbp)
	movq -32(%rbp), %rdi
	/*   %7 = const 5 [TAC] */
	movq $5, -32(%rbp)
	movq -32(%rbp), %rsi
	/*   %7 = call @sum_, 2 [TAC] */
	callq sum_
	movq -32(%rbp), %rdi
	callq __bx_print_int
	xorq %rax, %rax
	jmp .main.Lexit
.main.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq
