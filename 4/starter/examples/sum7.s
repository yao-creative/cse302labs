

	.globl sum7
	.text
sum7:
	pushq %rbp
	movq %rsp, %rbp
	subq $160, %rsp
	movq %rdi, -8(%rbp)
	movq %rsi, -16(%rbp)
	movq %rdx, -24(%rbp)
	movq %rcx, -32(%rbp)
	movq %r8, -40(%rbp)
	movq %r9, -48(%rbp)
	movq 16(%rbp), %r11
	movq %r11, -56(%rbp)
	/*  %.Lentry: [TAC] */
.sum7.Lentry:
	/*   %13 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -64(%rbp)
	/*   %14 = copy %1 [TAC] */
	movq -16(%rbp), %r11
	movq %r11, -72(%rbp)
	/*   %12 = add %13, %14 [TAC] */
	movq -64(%rbp), %r11
	addq -72(%rbp), %r11
	movq %r11, -80(%rbp)
	/*   %15 = copy %2 [TAC] */
	movq -24(%rbp), %r11
	movq %r11, -88(%rbp)
	/*   %11 = add %12, %15 [TAC] */
	movq -80(%rbp), %r11
	addq -88(%rbp), %r11
	movq %r11, -96(%rbp)
	/*   %16 = copy %3 [TAC] */
	movq -32(%rbp), %r11
	movq %r11, -104(%rbp)
	/*   %10 = add %11, %16 [TAC] */
	movq -96(%rbp), %r11
	addq -104(%rbp), %r11
	movq %r11, -112(%rbp)
	/*   %17 = copy %4 [TAC] */
	movq -40(%rbp), %r11
	movq %r11, -120(%rbp)
	/*   %9 = add %10, %17 [TAC] */
	movq -112(%rbp), %r11
	addq -120(%rbp), %r11
	movq %r11, -128(%rbp)
	/*   %18 = copy %5 [TAC] */
	movq -48(%rbp), %r11
	movq %r11, -136(%rbp)
	/*   %8 = add %9, %18 [TAC] */
	movq -128(%rbp), %r11
	addq -136(%rbp), %r11
	movq %r11, -144(%rbp)
	/*   %19 = copy %6 [TAC] */
	movq -56(%rbp), %r11
	movq %r11, -152(%rbp)
	/*   %7 = add %8, %19 [TAC] */
	movq -144(%rbp), %r11
	addq -152(%rbp), %r11
	movq %r11, -160(%rbp)
	movq -160(%rbp), %rax
	jmp .sum7.Lexit
.sum7.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq



	.globl main
	.text
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $80, %rsp
	/*  %.Lentry: [TAC] */
.main.Lentry:
	/*   %0 = const 0 [TAC] */
	movq $0, -8(%rbp)
	/*   %1 = const 1 [TAC] */
	movq $1, -16(%rbp)
	movq -16(%rbp), %rdi
	/*   %2 = const 1 [TAC] */
	movq $1, -24(%rbp)
	movq -24(%rbp), %rsi
	/*   %3 = const 1 [TAC] */
	movq $1, -32(%rbp)
	movq -32(%rbp), %rdx
	/*   %4 = const 1 [TAC] */
	movq $1, -40(%rbp)
	movq -40(%rbp), %rcx
	/*   %5 = const 1 [TAC] */
	movq $1, -48(%rbp)
	movq -48(%rbp), %r8
	/*   %6 = const 1 [TAC] */
	movq $1, -56(%rbp)
	movq -56(%rbp), %r9
	/*   %7 = const 1 [TAC] */
	movq $1, -64(%rbp)
	/*   %0 = call @sum7, 7 [TAC] */
	pushq $0
	pushq -64(%rbp)
	callq sum7
	addq $8, %rsp
	movq %rax, -8(%rbp)
	/*   %9 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -72(%rbp)
	movq -72(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	xorq %rax, %rax
	jmp .main.Lexit
.main.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq
