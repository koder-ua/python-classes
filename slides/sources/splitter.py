def get_line(fname):
	with open(fname) as fd:
		while True:
			ln = fd.readline()
			if ln == "":
				break
			yield ln

def parse_lines(it):
	for line in it:
		ip, x, y, rest = line.split(None, 3)

		date, rest = rest.split(']', 1)
		date += ']'

		pref, opts, rest = rest.split('"', 2)
		opts = '"{}"'.format(opts)

		code, rest = rest.rstrip().split(None, 1)

		yield [ip, x, y, date, opts, code, rest]

get_line('/home/koder/Downloads/access_log')