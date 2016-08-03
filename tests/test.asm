
	db 0x55
data1:	db "lkj"
	db 34
	
boot: 	nop
	move    $r4, $r5
	move	$r4, [123]
	move 	$r4, 12
	move  	$r5, [$sp-3]
	move 	[123], $st
	move    [123], 51
	move	[$r4+12], 0x14
	move	[$r4-12], 0x14
	move    [data1], $r4
	move    $r4, data1
	add 	$r4, $r5
	add	$r4, [123]
	add 	$r4, 12
	add   	$r5, [$sp-3]
	sub 	$r4, $r5
	sub	$r4, [123]
	sub 	$r4, 12
	sub   	$r5, [$sp-3]
	inc	$r1
	dec	$r1
	mul 	$r4, $r5
	mul	$r4, [123]
	mul 	$r4, 12
	mul   	$r5, [$sp-3]
	div 	$r4, $r5
	div	$r4, [123]
	div 	$r4, 12
	div   	$r5, [$sp-3]
	mod 	$r4, $r5
	mod	$r4, [123]
	mod 	$r4, 12
	mod   	$r5, [$sp-3]
	and 	$r4, $r5
	and	$r4, [123]
	and 	$r4, 12
	and   	$r5, [$sp-3]
	or 	$r4, $r5
	or	$r4, [123]
	or 	$r4, 12
	or   	$r5, [$sp-3]
	xor 	$r4, $r5
	xor	$r4, [123]
	xor 	$r4, 12
	xor   	$r5, [$sp-3]
	not   	$r5
	shiftl 	$r4, $r5
	shiftl	$r4, [123]
	shiftl 	$r4, 12
	shiftl 	$r5, [$sp-3]
	shiftr 	$r4, $r5
	shiftr	$r4, [123]
	shiftr 	$r4, 12
	shiftr 	$r5, [$sp-3]
	equal 	$r4, $r5
	equal	$r4, [123]
	equal 	$r4, 12
	equal 	$r5, [$sp-3]
	lt 	$r4, $r5
	lt	$r4, [123]
	lt 	$r4, 12
	lt 	$r5, [$sp-3]
	lte 	$r4, $r5
	lte	$r4, [123]
	lte 	$r4, 12
	lte 	$r5, [$sp-3]
	gt 	$r4, $r5
	gt	$r4, [123]
	gt 	$r4, 12
	gt 	$r5, [$sp-3]
	gte 	$r4, $r5
	gte	$r4, [123]
	gte 	$r4, 12
	gte 	$r5, [$sp-3]
	jump    l1
l1:	jump 	123
	jump	[$r4+4]
	jumpf 	123
	jumpf	[$r4+4]
	jumpt 	123
	jumpt	[$r4-4]
	call	123
	call    data1
	call	[$r4+4]
	ret
	reti
	seti
	cleari
	push 	$r5
	push	[123]
	push 	12
	push 	[$sp-3]
	pop	$r5
	halt
	sleep
	setbit	$r1, 4
	setbit  $r1, $r2
	clearbit	$r1, 4
	clearbit  $r1, $r2
	isset	$r1, 4
	isset  $r1, $r2
