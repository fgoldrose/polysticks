import copy
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np



def state_name(state, vertical):
	name = []
	if vertical:
		name.append("V")
	else:
		name.append("H")
	for i in state:
		if i == None:
			name.append(None)
		else:
			nn = []
			for j in sorted(i):
				nn.append(j)
			name.append(tuple(sorted(i)))
	return tuple(name)


# returns a list of states vertically accessible from state
def vert(state, n):
	state_copy = copy.deepcopy(state)
	vert_results = []
	vert_results.append(state_copy)

	for i in range(1, n):
		temp = copy.deepcopy(vert_results)
		for inter_state in vert_results:
			c = inter_state
			clone_state = copy.deepcopy(c)
			d = clone_state
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
		vert_results = temp
	return vert_results


def horiz(state, n):
	state_copy = copy.deepcopy(state)
	horiz_results = []
	horiz_results.append(state_copy)

	for i in range(0, n):
		temp = copy.deepcopy(horiz_results)
		for inter_state in horiz_results:
			c = inter_state
			clone_state = copy.deepcopy(c)
			d = clone_state
			if c[i] == None:
				d[i] = [i]
			elif len(d[i]) > 1:
				d[i].remove(i)
				d[i] = None
			else:
				continue
			temp.append(clone_state)
		horiz_results = temp

	# delete [None]*n from the list since it is not valid (but was needed as a helper)
	for p in horiz_results:
		if p == [None]*n:
			horiz_results.remove(p)
	return horiz_results

def name_to_state(name):
	state = []
	for p in name:
		if p == None:
			state.append(None)
		elif p != "V" and p != "H":
			if list(p) not in state:
				state.append(list(p))
			else:
				state.append(state[state.index(list(p))])

	return state

def generate_graph(n):
	graph = {}
	start= [None]*n

	name = state_name(start, True)
	graph[name] = {}
	vert_results = vert(start, n)
	for v in vert_results:
		sn = state_name(v, False)
		if sn in graph[name]:
			graph[name][sn]['weight'] +=1
		else:
			graph[name][sn] = {'weight': 1}
	graph[('END')] = {}

	allfound = False
	while allfound == False:
		allfound = True
		graph_updates = {}

		for state in graph:
			for s in graph[state]:
				if s not in graph:
					allfound = False
					graph_updates[s] = {}
					if s[0] == "H":
						if valid_end(s):
							graph_updates[s]['END'] = {'weight': 1}					
						newstate = name_to_state(s)					
						horiz_results = horiz(newstate, n)
						for h in horiz_results:
							sn = state_name(h, True)
							graph_updates[s][sn] = {'weight': 1}
					else:
						newstate = name_to_state(s)
						vert_results = vert(newstate, n)
						for v in vert_results:
							sn = state_name(v, False)
							if sn in graph_updates[s]:
								graph_updates[s][sn]['weight'] +=1
							else:
								graph_updates[s][sn] = {'weight': 1}
		graph.update(graph_updates)
	return graph

#checks if there are multiple groups
def valid_end(name):
	s = set(name)
	if None in s:
		s.remove(None)
	if 'V' in s:
		return False
	if 'H' in s:
		s.remove('H')
	if len(s) != 1:
		return False
	return True
'''
#checks if there are multiple groups
def invalid_end(name):
	s = set(name)
	if 'N' in s:
		s.remove('N')
	if len(s) > 1:
		return True
	return False

#this can be way more efficient!
#not yet updated for new method
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
	'''
'''
def enum_helper(n,m, powers):
	if m == 1:
		return 1
	total = powers[2*m][0,1]
	print('total', total)
	walks = total
	for i in range(1, m):
		h = enum_helper(n, i, powers)
		print(i, h)
		walks -= 2* h
	if(m > 2):
		j = powers[2*(m-2)][0,1]
		print(i,j)
		walks -= j
	return walks

def enumerate(n,m):
	powers = {}
	graph = generate_graph(n)
	G = nx.DiGraph(graph)
	matrix = nx.to_numpy_matrix(G)
	powers[1] = matrix
	for i in range(2, 2*m+1):
		newmatrix = copy.copy(matrix)
		newmatrix = np.matmul(newmatrix, powers[1])
		powers[i] = newmatrix
		matrix = newmatrix
	walks = enum_helper(n,m, powers)
	return walks
'''

def enum_helper(n,m, matrices):
	if n < 1:
		return 0
	if n == 1:
		return 1
	powered = np.linalg.matrix_power(matrices[n], 2*m)
	walks = powered[0,1]
	for i in range(1, n):
		walks -= 2 * enum_helper(i, m, matrices)
	if n > 2:
		walks -= np.linalg.matrix_power(matrices[n-2], 2*m)[0,1]
	return walks


def enumerate(n, m):
	matrices = {}
	for i in range(1, n+1):
		graph = generate_graph(i)
		G = nx.DiGraph(graph)
		matrix = nx.to_numpy_matrix(G)
		matrices[i] = matrix
	walks = enum_helper(n,m, matrices)
	return walks

print(enumerate(6,6))
#nx.draw(G, with_labels=False)
#plt.show()


'''
print("enum ", enumerate(1, (None,)*n, True, False, False))
print("enum ", enumerate(2, (None,)*n,  True, False, False))
print("enum ", enumerate(3, (None,)*n,  True, False, False))
print("enum ", enumerate(4, (None,)*n,  True, False, False))
print("enum ", enumerate(5, (None,)*n,  True, False, False))
print("enum ", enumerate(6, (None,)*n,  True, False, False))
print("enum ", enumerate(7, (None,)*n,  True, False, False))
'''

