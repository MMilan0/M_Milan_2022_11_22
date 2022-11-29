for(;;){
	$key = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')

	if ($key.VirtualKeyCode -eq 37){
		# left
		write-host -noNewLine [char]0x1b[1D
	}
	if ($key.VirtualKeyCode -eq 39){
		#right
	}
	if ($key.VirtualKeyCode -eq 38){
		#up
	}
	if ($key.VirtualKeyCode -eq 40){
		#down
	}

}