import os
import fnmatch

def scandir(base, filter, recursive=False):
	arr = filter.split('/')
	path = base + '/' + '/'.join(arr[:-1])
	filter = arr[-1]
	res = []
	list = os.listdir(path)
	if recursive:
		l = len(list)
		if l > 0:
			i = 0
			while i < l:
				file = path + '/' + list[i]
				file = file.replace('/../', '/').replace('/./', '/')
				if not os.path.isfile(file):
					res = res+scandir(file, './'+filter, True)
				i += 1
	flist = fnmatch.filter(list, filter)
	l = len(flist)
	if l > 0:
		i = 0
		while i < l:
			file = path + '/' + flist[i]
			file = file.replace('/../', '/').replace('/./', '/')
			if os.path.isfile(file):
				res.append(file)
			i += 1
	return res
