import rpdb2

def some_func(x, y):

	try:
		return x / y
	except:
		print "Wait for debugger..."
		rpdb2.start_embedded_debugger("my_passwd")
		raise

some_func(1, 1)
some_func(1, 0)
