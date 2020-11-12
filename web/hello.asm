reset:	jump start

int0:	reti
	nop

int1:	reti
	nop

start:	move $r1, hello
loop:	move $r2, [$r1]
	equal $r2, 0
	jumpt done
	move [224], $r2
	inc $r1
	jump loop
	

done:	halt

hello:	db "*** Hello world ***"
	db 10
	db 0
