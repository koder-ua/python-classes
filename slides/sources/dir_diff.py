import os
import os.path


def get_all(path):
	for cpath, dirs, files in os.walk(path):
		for fname in files:
			yield os.path.join(cpath, fname)


def walk_two(path1, path2):
	pp1 = lambda x  : os.path.join(path1, x) 
	pp2 = lambda x  : os.path.join(path2, x) 

	names1 = set(os.listdir(path1))
	names2 = set(os.listdir(path2))

	files1 = set(i for i in names1 if os.path.isfile(pp1(i)))
	files2 = set(i for i in names2 if os.path.isfile(pp2(i)))

	dirs1 = set(i for i in names1 if os.path.isdir(pp1(i)))
	dirs2 = set(i for i in names2 if os.path.isdir(pp2(i)))

	for i in files1 - files2:
		yield True, pp1(i)

	for i in files2 - files1:
		yield False, pp2(i)

	for name in dirs1 - dirs2:
		aname = pp1(name)
		for i in get_all(aname):
			yield True, i

	for name in dirs2 - dirs1:
		aname = pp2(name)
		for i in get_all(aname):
			yield False, i

	for name in (dirs1 & dirs2):
		aname1 = pp1(name)
		aname2 = pp2(name)
		for tp, name in  walk_two(aname1, aname2):
			yield tp, name






def walk_two2(path1, path2):
	files1 = set([i[len(path1): ] for i in get_all(path1)])
	files2 = set([i[len(path2): ] for i in get_all(path2)])

	return [os.path.join(path1,i) for i in files1 - files2], \
	       [os.path.join(path2,i) for i in files2 - files1],





print [i for tp,i in walk_two("/tmp/pp/p1", "/tmp/pp/p2") if tp]
print [i for tp,i in walk_two("/tmp/pp/p1", "/tmp/pp/p2") if not tp]
print
print

p1,p2 = walk_two2("/tmp/pp/p1", "/tmp/pp/p2")
print p1
print p2



