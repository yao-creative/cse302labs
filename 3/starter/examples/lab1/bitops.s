	.text
	.globl main
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $208, %rsp
	/*   %0 = const 0 [TAC] */
	movq $0, -8(%rbp)
	/*   %1 = const 0 [TAC] */
	movq $0, -16(%rbp)
	/*   %2 = const 0 [TAC] */
	movq $0, -24(%rbp)
	/*   %0 = const 10 [TAC] */
	movq $10, -8(%rbp)
	/*   %1 = const 42 [TAC] */
	movq $42, -16(%rbp)
	/*   %3 = const 100 [TAC] */
	movq $100, -32(%rbp)
	/*   %2 = neg %3 [TAC] */
	movq -32(%rbp), %r11
	negq %r11
	movq %r11, -24(%rbp)
	/*   %5 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -40(%rbp)
	/*   %6 = copy %1 [TAC] */
	movq -16(%rbp), %r11
	movq %r11, -48(%rbp)
	/*   %4 = and %5, %6 [TAC] */
	movq -40(%rbp), %r11
	andq -48(%rbp), %r11
	movq %r11, -56(%rbp)
	/*   print %4 [TAC] */
	movq -56(%rbp), %rdi
	callq bx_print_int
	/*   %8 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -64(%rbp)
	/*   %9 = copy %2 [TAC] */
	movq -24(%rbp), %r11
	movq %r11, -72(%rbp)
	/*   %7 = and %8, %9 [TAC] */
	movq -64(%rbp), %r11
	andq -72(%rbp), %r11
	movq %r11, -80(%rbp)
	/*   print %7 [TAC] */
	movq -80(%rbp), %rdi
	callq bx_print_int
	/*   %11 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -88(%rbp)
	/*   %12 = copy %1 [TAC] */
	movq -16(%rbp), %r11
	movq %r11, -96(%rbp)
	/*   %10 = or %11, %12 [TAC] */
	movq -88(%rbp), %r11
	orq -96(%rbp), %r11
	movq %r11, -104(%rbp)
	/*   print %10 [TAC] */
	movq -104(%rbp), %rdi
	callq bx_print_int
	/*   %14 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -112(%rbp)
	/*   %15 = copy %2 [TAC] */
	movq -24(%rbp), %r11
	movq %r11, -120(%rbp)
	/*   %13 = or %14, %15 [TAC] */
	movq -112(%rbp), %r11
	orq -120(%rbp), %r11
	movq %r11, -128(%rbp)
	/*   print %13 [TAC] */
	movq -128(%rbp), %rdi
	callq bx_print_int
	/*   %17 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -136(%rbp)
	/*   %18 = copy %1 [TAC] */
	movq -16(%rbp), %r11
	movq %r11, -144(%rbp)
	/*   %16 = xor %17, %18 [TAC] */
	movq -136(%rbp), %r11
	xorq -144(%rbp), %r11
	movq %r11, -152(%rbp)
	/*   print %16 [TAC] */
	movq -152(%rbp), %rdi
	callq bx_print_int
	/*   %20 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -160(%rbp)
	/*   %21 = copy %2 [TAC] */
	movq -24(%rbp), %r11
	movq %r11, -168(%rbp)
	/*   %19 = xor %20, %21 [TAC] */
	movq -160(%rbp), %r11
	xorq -168(%rbp), %r11
	movq %r11, -176(%rbp)
	/*   print %19 [TAC] */
	movq -176(%rbp), %rdi
	callq bx_print_int
	/*   %23 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -184(%rbp)
	/*   %22 = not %23 [TAC] */
	movq -184(%rbp), %r11
	notq %r11
	movq %r11, -192(%rbp)
	/*   print %22 [TAC] */
	movq -192(%rbp), %rdi
	callq bx_print_int
	/*   %25 = copy %2 [TAC] */
	movq -24(%rbp), %r11
	movq %r11, -200(%rbp)
	/*   %24 = not %25 [TAC] */
	movq -200(%rbp), %r11
	notq %r11
	movq %r11, -208(%rbp)
	/*   print %24 [TAC] */
	movq -208(%rbp), %rdi
	callq bx_print_int
	movq %rbp, %rsp
	popq %rbp
	movq $0, %rax
	retq
