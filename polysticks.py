import copy

n = 4

vertgraph = {}
horizgraph = {}
#finalvgraph = {}

start_state = {"partitions":[None]*n, "horiz":[], "vert":[]}

def state_name(state):
	name = []
	for i in state["partitions"]:
		if i == None:
			name.append("N")
		else:
			nn = ""
			for j in sorted(i):
				nn += str(j)
			name.append(nn)
	return tuple(name)

#vert is currently broken bc doesnt take into account that you can 
# get to an outcome in several ways. needs to be a weighted graph.
def vert(state):
	if state_name(state) in vertgraph:
		return

	state_copy = {"partitions":copy.deepcopy(state["partitions"]), "horiz":[], "vert":[]}
	state["vert"].append(state_copy)
	for i in range(1, n):
		temp = copy.deepcopy(state["vert"])
		for inter_state in state["vert"]:
			c = inter_state["partitions"]
			clone_state = {"partitions":copy.deepcopy(c), "horiz":[], "vert":[]}
			d = clone_state["partitions"]
			if c[i-1] == None and c[i] == None:
				newlist = [i-1, i]
				d[i-1] = newlist
				d[i] = newlist
			elif c[i] == None:
				d[i] = d[i-1]
				d[i-1].append(i)
			elif c[i-1] == None:
				d[i-1] = d[i]
				d[i].append(i-1)
			elif c[i-1] != c[i]:
				concat = d[i-1] + d[i]
				for b in concat:
					d[b] = concat
			#if they are the same, an extra copy is added
			temp.append(clone_state)
		state["vert"] = temp

	name = state_name(state)
	vertgraph[name] = {}
	for v in state["vert"]:
		sn = state_name(v)
		if sn in vertgraph[name]:
			vertgraph[name][sn] +=1
		else:
			vertgraph[name][sn] = 1

'''
def finalvert(state, notop, nobottom):
	name = state_name(state)
	if name in finalvgraph:
		if notop and nobottom and "-tb" in finalvgraph[name]:
				return
		if notop and "-t" in finalvgraph[name]:
			return
		if nobottom and "-b" in finalvgraph[name]:
			return
		if not (notop or nobottom) and "+tb" in finalvgraph[name]:
			return

	finalverts = []
	state_copy = {"partitions":copy.deepcopy(state["partitions"]), "horiz":[], "vert":[]}
	finalverts.append(state_copy)
	start = 1
	end = n
	c = state_copy["partitions"]
	if notop and c[0] == None:
		start = 2
		if c[1] == None:
			newlist = [0, 1]
			c[0] = newlist
			c[1] = newlist
		else:
			c[0] = c[1]
			c[1].append(0)

	if nobottom and c[n-1] == None:
		end = n-1
		if c[n-2] == None:
			newlist = [n-2, n-1]
			c[n-2] = newlist
			c[n-1] = newlist
		else:
			c[n-1] = c[n-2]
			c[n-2].append(n-1)

	toremove = []
	for i in range(start, end):
		temp = copy.deepcopy(finalverts)
		for inter_state in finalverts:
			c = inter_state["partitions"]
			clone_state = {"partitions":copy.deepcopy(c), "horiz":[], "vert":[]}
			d = clone_state["partitions"]
			if c[i-1] == None and c[i] == None:
				newlist = [i-1, i]
				d[i-1] = newlist
				d[i] = newlist
			elif c[i] == None:
				d[i] = d[i-1]
				d[i-1].append(i)
				#if c[i:] != [None]*(n-i):
				#	temp.remove(inter_state)
			elif c[i-1] == None:
				d[i-1] = d[i]
				d[i].append(i-1)
			elif c[i-1] != c[i]: #dont want to add a new one, must join them.
				concat = d[i-1] + d[i]
				for b in concat:
					d[b] = concat
				toremove.append(inter_state)
			temp.append(clone_state)
		finalverts = temp
	for r in toremove:
		if r in finalverts:
			finalverts.remove(r)

	addon = "+tb"
	if nobottom and notop:
		addon = "-tb"
	elif notop:
		addon = "-t"
	elif nobottom:
		addon = "-b"

	if name not in finalvgraph:
		finalvgraph[name] = {}
	finalvgraph[name][addon] = {}
	for v in finalverts:
		sn = state_name(v)
		if sn in finalvgraph[name][addon]:
			finalvgraph[name][addon][sn] +=1
		else:
			finalvgraph[name][addon][sn] = 1
'''

def horiz(state):
	if state_name(state) in horizgraph:
		return

	state_copy = {"partitions":copy.deepcopy(state["partitions"]), "horiz":[], "vert":[]}
	state["horiz"].append(state_copy)
	for i in range(0, n):
		temp = copy.deepcopy(state["horiz"])
		for inter_state in state["horiz"]:
			c = inter_state["partitions"]
			clone_state = {"partitions":copy.deepcopy(c), "horiz":[], "vert":[]}
			d = clone_state["partitions"]
			if c[i] == None:
				d[i] = [i]
			elif len(d[i]) > 1:
				d[i].remove(i)
				d[i] = None
			else:
				continue
			temp.append(clone_state)
		state["horiz"] = temp

	# delete [None]*n from the list since it is not valid (but was needed as a helper)
	for p in state["horiz"]:
		if p["partitions"] == [None]*n:
			state["horiz"].remove(p)

	horizgraph[state_name(state)] = []
	for h in state["horiz"]:
		sn = state_name(h)
		horizgraph[state_name(state)].append(sn)

def generate_graphs(start):
	vert(start)

	'''
	no_t = False
	no_b = False
	if start["partitions"][0] == None:
		no_t = True
	if start["partitions"][n-1] == None:
		no_b = True
	finalvert(start, False, False)
	if no_t:
		finalvert(start, True, False)
	if no_b:
		finalvert(start, False, True)
	if no_t and no_b:
		finalvert(start, True, True)
	'''
	for s in start["vert"]:
		horiz(s)
		for t in s["horiz"]:
			generate_graphs(t)

#checks if there are multiple groups
def invalid_end(name):
	s = set(name)
	if 'N' in s:
		s.remove('N')
	if len(s) > 1:
		return True
	return False

#this can be way more efficient!
def enumerate(width, start, vert, top, bottom):
	acc = 0
	if width == 0:
		if not top or not bottom:
			return 0
		if invalid_end(start):
			return 0
		return 1
	if vert:
		for v in vertgraph[start]:
			t = top
			b = bottom
			if v[0] != 'N':
				t = True
			if v[-1] != 'N':
				b = True
			acc += vertgraph[start][v] * enumerate(width-1, v, False, t, b)
	else:
		for h in horizgraph[start]:
			t = top
			b = bottom
			if h[0] != 'N':
				t = True
			if h[-1] != 'N':
				b = True
			acc += enumerate(width, h, True, t, b)
	return acc

ll = [1,2]
test_state = {"partitions":[None, ll, ll], "horiz":[], "vert":[]}
#test_state = start_state
#print(test_state)
#vert(test_state)
#horiz(test_state)
#print(test_state)
generate_graphs(start_state)
print("vertgraph", vertgraph)
print("horizgraph", horizgraph)

print("enum ", enumerate(1, ('N',)*n, True, False, False))
print("enum ", enumerate(2, ('N',)*n, True, False, False))
print("enum ", enumerate(3, ('N',)*n, True, False, False))
print("enum ", enumerate(4, ('N',)*n, True, False, False))
print("enum ", enumerate(5, ('N',)*n, True, False, False))
print("enum ", enumerate(6, ('N',)*n, True, False, False))


