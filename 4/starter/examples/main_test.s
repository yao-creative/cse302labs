	.globl f0
	.data
f0:  .quad 0
	.globl f1
	.data
f1:  .quad 1


	.globl main
	.text
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $64, %rsp
	/*  %.Lentry: [TAC] */
.main.Lentry:
	/*   %0 = const 0 [TAC] */
	movq $0, -8(%rbp)
	/*   jmp %.L0 [TAC] */
	/* --jmp .main.L0-- */
	/*  %.L0: [TAC] */
.main.L0:
	/*   %1 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -16(%rbp)
	/*   %2 = const 10 [TAC] */
	movq $10, -24(%rbp)
	/*   %3 = sub %1, %2 [TAC] */
	movq -16(%rbp), %r11
	subq -24(%rbp), %r11
	movq %r11, -32(%rbp)
	/*   jl %3, %.L1 [TAC] */
	cmpq $0, -32(%rbp)
	jl .main.L1
	/*   jmp %.L2 [TAC] */
	/* --jmp .main.L2-- */
	/*  %.L2: [TAC] */
.main.L2:
	xorq %rax, %rax
	jmp .main.Lexit
	/*  %.L1: [TAC] */
.main.L1:
	/*   %6 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -40(%rbp)
	movq -40(%rbp), %rdi
	/*   %5 = call @fib, 1 [TAC] */
	callq fib
	movq %rax, -48(%rbp)
	movq -48(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	/*   %7 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -56(%rbp)
	/*   %8 = const 1 [TAC] */
	movq $1, -64(%rbp)
	/*   %0 = add %7, %8 [TAC] */
	movq -56(%rbp), %r11
	addq -64(%rbp), %r11
	movq %r11, -8(%rbp)
	/*   jmp %.L0 [TAC] */
	jmp .main.L0
.main.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq



	.globl fib
	.text
fib:
	pushq %rbp
	movq %rsp, %rbp
	subq $128, %rsp
	movq %rdi, -8(%rbp)
	/*  %.Lentry: [TAC] */
.fib.Lentry:
	/*   %1 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -16(%rbp)
	/*   %2 = const 0 [TAC] */
	movq $0, -24(%rbp)
	/*   %3 = sub %1, %2 [TAC] */
	movq -16(%rbp), %r11
	subq -24(%rbp), %r11
	movq %r11, -32(%rbp)
	/*   jz %3, %.L0 [TAC] */
	cmpq $0, -32(%rbp)
	jz .fib.L0
	/*   jmp %.L1 [TAC] */
	/* --jmp .fib.L1-- */
	/*  %.L1: [TAC] */
.fib.L1:
	/*   %4 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -40(%rbp)
	/*   %5 = const 1 [TAC] */
	movq $1, -48(%rbp)
	/*   %6 = sub %4, %5 [TAC] */
	movq -40(%rbp), %r11
	subq -48(%rbp), %r11
	movq %r11, -56(%rbp)
	/*   jz %6, %.L3 [TAC] */
	cmpq $0, -56(%rbp)
	jz .fib.L3
	/*   jmp %.L4 [TAC] */
	/* --jmp .fib.L4-- */
	/*  %.L4: [TAC] */
.fib.L4:
	/*   %10 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -64(%rbp)
	/*   %11 = const 1 [TAC] */
	movq $1, -72(%rbp)
	/*   %9 = sub %10, %11 [TAC] */
	movq -64(%rbp), %r11
	subq -72(%rbp), %r11
	movq %r11, -80(%rbp)
	movq -80(%rbp), %rdi
	/*   %8 = call @fib, 1 [TAC] */
	callq fib
	movq %rax, -88(%rbp)
	/*   %14 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -96(%rbp)
	/*   %15 = const 2 [TAC] */
	movq $2, -104(%rbp)
	/*   %13 = sub %14, %15 [TAC] */
	movq -96(%rbp), %r11
	subq -104(%rbp), %r11
	movq %r11, -112(%rbp)
	movq -112(%rbp), %rdi
	/*   %12 = call @fib, 1 [TAC] */
	callq fib
	movq %rax, -120(%rbp)
	/*   %7 = add %8, %12 [TAC] */
	movq -88(%rbp), %r11
	addq -120(%rbp), %r11
	movq %r11, -128(%rbp)
	movq -128(%rbp), %rax
	jmp .fib.Lexit
	/*   jmp %.L5 [TAC] */
	/* --jmp .fib.L5-- */
	/*  %.L5: [TAC] */
.fib.L5:
	/*   jmp %.L2 [TAC] */
	/* --jmp .fib.L2-- */
	/*  %.L2: [TAC] */
.fib.L2:
	xorq %rax, %rax
	jmp .fib.Lexit
	/*  %.L0: [TAC] */
.fib.L0:
	movq f0(%rip), %rax
	jmp .fib.Lexit
	/*   jmp %.L2 [TAC] */
	jmp .fib.L2
	/*  %.L3: [TAC] */
.fib.L3:
	movq f1(%rip), %rax
	jmp .fib.Lexit
	/*   jmp %.L5 [TAC] */
	jmp .fib.L5
.fib.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq
