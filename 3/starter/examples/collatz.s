	.text
	.globl main
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $128, %rsp
	/*   %0 = const 837799 [TAC] */
	movq $837799, -8(%rbp)
	/*  %.L1: [TAC] */
.main.L1:
	/*   jmp %.L2 [TAC] */
	/* --jmp .main.L2-- */
	/*  %.L2: [TAC] */
.main.L2:
	/*   %4 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -16(%rbp)
	/*   print %4 [TAC] */
	movq -16(%rbp), %rdi
	callq bx_print_int
	/*   %8 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -24(%rbp)
	/*   %9 = const 1 [TAC] */
	movq $1, -32(%rbp)
	/*   %10 = sub %8, %9 [TAC] */
	movq -24(%rbp), %r11
	subq -32(%rbp), %r11
	movq %r11, -40(%rbp)
	/*   jz %10, %.L5 [TAC] */
	jz .main.L5
	/*   jmp %.L6 [TAC] */
	jmp .main.L6
	/*  %.L5: [TAC] */
.main.L5:
	/*   jmp %.L3 [TAC] */
	jmp .main.L3
	/*   jmp %.L7 [TAC] */
	jmp .main.L7
	/*  %.L6: [TAC] */
.main.L6:
	/*  %.L7: [TAC] */
.main.L7:
	/*   %15 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -48(%rbp)
	/*   %16 = const 2 [TAC] */
	movq $2, -56(%rbp)
	/*   %14 = mod %15, %16 [TAC] */
	movq -48(%rbp), %rax
	cqto
	idivq -56(%rbp)
	movq %rdx, -64(%rbp)
	/*   %17 = const 0 [TAC] */
	movq $0, -72(%rbp)
	/*   %18 = sub %14, %17 [TAC] */
	movq -64(%rbp), %r11
	subq -72(%rbp), %r11
	movq %r11, -80(%rbp)
	/*   jz %18, %.L11 [TAC] */
	jz .main.L11
	/*   jmp %.L12 [TAC] */
	jmp .main.L12
	/*  %.L11: [TAC] */
.main.L11:
	/*   %19 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -88(%rbp)
	/*   %20 = const 2 [TAC] */
	movq $2, -96(%rbp)
	/*   %0 = div %19, %20 [TAC] */
	movq -88(%rbp), %rax
	cqto
	idivq -96(%rbp)
	movq %rax, -8(%rbp)
	/*   jmp %.L13 [TAC] */
	jmp .main.L13
	/*  %.L12: [TAC] */
.main.L12:
	/*   %22 = const 3 [TAC] */
	movq $3, -104(%rbp)
	/*   %23 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -112(%rbp)
	/*   %21 = mul %22, %23 [TAC] */
	movq -104(%rbp), %rax
	imulq -112(%rbp)
	movq %rax, -120(%rbp)
	/*   %24 = const 1 [TAC] */
	movq $1, -128(%rbp)
	/*   %0 = add %21, %24 [TAC] */
	movq -120(%rbp), %r11
	addq -128(%rbp), %r11
	movq %r11, -8(%rbp)
	/*  %.L13: [TAC] */
.main.L13:
	/*   jmp %.L1 [TAC] */
	jmp .main.L1
	/*  %.L3: [TAC] */
.main.L3:
	movq %rbp, %rsp
	popq %rbp
	movq $0, %rax
	retq
