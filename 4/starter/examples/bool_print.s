

	.globl main
	.text
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $144, %rsp
	/*  %.Lentry: [TAC] */
.main.Lentry:
	/*   %2 = const 0 [TAC] */
	movq $0, -8(%rbp)
	/*   %2 = const 1 [TAC] */
	movq $1, -8(%rbp)
	/*   %1 = copy %2 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -16(%rbp)
	movq -16(%rbp), %rdi
	/*   call @__bx_print_bool [TAC] */
	callq __bx_print_bool
	/*   %5 = const 0 [TAC] */
	movq $0, -24(%rbp)
	/*   %5 = const 1 [TAC] */
	movq $1, -24(%rbp)
	/*   %4 = copy %5 [TAC] */
	movq -24(%rbp), %r11
	movq %r11, -32(%rbp)
	movq -32(%rbp), %rdi
	/*   call @__bx_print_bool [TAC] */
	callq __bx_print_bool
	/*   %8 = const 0 [TAC] */
	movq $0, -40(%rbp)
	/*   %8 = const 1 [TAC] */
	movq $1, -40(%rbp)
	/*   %7 = copy %8 [TAC] */
	movq -40(%rbp), %r11
	movq %r11, -48(%rbp)
	movq -48(%rbp), %rdi
	/*   call @__bx_print_bool [TAC] */
	callq __bx_print_bool
	/*   %11 = const 0 [TAC] */
	movq $0, -56(%rbp)
	/*   %11 = const 1 [TAC] */
	movq $1, -56(%rbp)
	/*   %10 = copy %11 [TAC] */
	movq -56(%rbp), %r11
	movq %r11, -64(%rbp)
	movq -64(%rbp), %rdi
	/*   call @__bx_print_bool [TAC] */
	callq __bx_print_bool
	/*   %14 = const 0 [TAC] */
	movq $0, -72(%rbp)
	/*   %13 = copy %14 [TAC] */
	movq -72(%rbp), %r11
	movq %r11, -80(%rbp)
	movq -80(%rbp), %rdi
	/*   call @__bx_print_bool [TAC] */
	callq __bx_print_bool
	/*   %17 = const 0 [TAC] */
	movq $0, -88(%rbp)
	/*   %16 = copy %17 [TAC] */
	movq -88(%rbp), %r11
	movq %r11, -96(%rbp)
	movq -96(%rbp), %rdi
	/*   call @__bx_print_bool [TAC] */
	callq __bx_print_bool
	/*   %20 = const 0 [TAC] */
	movq $0, -104(%rbp)
	/*   %19 = copy %20 [TAC] */
	movq -104(%rbp), %r11
	movq %r11, -112(%rbp)
	movq -112(%rbp), %rdi
	/*   call @__bx_print_bool [TAC] */
	callq __bx_print_bool
	/*   %23 = const 0 [TAC] */
	movq $0, -120(%rbp)
	/*   %22 = copy %23 [TAC] */
	movq -120(%rbp), %r11
	movq %r11, -128(%rbp)
	movq -128(%rbp), %rdi
	/*   call @__bx_print_bool [TAC] */
	callq __bx_print_bool
	/*   %26 = const 0 [TAC] */
	movq $0, -136(%rbp)
	/*   %25 = copy %26 [TAC] */
	movq -136(%rbp), %r11
	movq %r11, -144(%rbp)
	movq -144(%rbp), %rdi
	/*   call @__bx_print_bool [TAC] */
	callq __bx_print_bool
	xorq %rax, %rax
	jmp .main.Lexit
.main.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq
