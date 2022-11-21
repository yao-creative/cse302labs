	.text
	.globl main
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $256, %rsp
	/*   %0 = const 833779 [TAC] */
	movq $833779, -8(%rbp)
	/*   %5 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -16(%rbp)
	/*   %6 = const 2 [TAC] */
	movq $2, -24(%rbp)
	/*   %4 = mod %5, %6 [TAC] */
	movq -16(%rbp), %rax
	cqto
	idivq -24(%rbp)
	movq %rdx, -32(%rbp)
	/*   %7 = const 0 [TAC] */
	movq $0, -40(%rbp)
	/*   %8 = sub %4, %7 [TAC] */
	movq -32(%rbp), %r11
	subq -40(%rbp), %r11
	movq %r11, -48(%rbp)
	/*   jz %8, %.L1 [TAC] */
	jz .main.L1
	/*   jmp %.L2 [TAC] */
	jmp .main.L2
	/*  %.L1: [TAC] */
.main.L1:
	/*   %9 = const 2 [TAC] */
	movq $2, -56(%rbp)
	/*   print %9 [TAC] */
	movq -56(%rbp), %rdi
	callq bx_print_int
	/*   jmp %.L3 [TAC] */
	jmp .main.L3
	/*  %.L2: [TAC] */
.main.L2:
	/*   %14 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -64(%rbp)
	/*   %15 = const 3 [TAC] */
	movq $3, -72(%rbp)
	/*   %13 = mod %14, %15 [TAC] */
	movq -64(%rbp), %rax
	cqto
	idivq -72(%rbp)
	movq %rdx, -80(%rbp)
	/*   %16 = const 0 [TAC] */
	movq $0, -88(%rbp)
	/*   %17 = sub %13, %16 [TAC] */
	movq -80(%rbp), %r11
	subq -88(%rbp), %r11
	movq %r11, -96(%rbp)
	/*   jz %17, %.L10 [TAC] */
	jz .main.L10
	/*   jmp %.L11 [TAC] */
	jmp .main.L11
	/*  %.L10: [TAC] */
.main.L10:
	/*   %18 = const 3 [TAC] */
	movq $3, -104(%rbp)
	/*   print %18 [TAC] */
	movq -104(%rbp), %rdi
	callq bx_print_int
	/*   jmp %.L12 [TAC] */
	jmp .main.L12
	/*  %.L11: [TAC] */
.main.L11:
	/*   %23 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -112(%rbp)
	/*   %24 = const 5 [TAC] */
	movq $5, -120(%rbp)
	/*   %22 = mod %23, %24 [TAC] */
	movq -112(%rbp), %rax
	cqto
	idivq -120(%rbp)
	movq %rdx, -128(%rbp)
	/*   %25 = const 0 [TAC] */
	movq $0, -136(%rbp)
	/*   %26 = sub %22, %25 [TAC] */
	movq -128(%rbp), %r11
	subq -136(%rbp), %r11
	movq %r11, -144(%rbp)
	/*   jz %26, %.L19 [TAC] */
	jz .main.L19
	/*   jmp %.L20 [TAC] */
	jmp .main.L20
	/*  %.L19: [TAC] */
.main.L19:
	/*   %27 = const 5 [TAC] */
	movq $5, -152(%rbp)
	/*   print %27 [TAC] */
	movq -152(%rbp), %rdi
	callq bx_print_int
	/*   jmp %.L21 [TAC] */
	jmp .main.L21
	/*  %.L20: [TAC] */
.main.L20:
	/*   %32 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -160(%rbp)
	/*   %33 = const 7 [TAC] */
	movq $7, -168(%rbp)
	/*   %31 = mod %32, %33 [TAC] */
	movq -160(%rbp), %rax
	cqto
	idivq -168(%rbp)
	movq %rdx, -176(%rbp)
	/*   %34 = const 0 [TAC] */
	movq $0, -184(%rbp)
	/*   %35 = sub %31, %34 [TAC] */
	movq -176(%rbp), %r11
	subq -184(%rbp), %r11
	movq %r11, -192(%rbp)
	/*   jz %35, %.L28 [TAC] */
	jz .main.L28
	/*   jmp %.L29 [TAC] */
	jmp .main.L29
	/*  %.L28: [TAC] */
.main.L28:
	/*   %36 = const 7 [TAC] */
	movq $7, -200(%rbp)
	/*   print %36 [TAC] */
	movq -200(%rbp), %rdi
	callq bx_print_int
	/*   jmp %.L30 [TAC] */
	jmp .main.L30
	/*  %.L29: [TAC] */
.main.L29:
	/*   %41 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -208(%rbp)
	/*   %42 = const 11 [TAC] */
	movq $11, -216(%rbp)
	/*   %40 = mod %41, %42 [TAC] */
	movq -208(%rbp), %rax
	cqto
	idivq -216(%rbp)
	movq %rdx, -224(%rbp)
	/*   %43 = const 0 [TAC] */
	movq $0, -232(%rbp)
	/*   %44 = sub %40, %43 [TAC] */
	movq -224(%rbp), %r11
	subq -232(%rbp), %r11
	movq %r11, -240(%rbp)
	/*   jz %44, %.L37 [TAC] */
	jz .main.L37
	/*   jmp %.L38 [TAC] */
	jmp .main.L38
	/*  %.L37: [TAC] */
.main.L37:
	/*   %45 = const 11 [TAC] */
	movq $11, -248(%rbp)
	/*   print %45 [TAC] */
	movq -248(%rbp), %rdi
	callq bx_print_int
	/*   jmp %.L39 [TAC] */
	jmp .main.L39
	/*  %.L38: [TAC] */
.main.L38:
	/*  %.L39: [TAC] */
.main.L39:
	/*  %.L30: [TAC] */
.main.L30:
	/*  %.L21: [TAC] */
.main.L21:
	/*  %.L12: [TAC] */
.main.L12:
	/*  %.L3: [TAC] */
.main.L3:
	movq %rbp, %rsp
	popq %rbp
	movq $0, %rax
	retq
