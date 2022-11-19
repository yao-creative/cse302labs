

	.globl fizzbuzz
	.text
fizzbuzz:
	pushq %rbp
	movq %rsp, %rbp
	subq $208, %rsp
	movq %rdi, -8(%rbp)
	movq %rsi, -16(%rbp)
	/*  %.Lentry: [TAC] */
.fizzbuzz.Lentry:
	/*   jmp %.L0 [TAC] */
	/* --jmp .fizzbuzz.L0-- */
	/*  %.L0: [TAC] */
.fizzbuzz.L0:
	/*   %2 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -24(%rbp)
	/*   %3 = copy %1 [TAC] */
	movq -16(%rbp), %r11
	movq %r11, -32(%rbp)
	/*   %4 = sub %2, %3 [TAC] */
	movq -24(%rbp), %r11
	subq -32(%rbp), %r11
	movq %r11, -40(%rbp)
	/*   jle %4, %.L1 [TAC] */
	cmpq $0, -40(%rbp)
	jle .fizzbuzz.L1
	/*   jmp %.L2 [TAC] */
	/* --jmp .fizzbuzz.L2-- */
	/*  %.L2: [TAC] */
.fizzbuzz.L2:
	xorq %rax, %rax
	jmp .fizzbuzz.Lexit
	/*  %.L1: [TAC] */
.fizzbuzz.L1:
	/*   %6 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -48(%rbp)
	/*   %7 = const 3 [TAC] */
	movq $3, -56(%rbp)
	/*   %5 = mod %6, %7 [TAC] */
	movq -48(%rbp), %rax
	cqto
	idivq -56(%rbp)
	movq %rdx, -64(%rbp)
	/*   %8 = const 0 [TAC] */
	movq $0, -72(%rbp)
	/*   %9 = sub %5, %8 [TAC] */
	movq -64(%rbp), %r11
	subq -72(%rbp), %r11
	movq %r11, -80(%rbp)
	/*   jz %9, %.L3 [TAC] */
	cmpq $0, -80(%rbp)
	jz .fizzbuzz.L3
	/*   jmp %.L4 [TAC] */
	/* --jmp .fizzbuzz.L4-- */
	/*  %.L4: [TAC] */
.fizzbuzz.L4:
	/*   %20 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -88(%rbp)
	/*   %21 = const 5 [TAC] */
	movq $5, -96(%rbp)
	/*   %19 = mod %20, %21 [TAC] */
	movq -88(%rbp), %rax
	cqto
	idivq -96(%rbp)
	movq %rdx, -104(%rbp)
	/*   %22 = const 0 [TAC] */
	movq $0, -112(%rbp)
	/*   %23 = sub %19, %22 [TAC] */
	movq -104(%rbp), %r11
	subq -112(%rbp), %r11
	movq %r11, -120(%rbp)
	/*   jz %23, %.L9 [TAC] */
	cmpq $0, -120(%rbp)
	jz .fizzbuzz.L9
	/*   jmp %.L10 [TAC] */
	/* --jmp .fizzbuzz.L10-- */
	/*  %.L10: [TAC] */
.fizzbuzz.L10:
	/*   %27 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -128(%rbp)
	movq -128(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	/*   jmp %.L11 [TAC] */
	/* --jmp .fizzbuzz.L11-- */
	/*  %.L11: [TAC] */
.fizzbuzz.L11:
	/*   jmp %.L5 [TAC] */
	/* --jmp .fizzbuzz.L5-- */
	/*  %.L5: [TAC] */
.fizzbuzz.L5:
	/*   %28 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -136(%rbp)
	/*   %29 = const 1 [TAC] */
	movq $1, -144(%rbp)
	/*   %0 = add %28, %29 [TAC] */
	movq -136(%rbp), %r11
	addq -144(%rbp), %r11
	movq %r11, -8(%rbp)
	/*   jmp %.L0 [TAC] */
	jmp .fizzbuzz.L0
	/*  %.L3: [TAC] */
.fizzbuzz.L3:
	/*   %11 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -152(%rbp)
	/*   %12 = const 5 [TAC] */
	movq $5, -160(%rbp)
	/*   %10 = mod %11, %12 [TAC] */
	movq -152(%rbp), %rax
	cqto
	idivq -160(%rbp)
	movq %rdx, -168(%rbp)
	/*   %13 = const 0 [TAC] */
	movq $0, -176(%rbp)
	/*   %14 = sub %10, %13 [TAC] */
	movq -168(%rbp), %r11
	subq -176(%rbp), %r11
	movq %r11, -184(%rbp)
	/*   jz %14, %.L6 [TAC] */
	cmpq $0, -184(%rbp)
	jz .fizzbuzz.L6
	/*   jmp %.L7 [TAC] */
	/* --jmp .fizzbuzz.L7-- */
	/*  %.L7: [TAC] */
.fizzbuzz.L7:
	/*   %18 = const 333 [TAC] */
	movq $333, -192(%rbp)
	movq -192(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	/*   jmp %.L8 [TAC] */
	/* --jmp .fizzbuzz.L8-- */
	/*  %.L8: [TAC] */
.fizzbuzz.L8:
	/*   jmp %.L5 [TAC] */
	jmp .fizzbuzz.L5
	/*  %.L6: [TAC] */
.fizzbuzz.L6:
	/*   %16 = const 151515 [TAC] */
	movq $151515, -200(%rbp)
	movq -200(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	/*   jmp %.L8 [TAC] */
	jmp .fizzbuzz.L8
	/*  %.L9: [TAC] */
.fizzbuzz.L9:
	/*   %25 = const 555 [TAC] */
	movq $555, -208(%rbp)
	movq -208(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	/*   jmp %.L11 [TAC] */
	jmp .fizzbuzz.L11
.fizzbuzz.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq



	.globl main
	.text
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $16, %rsp
	/*  %.Lentry: [TAC] */
.main.Lentry:
	/*   %1 = const 0 [TAC] */
	movq $0, -8(%rbp)
	movq -8(%rbp), %rdi
	/*   %2 = const 100 [TAC] */
	movq $100, -16(%rbp)
	movq -16(%rbp), %rsi
	/*   call @fizzbuzz [TAC] */
	callq fizzbuzz
	xorq %rax, %rax
	jmp .main.Lexit
.main.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq
