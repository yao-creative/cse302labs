

	.globl sum7
	.text
sum7:
	pushq %rbp
	movq %rsp, %rbp
	subq $240, %rsp
	movq %rdi, -8(%rbp)
	movq %rsi, -16(%rbp)
	movq %rdx, -24(%rbp)
	movq %rcx, -32(%rbp)
	movq %r8, -40(%rbp)
	movq %r9, -48(%rbp)
	movq 16(%rbp), %r11
	movq %r11, -56(%rbp)
	movq 24(%rbp), %r11
	movq %r11, -64(%rbp)
	movq 32(%rbp), %r11
	movq %r11, -72(%rbp)
	movq 40(%rbp), %r11
	movq %r11, -80(%rbp)
	/*  %.Lentry: [TAC] */
.sum7.Lentry:
	/*   %11 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -88(%rbp)
	/*   %13 = copy %1 [TAC] */
	movq -16(%rbp), %r11
	movq %r11, -96(%rbp)
	/*   %15 = copy %2 [TAC] */
	movq -24(%rbp), %r11
	movq %r11, -104(%rbp)
	/*   %17 = copy %3 [TAC] */
	movq -32(%rbp), %r11
	movq %r11, -112(%rbp)
	/*   %19 = copy %4 [TAC] */
	movq -40(%rbp), %r11
	movq %r11, -120(%rbp)
	/*   %21 = copy %5 [TAC] */
	movq -48(%rbp), %r11
	movq %r11, -128(%rbp)
	/*   %23 = copy %6 [TAC] */
	movq -56(%rbp), %r11
	movq %r11, -136(%rbp)
	/*   %25 = copy %7 [TAC] */
	movq -64(%rbp), %r11
	movq %r11, -144(%rbp)
	/*   %27 = copy %8 [TAC] */
	movq -72(%rbp), %r11
	movq %r11, -152(%rbp)
	/*   %28 = copy %9 [TAC] */
	movq -80(%rbp), %r11
	movq %r11, -160(%rbp)
	/*   %26 = add %27, %28 [TAC] */
	movq -152(%rbp), %r11
	addq -160(%rbp), %r11
	movq %r11, -168(%rbp)
	/*   %24 = add %25, %26 [TAC] */
	movq -144(%rbp), %r11
	addq -168(%rbp), %r11
	movq %r11, -176(%rbp)
	/*   %22 = add %23, %24 [TAC] */
	movq -136(%rbp), %r11
	addq -176(%rbp), %r11
	movq %r11, -184(%rbp)
	/*   %20 = add %21, %22 [TAC] */
	movq -128(%rbp), %r11
	addq -184(%rbp), %r11
	movq %r11, -192(%rbp)
	/*   %18 = add %19, %20 [TAC] */
	movq -120(%rbp), %r11
	addq -192(%rbp), %r11
	movq %r11, -200(%rbp)
	/*   %16 = add %17, %18 [TAC] */
	movq -112(%rbp), %r11
	addq -200(%rbp), %r11
	movq %r11, -208(%rbp)
	/*   %14 = add %15, %16 [TAC] */
	movq -104(%rbp), %r11
	addq -208(%rbp), %r11
	movq %r11, -216(%rbp)
	/*   %12 = add %13, %14 [TAC] */
	movq -96(%rbp), %r11
	addq -216(%rbp), %r11
	movq %r11, -224(%rbp)
	/*   %10 = add %11, %12 [TAC] */
	movq -88(%rbp), %r11
	addq -224(%rbp), %r11
	movq %r11, -232(%rbp)
	movq -232(%rbp), %rax
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
	subq $96, %rsp
	/*  %.Lentry: [TAC] */
.main.Lentry:
	/*   %0 = const 0 [TAC] */
	movq $0, -8(%rbp)
	/*   %3 = const 1 [TAC] */
	movq $1, -16(%rbp)
	movq -16(%rbp), %rdi
	/*   %4 = const 1 [TAC] */
	movq $1, -24(%rbp)
	movq -24(%rbp), %rsi
	/*   %5 = const 1 [TAC] */
	movq $1, -32(%rbp)
	movq -32(%rbp), %rdx
	/*   %6 = const 1 [TAC] */
	movq $1, -40(%rbp)
	movq -40(%rbp), %rcx
	/*   %7 = const 1 [TAC] */
	movq $1, -48(%rbp)
	movq -48(%rbp), %r8
	/*   %8 = const 1 [TAC] */
	movq $1, -56(%rbp)
	movq -56(%rbp), %r9
	/*   %9 = const 1 [TAC] */
	movq $1, -64(%rbp)
	/*   %10 = const 1 [TAC] */
	movq $1, -72(%rbp)
	/*   %11 = const 1 [TAC] */
	movq $1, -80(%rbp)
	/*   %12 = const 1 [TAC] */
	movq $1, -88(%rbp)
	/*   %2 = call @sum7, 10 [TAC] */
	pushq -88(%rbp)
	pushq -80(%rbp)
	pushq -72(%rbp)
	pushq -64(%rbp)
	callq sum7
	addq $32, %rsp
	movq %rax, -96(%rbp)
	movq -96(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	xorq %rax, %rax
	jmp .main.Lexit
.main.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq
