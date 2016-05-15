#Python methods for unrooted trees built from newick strings
#Author: Noah Weber
#Note: treemeth stands for "tree methods" it is not a kind of meth for trees
#Note: For Python 2.7, also needs pyparsing module for Python2
#EDIT: Changed some things, it should now work for Python3 as well as 2
#EDIT: All quartets clarified to mean ALL efficient Quartets.  
import sys
import pyparsing as pp
from itertools import combinations
import time

class UnrootedTree:
	'Holds data for an unrooted tree represented as a list of lists' 
	def __init__(self, tr):
		"""tr is a list of lists which represents the actual tree""" 
		self.tree = list(tr) 
		self.size = tsize(self.tree)
		self.nlist = node_list(self.tree)
		self.adjlist = adj_list(self.tree, self.nlist)
		self.dists, self.paths = self.all_paths()
		self.rts_list = self.all_rts()
		self.subtrees = self.all_subtrees()

	def get_nd(self, nd_id):
		"""return node from node id"""
		if nd_id >= len(self.nlist):
			print("{} is not a valid node index, print_nodes to get list of valid indices".format(nd_id))
			return None
		else:
			return self.nlist[nd_id]

	def get_adj(self, nd_id):
		"""returns set of node ids adjacent to nd_id"""
		if nd_id >= len(self.nlist):
			print("{} is not a valid node index, print_nodes to get list of valid indices".format(nd_id))
			return None
		else:
			return self.adjlist[nd_id]

	def calc_rts(self, nd_id):
		"""calculate the relative taxa set for the internal node nd (node index)"""
		if nd_id >= len(self.nlist):
			print("{} is not a valid node index, print_nodes to get list of valid indices".format(nd_id))
			return None
		rts = []
		node = self.get_nd(nd_id) 
		if not leaf(node):
			adjacent = self.get_adj(nd_id)
			for i in adjacent:
				if leaf(self.get_nd(i)):
					rts.append(i) #add directly adjacent leaves
				else:
					rts.append(self.nearest_leaf(i, nd_id)) #append nearest leaf

		#return self.map_to_nodes(rts)
		return rts
	
	def all_rts(self):
		"""precalculate rts for all nodes, return list whose ith element contains the rts 
			of the node with nd_id i
		"""
		rts_list = [[] for i in range(len(self.nlist))]
		for i in range(len(self.nlist)):
			if not leaf(self.get_nd(i)):
				rts_list[i] = self.calc_rts(i)	
		return rts_list
	
	def rts(self, nd_id):
		return self.rts_list[nd_id]
	
	def vds(self, nd_id):
		"""return the vertex defining set (2 pair combinations of rts) of a node
			indicated by nd_id, return as a list of size 2 lists
		"""
		rt_set = self.rts(nd_id)
		return [list(i) for i in combinations(rt_set, 2)]
	
	def all_subtrees(self):
		"""precalculate all subtree groups for all nodes, store them in a list whose ith element contains 
			the subtrees formed by removing the node with nd_id i
		"""
		s_trees = [[] for i in range(len(self.nlist))]
		for i in range(len(self.nlist)):
			if not leaf(self.get_nd(i)):
				adj = self.get_adj(i)
				for j in adj:
					s_trees[i].append(self.calc_subtree_nodes(j, i))
		return s_trees

	def subtree_nodes(self, nd_id):
		"""return the subtrees that occur from removing inner node nd_id"""
		return self.subtrees[nd_id]

	def calc_subtree_nodes(self, nd_id, par_id):
		"""put in a list the nodes of the subtree formed by nd_id when the branch indicated 
		   by par_id is ignored
		"""
		sub = [nd_id]
		adjacent = self.get_adj(nd_id)
		for i in adjacent:
			if i != par_id:
				if leaf(self.get_nd(i)):
					sub.append(i)
				else:
					sub.extend(self.calc_subtree_nodes(i, nd_id))
		return sub

	def quartet(self, nd1, nd2):
		"""return the quartet (as a pair of size two lists), for nodes indicated by the
		   ids nd1 and nd2
		"""
		rts1 = self.rts(nd1)
		rts2 = self.rts(nd2)
		groups1 = [set(x) for x in self.subtree_nodes(nd1)] # [set(self.subtree_nodes(x, nd1)) for x in self.get_adj(nd1)]
		groups2 = [set(x) for x in self.subtree_nodes(nd2)] #[set(self.subtree_nodes(x, nd2)) for x in self.get_adj(nd2)]
		quar = [[], []]

		for i in groups1:
			if i.issuperset(groups2[0].union(groups2[1])) or i.issuperset(groups2[1].union(groups2[2])) or i.issuperset(groups2[0].union(groups2[2])):
				#i has two groups of group2 as subset, find element of rts1 in i	
				li = list(i)
				for j in rts1: #add elements of rts that are not in i to quar[0]
					if not j in li:
						quar[0].append(j)
				break;
		for i in groups2:
			if i.issuperset(groups1[0].union(groups1[1])) or i.issuperset(groups1[1].union(groups1[2])) or i.issuperset(groups1[0].union(groups1[2])):
			#i has two groups of group1 as subset, find element of rts2 in i	
				li = list(i)
				for j in rts2: #add elements of rts that are not in i to quar[1]
					if not j in li:
						quar[1].append(j)
				break;
		return [self.map_to_nodes(x) for x in quar] 
			
	def eqs_quartets(self):
		"""return list of all efficient quartets in tree"""
		quars = []
		nd_pairs = list(combinations(range(len(self.nlist)), 2))
		for i in nd_pairs:
			if (not leaf(self.get_nd(i[0]))) and (not leaf(self.get_nd(i[1]))):
				quars.append(self.quartet(i[0], i[1]))
		return quars
	
	def linked_quartets(self):
		"""Returns list of linked system of quartets
		""" 
		nd_pairs = list(combinations(range(len(self.nlist)), 2))
		return [self.quartet(x[0], x[1]) for x in nd_pairs if self.linked_pair(x[0], x[1])]

	def linked_pair(self, nd1, nd2):
		"""Return true if node pair indicated by node ids has path length 1 between them.
		"""
		linked = False	
		if (not leaf(self.get_nd(nd1))) and (not leaf(self.get_nd(nd2))):  
			if self.dists[nd1][nd2] <= 1:
				linked = True
		'''	elif self.adj_leaves(nd1) == 2 or self.adj_leaves(nd2) == 2:
				linked = True
			elif self.single_leaf_series(nd1, nd2):
                        	linked = True
                '''
		return linked

	def single_leaf_series(self, nd1, nd2):
		"""Return true if path between nd1 and nd2 (node_ids) is a series of three 
		or more nodes with single leaf edges (this may or may not include nd1 and nd2"""
		isseries = True
		p = self.path(nd1, nd2)
		between = p[1:len(p) - 1] #get nodes between nd1 and nd2
		for i in between:
			if self.adj_leaves(i) != 1:
				isseries = False
				break
		if isseries:
			return True
		else:
			return False
			
	def adj_leaves(self, nd_id):
		"""Return number of leaves adjacent to node indicated by nd_id"""
		leaf_count = 0
		adj = self.get_adj(nd_id)
		for i in adj:
			if leaf(self.get_nd(i)): #count adjacent leaves
				leaf_count = leaf_count + 1
		return leaf_count
		
	def nearest_leaf(self, nd_id, par_nd):
		"""return the node id of nearest leaf in the subtree indicated by node id nd_id,
		   the branches of the sub tree are the adjacent nodes that are not 
		   the parent node indicated by id par_nd, this is support for finding rts"""
		branches = []
		adjacent = self.get_adj(nd_id)
		for i in adjacent:
			if i != par_nd: 
				if leaf(self.get_nd(i)):
					return i 
				else:
					branches.append(i)
		#if neither branch was a leaf, find nearest leaf for both branches, pick the closest 
		leaf1 = self.nearest_leaf(branches[0], nd_id)
		leaf2 = self.nearest_leaf(branches[1], nd_id)
	#	if self.dists[nd_id][leaf1] <= self.dists[nd_id][leaf2]:
		if self.dists[nd_id][leaf1] < self.dists[nd_id][leaf2]:
			return leaf1
		elif self.dists[nd_id][leaf1] > self.dists[nd_id][leaf2]:
			return leaf2
		elif self.adj_leaves(branches[0])==2:
			return leaf1
		elif self.adj_leaves(branches[1])==2:
			return leaf2
		else:
			return leaf1


	def path(self, u, v):
		"""Returns the shortest path from node nd1 to node nd2 (node ids)"""
		return self.paths[u][v]

	def print_nodes(self):
		"""prints the nodes in the tree and their corresponding ids"""
		print("Indices to be used for nodes in tree: ")
		for i in range(len(self.nlist)):  #print what index corresponds to which node
			print("{} = {}".format(self.nlist[i], i))

	def map_to_nodes(self, nd_ids):
		"""convert list of node indices, nd_ids to list of node representations using mapping from nlist"""
		return [self.nlist[i] for i in nd_ids]

	def leaf_map(self):
		"""return dictionary that maps leaf names to index in node list
			assumes nodes are uniquely named
		"""
		lmap = {}
		for i in range(len(self.nlist)):
			if leaf(self.nlist[i]):
				lmap[self.nlist[i]] = i
		return lmap
	
	def bf_path_search(self, u):
		"""search for all shortests paths from node id u breadth first, return distances and paths"""
		Q = [u] #a queue to hold nodes
		dists = [0 for x in range(self.size)]
		paths = [[u] for x in range(self.size)]
		notfound = list(range(self.size)) #list of all nodes id's that we have not processed yet
		notfound.remove(u)
		while Q:
			v = Q[0]  #v is current node being processed
			del Q[0]  #dequeue node
			adj = [x for x in self.get_adj(v) if x in notfound]	
			for node in adj:
				Q.append(node) #enqueue
				notfound.remove(node) 
				#distance and path from u to node is 1 more then dist/path from u to v
				dists[node] = dists[v] + 1
				paths[node] = list(paths[v])
				paths[node].append(node)
		return dists, paths
	
	def all_paths(self):
		"""Find the all pair shortest paths for the tree. Return alldists, allpaths,
			where alldists is an matrix whos ijth element stores dist between i and j, 
			allpaths is matrix whos ijth element stores an array of path from i to j
		"""
				
		alldists = [[0]*self.size for x in range(self.size)]
		allpaths = [[[] for x in range(self.size)] for y in range(self.size)]
		for i in list(range(self.size)): #find shortest path, dist for every node
			dists, paths =  self.bf_path_search(i)
			alldists[i] = dists
			allpaths[i] = paths
		return alldists, allpaths

#End class def

#**************************************************
#Supporting Methods
#*************************************************
def tparse(inp):
	"""Parse newick string into nested list form"""
	s = inp.replace(',', ' ')
	s = s.replace(';', ' ')
	num = pp.Regex(r"-?\d+(\.\d+)?")
	alp = pp.Word(pp.alphas)
	term = num | alp
	pars = pp.nestedExpr('(', ')', term)
	try:
		li = pars.parseString(s).asList()[0] 
	except pp.ParseException: #input in incorrect format
		print("Error Parsing the tree")
		li = []
	return li

def loadtree(filename):
	"""Reads in a newick string from file, returns 
		a UnrootedTree representation of string
	"""
	s = ""
	try:
		with open(filename) as f:
			s = f.read()	
	except EnvironmentError:
		print("There was an error reading the file '{}', it probably does not exist in the current directory".format(filename))

	li = tparse(s)
	if li: #if the string was in valid format 
		return UnrootedTree(li) 
	else:
		print("File could not be read, check the format of the file")
		return None	
		
def print_quartets(quars, filename = None):
	"""print quartets in (a,b)|(c,d) form
		Optionally you can print to a file by passing filename
		Defaults to printing to console
	"""
	if not filename:	#console print
		for i in quars:
			left = i[0]
			right = i[1]
			print("{},{}|{},{}".format(left[0], left[1], right[0], right[1]))
	else: #file print
		with open(filename, 'w') as f:
			for i in quars:
				left = i[0]
				right = i[1]
				f.write("{},{}|{},{}\n".format(left[0], left[1], right[0], right[1]))

def adj_list(li, nlist):
	"""Return adjacency list of li, nlist is the list of nodes in tree, 
	   the index of the node in that list is used to reference the node in
	   the adjacency list (ie. the ith node in adj list is = ith node in nlist ),	
	   ith index in adj list contains list of indices in nlist that ith node
	   is adjacent to
	"""
	indx = lambda x: nlist.index(x) #returns the index of list x in nlist
	adj = [[] for i in range(len(nlist))] #create empty adj list
	#add top two nodes to each others adjacency list
	adj[indx(li[0])].append(indx(li[1]))
	adj[indx(li[1])].append(indx(li[0]))
	#find rest of adjacent nodes
	for i in range(len(nlist)): 
		if isinstance(nlist[i], list):
		#for all child nodes of nlist[i], append child nodes to adj[i], and nlist[i] to child's adjlist entry
			for j in nlist[i]: 
				adj[i].append(indx(j)) 
				adj[indx(j)].append(i)
	return adj

#Too slow for our purposes, our trees dont have cycles, so we can find the shortest path
#faster with breadth first search
def ap_shortest_paths(li, nlist, adj, paths_only = True):
	"""Use Floyd-Warshall algorithm to find all pairs shortest paths for
		tree described by nested list li, with node list nlist, and adjacency list adj
		Can possibly return	two values (default to return only next_node):
		dist - a matrix that contains the distances
		next_node - matrix whose [i][j] elements holds the first node i travels
			        to on its shortest path to j
	"""
	verts = len(nlist)
	#begin by setting it to inf
	dist = [[float('inf') for i in range(verts)] for j in range(verts)]
	next_node = [[None for i in range(verts)] for j in range(verts)]
	for i in range(verts):
		dist[i][i] = 0	
	for i in range(verts): #set adjacent nodes to dist = 1
		for j in adj[i]:
			dist[i][j] = 1
			next_node[i][j] = j
	for k in range(verts):
		for i in range(verts):
			for j in range(verts):
				if dist[i][j] > (dist[i][k] + dist[k][j]):
					dist[i][j] = dist[i][k] + dist[k][j]
					next_node[i][j] = next_node[i][k]
	if(paths_only):
		return next_node
	else:
		return next_node, dist

#def ppath(self, u, v):
#	"""Returns the shortest path from node nd1 to node nd2 (node ids)"""
#	if self.nextnodes[u][v] == None: #check if theres a path
#		return None
#	else:
#		path_list = [u]
#		while not (u == v): #update path till we reach v
#			u = self.nextnodes[u][v]
#			path_list.append(u)
#		return path_list

def node_list(li):
	"""return a list of all nodes in tree,
		the node's index in this list is the value
		used as there index for the adjacency list
	"""
	nodes = list(li)
	for i in li: #add elements of current level into map
		if isinstance(i, list):
			nodes.extend(node_list(i))
	return nodes 
	
def tsize(t):
	"""Return number of nodes in a tree"""
	size = 0
	if not leaf(t): 
		size = size + len(t) #get num nodes in tree
		for i in t: #get size of sub trees recursivly 
			size = size + tsize(i)
	return size		

def leaf(t):
	"""tells whether node is a leaf,
		should of probably put this in sooner
	"""
	if isinstance(t, list):
		return False
	else:
		return True

def index_map(li):
	"""Returns mapping of tree nodes to integer value indices"""
	nodes = node_list(li)
	imap = dict(zip([str(i) for i in nodes], range(len(nodes)))) #keys are in string form of the node
	return imap

#deprecated method only used in tests, don't use this
def print_adjacent(li, parent = []):
	"""Print out what nodes are adjacent to a node"""
	if not parent and isinstance(li, list): #if this is first call (no parent passed in) 
		#print nodes adjacent to two parents
		print("Adjacent to {}: ".format(li[0])) 
		print(li[1])
		if(isinstance(li[0], list)):
			for i in li[0]:
				print(i)
		print( "Adjacent to {}: ".format(li[1])) 
		print(li[0])
		if(isinstance(li[1], list)):
			for i in li[1]:
				print(i)
		#print nodes adjacent for rest of nodes
		if(isinstance(li[0], list)):
			for i in li[0]:
				print_adjacent(i, li[0])
		if(isinstance(li[1], list)):
			for i in li[1]:
				print_adjacent(i, li[1])
	elif isinstance(li, list): #if child node
		print("Adjacent to {}: ".format(li)) 
		print(parent)
		for i in li:
			print(i)
		for i in li:
			print_adjacent(i, li) #print nodes adjacent for rest of nodes
	else:  #if its a single number
		print("Adjacent to {}: ".format(li))
		print(parent)

#dont use this method to print nodes, use UnrootedTree method print_nodes instead
def print_nodes_old(t):
	"""Print list of nodes in tree"""
	if isinstance(t, list):
		print("\nNodes for subtree {}".format(t))
		for i in t:
			print(i)
		for i in t:
			print_nodes(i)

#*************************************
#Main 
#*************************************
if __name__ == "__main__":
#test the methods as needed in here
#	s = raw_input("Filename: ")
#	while s:
#		tr = loadtree(s)
#		q = tr.linked_quartets()
#		print("")
#		print_quartets(q)
#		print("")
#		s = raw_input("Filename: ")
	infile = sys.argv[1]
	outfile = sys.argv[2]
	tr = loadtree(infile)
	start = time.clock()
	if len(sys.argv) > 3 and sys.argv[3] == "link":
		q = tr.linked_quartets()
	else:
		q = tr.eqs_quartets()
	print_quartets(q, outfile)
	#print("size={}".format(tr.size))
	print("Printed quartets of tree from file '{}' to the file '{}'".format(infile, outfile))
	print("The time it took to compute quartets to send to maxcut was '{}' seconds".format(time.clock()-start))
