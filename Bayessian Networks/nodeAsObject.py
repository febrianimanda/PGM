"""Structure"""
example_dag = [
	{
		'node' : {
			'alias'	: 'A',
			'desc'	: 'Winter',
			'value'	: True
		},
		'parent' 	: [],
		'child'		: ['B','C']
	},
	{
		'B' : {
			'alias'	: 'B',
			'desc' 	: 'Sprinkler',
			'value'	: True
		},
		'parent'	:	['A'],
		'child'		: ['D'],
	},
	{
		'C'	: {
			'alias'	: 'C',
			'desc'	: 'Rain',
			'value'	: True
		},
		'parent'	: ['A'],
		'child'		: ['D', 'E'],
	},
	{
		'D'	: {
			'alias'	: 'D',
			'desc'	: 'Wet Grass',
			'value'	: True
		},
		'parent'	: ['B', 'C'],
		'child'		: [],
	},
	{
		'E' : {
			'alias'	: 'E',
			'desc'	: 'Slippery Road',
			'value'	: True
		},
		'parent'	: ['C'],
		'child'		: [],
	}
]

example_CPT = [

	{
		'node'	: 'A',
		'given'	: None,
		'value'	: [.6, .4]
	},
	{
		'node'	: 'B',
		'given'	: 'A',
		'value'	: [.2, .8, .75, .25]
	},
	{
		'node'	: 'E',
		'given'	: 'C',
		'value'	: [.7, .3, 0, 1]
	},
	{
		'node'	: 'C',
		'given'	: 'A',
		'value'	: [.8, .2, .1, .9]
	},
	{
		'node'	: 'D',
		'given'	: '[B,C]',
		'value'	: [.95, .05, .9, .1, .8, .2, 0, 1]
	}
]

class DAG:
	'Common base class for Directed Acyclid Graph'

	def __init__(self, listNode = []):
		self._nodeCount = 0
		self._listNode = listNode[:] if len(listNode) == 0 else listNode
		self._listCPT = []

	def showNodeCounter(self):
		print 'Total Nodes in DAG: %d' % self._nodeCount

	def showAllNode(self):
		for i in self._listNode:
			print i

	def addNode(self, node):
		if isinstance(node, list):
			for x in node:
				obj = { 'node': x, 'parent': [], 'child': [] }
				self._nodeCount += 1
				self._listNode.append(obj)
		else:
				obj = { 'node': node, 'parent': [], 'child': [] }
				self._nodeCount += 1
				self._listNode.append(obj)

	def addConnection(self, node, connection, status='child'):
		islist = isinstance(connection, list)
		if status == 'parent' :
			if islist:
				self.getNode(node)['parent'].extend(connection)
			else:
				self.getNode(node)['parent'].append(connection)
		else:
			if islist:
				self.getNode(node)['child'].extend(connection)
			else:
				self.getNode(node)['child'].append(connection)
		print "Node %s: Node %s as %s successfully connected " % (node, connection, status)

	def addCPT(self, node, givenNode, listValue):
		islist = isinstance(givenNode, list)
		length = 1 + (len(givenNode) if (islist == True) else 1)
		iCPT = len(self._listCPT) + 1
		if 2**length == len(listValue):
			obj = {
				'name' : '%s|%s' % (node, ''.join([x.getAlias() for x in givenNode]) if islist else givenNode.getAlias()),
				'node' : node, 'given' : givenNode, 'value' : listValue,
			}
			self._listCPT.append(obj)
			print "CPT %s|%s successfully added" % (node, ''.join([x.getAlias() for x in givenNode]) if islist else givenNode.getAlias())
		else:
			print "CPT seems not properly, please try again"

	def getAllCPT(self):
		return self._listCPT

	def getCPT(self, node, given):
		return [x for x in self._listCPT if x['node'] == node and x['given'] == given]

	def isTrail(self, nodeA, nodeB, visited = []):
		visited = visited[:] if len(visited) == 0 else visited
		if nodeA not in visited:
			visited.append(nodeA)
			if self.isNodeHave(nodeA, 'child'):
				for x in self.getNode(nodeA)['child']:
					if x == nodeB :
						return True
					else:
						if self.isTrail(x, nodeB, visited):
							return True
			elif self.isNodeHave(nodeA, 'parent'):
				for x in self.getNode(nodeA)['parent']:
					if x == nodeB:
						return True
					else:
						if self.isTrail(x, nodeB, visited):
							return True
		return False

	def getNode(self, alias):
		for x in self._listNode:
			if x['node'] == alias :
				return x
		return None

	def getFromNode(self, node, things = 'child'):
		obj = self.getNode(node)
		if obj != None:
			return obj[things]
		return None

	def isNodeHave(self, node, things='child'):
		obj = self.getNode(node)
		if obj != None:
			return len(obj[things]) != 0
		return False

	def showFromNode(self, node, things):
		obj = self.getNode(node)
		if obj != None:
			print 'Child Node %s : %s' % (node, obj[things])
		else:
			print 'Node tidak ditemukan'

	def showAllCPT(self):
		for x in self._listCPT:
			print x

	def encodes(self, fd):
		for i in fd:
			if isinstance(i, list):
				if self.getNode(i[0]) == None:
					self.addNode(i[0])
				if isinstance(i[1], list):
					for j in i[1]:
						if self.getNode(j) == None:
							self.addNode(j)
						self.addConnection(j, i[0])
				else:
					if self.getNode(i[1]) == None:
						self.addNode(i[0])
					self.addConnection(i[1], i[0])
				self.addConnection(i[0],i[1], 'parent')
			else:
				self.addNode(i)

class Node:
	'Common base class for Node in DAG'

	def __init__(self, alias, desc):
		self._alias = alias
		self._desc = desc
		self._value = True

	def __str__(self):
		return self._alias

	def __repr__(self):
		return self._alias
		
	def setValue(self, value):
		self._value = value

	def getAlias(self):
		return self._alias

	def getDesc(self):
		return self._desc


dag = DAG()
a = Node('A', 'Winter')
b = Node('B', 'Sprinkler')
c = Node('C', 'Rain')
d = Node('D', 'Wet Grass')
e = Node('E', 'Slippery Road')

enc = [a,[b,a],[c,a],[d,[b,c]],[e,c]]
dag.encodes(enc)
dag.showAllNode()
dag.addCPT(b,a,[.2, .8, .75, .25])
dag.addCPT(e,c,[.7, .3, 0, 1])
dag.addCPT(c,a,[.8, .2, .1, .9])
dag.addCPT(d,[b,c],[.95, .05, .9, .1, .8, .2, 0, 1])