

	.globl sum7
	.text
sum7:
	pushq %rbp
	movq %rsp, %rbp
	subq $160, %rsp
	/*  %.Lentry: [TAC] */
.sum7.Lentry:
	/*   %8 = copy %0 [TAC] */
	movq %rdi, %r11
	movq %r11, -64(%rbp)
	/*   %10 = copy %1 [TAC] */
	movq %rsi, %r11
	movq %r11, -72(%rbp)
	/*   %12 = copy %2 [TAC] */
	movq %rdx, %r11
	movq %r11, -80(%rbp)
	/*   %14 = copy %3 [TAC] */
	movq %rcx, %r11
	movq %r11, -88(%rbp)
	/*   %16 = copy %4 [TAC] */
	movq %r8, %r11
	movq %r11, -96(%rbp)
	/*   %18 = copy %5 [TAC] */
	movq %r9, %r11
	movq %r11, -104(%rbp)
	/*   %19 = copy %6 [TAC] */
	movq 16(%rbp), %r11
	movq %r11, -112(%rbp)
	/*   %17 = add %18, %19 [TAC] */
	movq -104(%rbp), %r11
	addq -112(%rbp), %r11
	movq %r11, -120(%rbp)
	/*   %15 = add %16, %17 [TAC] */
	movq -96(%rbp), %r11
	addq -120(%rbp), %r11
	movq %r11, -128(%rbp)
	/*   %13 = add %14, %15 [TAC] */
	movq -88(%rbp), %r11
	addq -128(%rbp), %r11
	movq %r11, -136(%rbp)
	/*   %11 = add %12, %13 [TAC] */
	movq -80(%rbp), %r11
	addq -136(%rbp), %r11
	movq %r11, -144(%rbp)
	/*   %9 = add %10, %11 [TAC] */
	movq -72(%rbp), %r11
	addq -144(%rbp), %r11
	movq %r11, -152(%rbp)
	/*   %7 = add %8, %9 [TAC] */
	movq -64(%rbp), %r11
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
