import IPython

def some_func(x, y):

	try:
		return x / y
	except:
		IPython.embed()
		raise

some_func(1, 1)
some_func(1, 0)
