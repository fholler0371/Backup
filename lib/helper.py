"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Version 1.0
"""

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
