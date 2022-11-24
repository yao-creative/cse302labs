

	.globl test_bracks
	.text
test_bracks:
	pushq %rbp
	movq %rsp, %rbp
	subq $64, %rsp
	movq %rdi, -8(%rbp)
	/*  %.Lentry: [TAC] */
.test_bracks.Lentry:
	/*   %2 = const 0 [TAC] */
	movq $0, -16(%rbp)
	/*   %4 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -24(%rbp)
	/*   %5 = const 3 [TAC] */
	movq $3, -32(%rbp)
	/*   %3 = add %4, %5 [TAC] */
	movq -24(%rbp), %r11
	addq -32(%rbp), %r11
	movq %r11, -40(%rbp)
	/*   %6 = const 5 [TAC] */
	movq $5, -48(%rbp)
	/*   %7 = sub %3, %6 [TAC] */
	movq -40(%rbp), %r11
	subq -48(%rbp), %r11
	movq %r11, -56(%rbp)
	/*   jz %7, %.L0 [TAC] */
	cmpq $0, -56(%rbp)
	jz .test_bracks.L0
	/*   jmp %.L1 [TAC] */
	/* --jmp .test_bracks.L1-- */
	/*  %.L1: [TAC] */
.test_bracks.L1:
	/*   %1 = copy %2 [TAC] */
	movq -16(%rbp), %r11
	movq %r11, -64(%rbp)
	movq -64(%rbp), %rax
	jmp .test_bracks.Lexit
	/*  %.L0: [TAC] */
.test_bracks.L0:
	/*   %2 = const 1 [TAC] */
	movq $1, -16(%rbp)
	/*   jmp %.L1 [TAC] */
	jmp .test_bracks.L1
.test_bracks.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq



	.globl main
	.text
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $32, %rsp
	/*  %.Lentry: [TAC] */
.main.Lentry:
	/*   %2 = const 0 [TAC] */
	movq $0, -8(%rbp)
	/*   %4 = const 2 [TAC] */
	movq $2, -16(%rbp)
	movq -16(%rbp), %rdi
	/*   %3 = call @test_bracks, 1 [TAC] */
	callq test_bracks
	movq %rax, -24(%rbp)
	/*   jz %3, %.L1 [TAC] */
	cmpq $0, -24(%rbp)
	jz .main.L1
	/*   jmp %.L0 [TAC] */
	/* --jmp .main.L0-- */
	/*  %.L0: [TAC] */
.main.L0:
	/*   %2 = const 1 [TAC] */
	movq $1, -8(%rbp)
	/*   jmp %.L1 [TAC] */
	/* --jmp .main.L1-- */
	/*  %.L1: [TAC] */
.main.L1:
	/*   %1 = copy %2 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	movq -32(%rbp), %rdi
	/*   call @__bx_print_bool [TAC] */
	callq __bx_print_bool
	xorq %rax, %rax
	jmp .main.Lexit
.main.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq
