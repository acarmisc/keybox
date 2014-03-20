def colorize(s, c):
	colors = {
		'blue': '\033[94m',
		'green': '\033[92m',
		'warning': '\033[93m',
		'fail': '\033[91m',
		'end': '\033[0m',
	}
	
	return ''.join([colors[c],s,colors['end']])