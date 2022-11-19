

	.globl fib
	.text
fib:
	pushq %rbp
	movq %rsp, %rbp
	subq $144, %rsp
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
	/*   %5 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -40(%rbp)
	/*   %6 = const 1 [TAC] */
	movq $1, -48(%rbp)
	/*   %7 = sub %5, %6 [TAC] */
	movq -40(%rbp), %r11
	subq -48(%rbp), %r11
	movq %r11, -56(%rbp)
	/*   jz %7, %.L3 [TAC] */
	cmpq $0, -56(%rbp)
	jz .fib.L3
	/*   jmp %.L4 [TAC] */
	/* --jmp .fib.L4-- */
	/*  %.L4: [TAC] */
.fib.L4:
	/*   %12 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -64(%rbp)
	/*   %13 = const 1 [TAC] */
	movq $1, -72(%rbp)
	/*   %11 = sub %12, %13 [TAC] */
	movq -64(%rbp), %r11
	subq -72(%rbp), %r11
	movq %r11, -80(%rbp)
	movq -80(%rbp), %rdi
	/*   %10 = call @fib, 1 [TAC] */
	callq fib
	movq %rax, -88(%rbp)
	/*   %16 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -96(%rbp)
	/*   %17 = const 2 [TAC] */
	movq $2, -104(%rbp)
	/*   %15 = sub %16, %17 [TAC] */
	movq -96(%rbp), %r11
	subq -104(%rbp), %r11
	movq %r11, -112(%rbp)
	movq -112(%rbp), %rdi
	/*   %14 = call @fib, 1 [TAC] */
	callq fib
	movq %rax, -120(%rbp)
	/*   %9 = add %10, %14 [TAC] */
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
	/*   %4 = const 0 [TAC] */
	movq $0, -136(%rbp)
	movq -136(%rbp), %rax
	jmp .fib.Lexit
	/*   jmp %.L2 [TAC] */
	jmp .fib.L2
	/*  %.L3: [TAC] */
.fib.L3:
	/*   %8 = const 1 [TAC] */
	movq $1, -144(%rbp)
	movq -144(%rbp), %rax
	jmp .fib.Lexit
	/*   jmp %.L5 [TAC] */
	jmp .fib.L5
.fib.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq



	.globl is_even
	.text
is_even:
	pushq %rbp
	movq %rsp, %rbp
	subq $80, %rsp
	movq %rdi, -8(%rbp)
	/*  %.Lentry: [TAC] */
.is_even.Lentry:
	/*   %2 = const 0 [TAC] */
	movq $0, -16(%rbp)
	/*   %3 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -24(%rbp)
	/*   %4 = const 0 [TAC] */
	movq $0, -32(%rbp)
	/*   %5 = sub %3, %4 [TAC] */
	movq -24(%rbp), %r11
	subq -32(%rbp), %r11
	movq %r11, -40(%rbp)
	/*   jz %5, %.L0 [TAC] */
	cmpq $0, -40(%rbp)
	jz .is_even.L0
	/*   jmp %.L2 [TAC] */
	/* --jmp .is_even.L2-- */
	/*  %.L2: [TAC] */
.is_even.L2:
	/*   %8 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -48(%rbp)
	/*   %9 = const 1 [TAC] */
	movq $1, -56(%rbp)
	/*   %7 = sub %8, %9 [TAC] */
	movq -48(%rbp), %r11
	subq -56(%rbp), %r11
	movq %r11, -64(%rbp)
	movq -64(%rbp), %rdi
	/*   %6 = call @is_odd, 1 [TAC] */
	callq is_odd
	movq %rax, -72(%rbp)
	/*   jz %6, %.L1 [TAC] */
	cmpq $0, -72(%rbp)
	jz .is_even.L1
	/*   jmp %.L0 [TAC] */
	/* --jmp .is_even.L0-- */
	/*  %.L0: [TAC] */
.is_even.L0:
	/*   %2 = const 1 [TAC] */
	movq $1, -16(%rbp)
	/*   jmp %.L1 [TAC] */
	/* --jmp .is_even.L1-- */
	/*  %.L1: [TAC] */
.is_even.L1:
	/*   %1 = copy %2 [TAC] */
	movq -16(%rbp), %r11
	movq %r11, -80(%rbp)
	movq -80(%rbp), %rax
	jmp .is_even.Lexit
.is_even.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq



	.globl is_odd
	.text
is_odd:
	pushq %rbp
	movq %rsp, %rbp
	subq $80, %rsp
	movq %rdi, -8(%rbp)
	/*  %.Lentry: [TAC] */
.is_odd.Lentry:
	/*   %2 = const 42 [TAC] */
	movq $42, -16(%rbp)
	/*   %3 = const 42 [TAC] */
	movq $42, -24(%rbp)
	/*   %1 = add %2, %3 [TAC] */
	movq -16(%rbp), %r11
	addq -24(%rbp), %r11
	movq %r11, -32(%rbp)
	/*   %5 = const 0 [TAC] */
	movq $0, -40(%rbp)
	/*   %8 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -48(%rbp)
	/*   %9 = const 1 [TAC] */
	movq $1, -56(%rbp)
	/*   %7 = sub %8, %9 [TAC] */
	movq -48(%rbp), %r11
	subq -56(%rbp), %r11
	movq %r11, -64(%rbp)
	movq -64(%rbp), %rdi
	/*   %6 = call @is_even, 1 [TAC] */
	callq is_even
	movq %rax, -72(%rbp)
	/*   jz %6, %.L1 [TAC] */
	cmpq $0, -72(%rbp)
	jz .is_odd.L1
	/*   jmp %.L0 [TAC] */
	/* --jmp .is_odd.L0-- */
	/*  %.L0: [TAC] */
.is_odd.L0:
	/*   %5 = const 1 [TAC] */
	movq $1, -40(%rbp)
	/*   jmp %.L1 [TAC] */
	/* --jmp .is_odd.L1-- */
	/*  %.L1: [TAC] */
.is_odd.L1:
	/*   %4 = copy %5 [TAC] */
	movq -40(%rbp), %r11
	movq %r11, -80(%rbp)
	movq -80(%rbp), %rax
	jmp .is_odd.Lexit
.is_odd.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq



	.globl print_range
	.text
print_range:
	pushq %rbp
	movq %rsp, %rbp
	subq $96, %rsp
	movq %rdi, -8(%rbp)
	movq %rsi, -16(%rbp)
	/*  %.Lentry: [TAC] */
.print_range.Lentry:
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
	/*   jl %4, %.L0 [TAC] */
	cmpq $0, -40(%rbp)
	jl .print_range.L0
	/*   jmp %.L1 [TAC] */
	/* --jmp .print_range.L1-- */
	/*  %.L1: [TAC] */
.print_range.L1:
	/*   jmp %.L2 [TAC] */
	/* --jmp .print_range.L2-- */
	/*  %.L2: [TAC] */
.print_range.L2:
	xorq %rax, %rax
	jmp .print_range.Lexit
	/*  %.L0: [TAC] */
.print_range.L0:
	/*   %6 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -48(%rbp)
	movq -48(%rbp), %rdi
	/*   call @__bx_print_int [TAC] */
	callq __bx_print_int
	/*   %9 = copy %0 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -56(%rbp)
	/*   %10 = const 1 [TAC] */
	movq $1, -64(%rbp)
	/*   %8 = add %9, %10 [TAC] */
	movq -56(%rbp), %r11
	addq -64(%rbp), %r11
	movq %r11, -72(%rbp)
	movq -72(%rbp), %rdi
	/*   %11 = copy %1 [TAC] */
	movq -16(%rbp), %r11
	movq %r11, -80(%rbp)
	movq -80(%rbp), %rsi
	/*   call @print_range [TAC] */
	callq print_range
	movq -88(%rbp), %rax
	jmp .print_range.Lexit
	/*   jmp %.L2 [TAC] */
	jmp .print_range.L2
.print_range.Lexit:
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
	/*   %2 = const 0 [TAC] */
	movq $0, -8(%rbp)
	/*   %4 = const 4 [TAC] */
	movq $4, -16(%rbp)
	movq -16(%rbp), %rdi
	/*   %3 = call @is_even, 1 [TAC] */
	callq is_even
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
	/*   %7 = const 0 [TAC] */
	movq $0, -40(%rbp)
	/*   %9 = const 5 [TAC] */
	movq $5, -48(%rbp)
	movq -48(%rbp), %rdi
	/*   %8 = call @is_odd, 1 [TAC] */
	callq is_odd
	movq %rax, -56(%rbp)
	/*   jz %8, %.L3 [TAC] */
	cmpq $0, -56(%rbp)
	jz .main.L3
	/*   jmp %.L2 [TAC] */
	/* --jmp .main.L2-- */
	/*  %.L2: [TAC] */
.main.L2:
	/*   %7 = const 1 [TAC] */
	movq $1, -40(%rbp)
	/*   jmp %.L3 [TAC] */
	/* --jmp .main.L3-- */
	/*  %.L3: [TAC] */
.main.L3:
	/*   %6 = copy %7 [TAC] */
	movq -40(%rbp), %r11
	movq %r11, -64(%rbp)
	movq -64(%rbp), %rdi
	/*   call @__bx_print_bool [TAC] */
	callq __bx_print_bool
	/*   %11 = const 3 [TAC] */
	movq $3, -72(%rbp)
	movq -72(%rbp), %rdi
	/*   %12 = const 9 [TAC] */
	movq $9, -80(%rbp)
	movq -80(%rbp), %rsi
	/*   call @print_range [TAC] */
	callq print_range
	/*   %15 = const 4 [TAC] */
	movq $4, -88(%rbp)
	movq -88(%rbp), %rdi
	/*   %14 = call @fib, 1 [TAC] */
	callq fib
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
