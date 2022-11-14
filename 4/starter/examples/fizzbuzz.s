

	.globl fizzbuzz
	.text
fizzbuzz:
	pushq %rbp
	movq %rsp, %rbp
	subq $2, %rsp
	/*  %.L0: [TAC] */
.fizzbuzz.L0:
	/*   %2 = copy %0 [TAC] */
	movq %rdi, %r11
	movq %r11, -24(%rbp)
	/*   %3 = copy %1 [TAC] */
	movq %rsi, %r11
	movq %r11, -32(%rbp)
	/*   %4 = sub %2, %3 [TAC] */
	movq -24(%rbp), %r11
	subq -32(%rbp), %r11
	movq %r11, -40(%rbp)
	/*   jle %4, %.L1 [TAC] */
	jle .fizzbuzz.L1
	/*   jmp %.L2 [TAC] */
	jmp .fizzbuzz.L2
	/*  %.L1: [TAC] */
.fizzbuzz.L1:
	/*   %6 = copy %0 [TAC] */
	movq %rdi, %r11
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
	jz .fizzbuzz.L3
	/*   jmp %.L4 [TAC] */
	jmp .fizzbuzz.L4
	/*  %.L3: [TAC] */
.fizzbuzz.L3:
	/*   %11 = copy %0 [TAC] */
	movq %rdi, %r11
	movq %r11, -88(%rbp)
	/*   %12 = const 5 [TAC] */
	movq $5, -96(%rbp)
	/*   %10 = mod %11, %12 [TAC] */
	movq -88(%rbp), %rax
	cqto
	idivq -96(%rbp)
	movq %rdx, -104(%rbp)
	/*   %13 = const 0 [TAC] */
	movq $0, -112(%rbp)
	/*   %14 = sub %10, %13 [TAC] */
	movq -104(%rbp), %r11
	subq -112(%rbp), %r11
	movq %r11, -120(%rbp)
	/*   jz %14, %.L6 [TAC] */
	jz .fizzbuzz.L6
	/*   jmp %.L7 [TAC] */
	jmp .fizzbuzz.L7
	/*  %.L6: [TAC] */
.fizzbuzz.L6:
	/*   %15 = const 151515 [TAC] */
	movq $151515, -128(%rbp)
	movq -136(%rbp), %rdi
	callq print
	/*   jmp %.L8 [TAC] */
	jmp .fizzbuzz.L8
	/*  %.L7: [TAC] */
.fizzbuzz.L7:
	/*   %17 = const 333 [TAC] */
	movq $333, -144(%rbp)
	movq -152(%rbp), %rdi
	callq print
	/*  %.L8: [TAC] */
.fizzbuzz.L8:
	/*   jmp %.L5 [TAC] */
	jmp .fizzbuzz.L5
	/*  %.L4: [TAC] */
.fizzbuzz.L4:
	/*   %20 = copy %0 [TAC] */
	movq %rdi, %r11
	movq %r11, -160(%rbp)
	/*   %21 = const 5 [TAC] */
	movq $5, -168(%rbp)
	/*   %19 = mod %20, %21 [TAC] */
	movq -160(%rbp), %rax
	cqto
	idivq -168(%rbp)
	movq %rdx, -176(%rbp)
	/*   %22 = const 0 [TAC] */
	movq $0, -184(%rbp)
	/*   %23 = sub %19, %22 [TAC] */
	movq -176(%rbp), %r11
	subq -184(%rbp), %r11
	movq %r11, -192(%rbp)
	/*   jz %23, %.L9 [TAC] */
	jz .fizzbuzz.L9
	/*   jmp %.L10 [TAC] */
	jmp .fizzbuzz.L10
	/*  %.L9: [TAC] */
.fizzbuzz.L9:
	/*   %24 = const 555 [TAC] */
	movq $555, -200(%rbp)
	movq -208(%rbp), %rdi
	callq print
	/*   jmp %.L11 [TAC] */
	jmp .fizzbuzz.L11
	/*  %.L10: [TAC] */
.fizzbuzz.L10:
	movq %rdi, %rdi
	callq print
	/*  %.L11: [TAC] */
.fizzbuzz.L11:
	/*  %.L5: [TAC] */
.fizzbuzz.L5:
	/*   %27 = copy %0 [TAC] */
	movq %rdi, %r11
	movq %r11, -216(%rbp)
	/*   %28 = const 1 [TAC] */
	movq $1, -224(%rbp)
	/*   %0 = add %27, %28 [TAC] */
	movq -216(%rbp), %r11
	addq -224(%rbp), %r11
	movq %r11, %rdi
	/*   jmp %.L0 [TAC] */
	jmp .fizzbuzz.L0
	/*  %.L2: [TAC] */
.fizzbuzz.L2:
	xorq %rax, %rax
	jmp fizzbuzz.Lexit
.fizzbuzz.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq



	.globl main
	.text
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $0, %rsp
	/*   %0 = const 0 [TAC] */
	movq $0, -8(%rbp)
	movq -16(%rbp), %rdi
	/*   %0 = const 100 [TAC] */
	movq $100, -8(%rbp)
	movq -24(%rbp), %rsi
	callq fizzbuzz
	xorq %rax, %rax
	jmp main.Lexit
.main.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq
