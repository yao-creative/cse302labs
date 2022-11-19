	.globl x
	.data
x:  .quad 0
	.globl y
	.data
y:  .quad 42
	.globl b
	.data
b:  .quad 1
	.globl z
	.data
z:  .quad -42


	.globl main
	.text
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $128, %rsp
	/*  %.Lentry: [TAC] */
.main.Lentry:
	/*   %1 = const 10 [TAC] */
	movq $10, -8(%rbp)
	/*   %2 = const 20 [TAC] */
	movq $20, -16(%rbp)
	/*   %0 = add %1, %2 [TAC] */
	movq -8(%rbp), %r11
	addq -16(%rbp), %r11
	movq %r11, -24(%rbp)
	/*   %3 = const 10 [TAC] */
	movq $10, -32(%rbp)
	/*   %5 = copy %3 [TAC] */
	movq -32(%rbp), %r11
	movq %r11, -40(%rbp)
	/*   %6 = const 3 [TAC] */
	movq $3, -48(%rbp)
	/*   %4 = mul %5, %6 [TAC] */
	movq -40(%rbp), %rax
	imulq -48(%rbp)
	movq %rax, -56(%rbp)
	/*   %8 = copy %0 [TAC] */
	movq -24(%rbp), %r11
	movq %r11, -64(%rbp)
	movq -64(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	/*   %10 = copy %4 [TAC] */
	movq -56(%rbp), %r11
	movq %r11, -72(%rbp)
	movq -72(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	/*   %12 = copy %3 [TAC] */
	movq -32(%rbp), %r11
	movq %r11, -80(%rbp)
	movq -80(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	/*   %14 = copy @x [TAC] */
	movq x(%rip), %r11
	movq %r11, -88(%rbp)
	movq -88(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	/*   %16 = copy @y [TAC] */
	movq y(%rip), %r11
	movq %r11, -96(%rbp)
	movq -96(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	/*   %19 = const 0 [TAC] */
	movq $0, -104(%rbp)
	/*   jz @b, %.L1 [TAC] */
	cmpq $0, b(%rip)
	jz .main.L1
	/*   jmp %.L0 [TAC] */
	/* --jmp .main.L0-- */
	/*  %.L0: [TAC] */
.main.L0:
	/*   %19 = const 1 [TAC] */
	movq $1, -104(%rbp)
	/*   jmp %.L1 [TAC] */
	/* --jmp .main.L1-- */
	/*  %.L1: [TAC] */
.main.L1:
	/*   %18 = copy %19 [TAC] */
	movq -104(%rbp), %r11
	movq %r11, -112(%rbp)
	movq -112(%rbp), %rdi
	/*   call @__bx_print_bool [TAC] */
	callq __bx_print_bool
	/*   %21 = copy @z [TAC] */
	movq z(%rip), %r11
	movq %r11, -120(%rbp)
	movq -120(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	xorq %rax, %rax
	jmp .main.Lexit
.main.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq
