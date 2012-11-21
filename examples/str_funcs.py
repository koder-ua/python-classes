def decode(data):
	res = []
	prev = None
	inserted = False
	for i in data:
		if prev == i:
			if not inserted:
				if '#' == i:
					res.append(res[-1])
				else:
					res.append(i)
				inserted = True
		else:
			inserted = False
		prev = i
	return "".join(res)

decode("11122223####")
