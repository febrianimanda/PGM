"""Structure"""
example_dag = {
	'A' : {
		'desc'		: 'Winter',
		'parent'	: [],
		'child'		: ['B','C'],
		'value'		: True
	},
	'B' : {
		'desc' 	: 'Sprinkler',
		'parent'	:	['A'],
		'child'		: ['D'],
		'value'		: True
	},
	'C'	: {
		'desc'		: 'Rain',
		'parent'	: ['A'],
		'child'		: ['D', 'E'],
		'value'		: True
	},
	'D'	: {
		'desc'		: 'Wet Grass',
		'parent'	: ['B', 'C'],
		'child'		: [],
		'value'		: True
	},
	'E' : {
		'desc'		: 'Slippery Road',
		'parent'	: ['C'],
		'child'		: [],
		'value'		: True
	}
}

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
		print 'Total Nodes: %d' % self._nodeCount

	def showAllNode(self):
		print "Nodes in DAG : %s" % [x.getAlias() for x in self._listNode]

	def addNode(self, node):
		if isinstance(node, list):
			for x in node:
				self._nodeCount += 1
				self._listNode.append(x)
		else:
				self._nodeCount += 1
				self._listNode.append(node)

	# with weaknes CPT name is not flexible
	# def addCPT(self, node, givenNode, listValue):
	# 	islist = isinstance(givenNode, list)
	# 	length = 1 + (len(givenNode) if (islist == True) else 1)
	# 	name = "%s|%s" % (node.getAlias(), ''.join([x.getAlias() for x in givenNode]) if islist else givenNode.getAlias())
	# 	if 2**length == len(listValue):
	# 		self._listCPT[name] = listValue
	# 		print "CPT successfully added"
	# 	else:
	# 		print "CPT seems not properly, please try again"

	def addCPT(self, node, givenNode, listValue):
		islist = isinstance(givenNode, list)
		length = 1 + (len(givenNode) if (islist == True) else 1)
		iCPT = len(self._listCPT) + 1
		if 2**length == len(listValue):
			obj = {
				'name' : '%s given %s' % (node.getAlias(), ''.join([x.getAlias() for x in givenNode]) if islist else givenNode.getAlias()),
				'node' : node,
				'given' : givenNode,
				'value' : listValue,
			}
			self._listCPT.append(obj)
			print "CPT %s given %s successfully added" % (node.getAlias(), ''.join([x.getAlias() for x in givenNode]) if islist else givenNode.getAlias())
		else:
			print "CPT seems not properly, please try again"

	def getCPT(self, alias, given):
		return [x for x in self._listCPT if x['node'] == alias and x['given'] == given]

	def getNode(self, alias):
		for x in self._listNode:
			if x.getAlias() == alias :
				return x
		return None

	def isTrail(self, nodeA, nodeB, visited = []):
		print nodeA.getAlias(), nodeB.getAlias()
		visited = visited[:] if len(visited) == 0 else visited
		if nodeA not in visited:
			visited.append(nodeA)
			if nodeA.isHaveChild():
				for x in nodeA.getChild():
					print x.getAlias(), ' child'
					if x == nodeB :
						return True
					else:
						if self.isTrail(x, nodeB, visited) == True:
							return True
			elif nodeA.isHaveParent():
				for x in nodeA.getParent():
					print x.getAlias(), ' parent'
					if x == nodeB:
						return True
					else:
						if self.isTrail(x, nodeB, visited) == True:
							return True
		return False


class Node:
	'Common base class for Node in DAG'

	def __init__(self, alias, desc, parent = [], child = []):
		self._alias = alias
		self._desc = desc
		self._parent = child[:] if len(parent) == 0 else parent
		self._child = child[:] if len(child) == 0 else parent
		self._value = True

	# def __str__(self):
	# 	return str(self._alias)

	# def __repr__(self):
	# 	return str(self._alias)

	def addConnection(self, connection, status='child'):
		islist = (isinstance(connection, list))
		if status == 'parent' :
			if islist:
				self._parent.extend(connection)
			else:
				self._parent.append(connection)
		else:
			if islist:
				self._child.extend(connection)
			else:
				self._child.append(connection)
		if islist:
			print "Node %s: Node %s sebagai %s berhasil dihubungkan " % (self._alias, [x.getAlias() for x in connection], status)
		else:
			print "Node %s: Node %s sebagai %s berhasil dihubungkan " % (self._alias, connection.getAlias(), status)
		# print "Node %s sebagai %s berhasil dihubungkan " % (connection, status)
		
	def setValue(self, value):
		self._value = value

	def getAlias(self):
		return self._alias

	def getDesc(self):
		return self._desc

	def getParent(self):
		return self._parent

	def getChild(self):
		return self._child	

	def isHaveChild(self):
		return len(self._child) != 0

	def isHaveParent(self):
		return len(self._parent) != 0

	def showChild(self):
		print [node.getAlias() for node in self._child]

	def showParent(self):
		print [node.getAlias() for node in self._parent]

dag = DAG()
A = Node('A', 'Winter')
B = Node('B', 'Sprinkler', [A])
C = Node('C', 'Rain', [A])
D = Node('D', 'Wet Grass', [B,C])
E = Node('E', 'Slippery Road', [C])

A.addConnection([B,C])
B.addConnection(D)
C.addConnection(E)

dag.addNode([A,B,C,D,E])
dag.showAllNode()
dag.addCPT(B,A,[.2, .8, .75, .25])
dag.addCPT(E,C,[.7, .3, 0, 1])
dag.addCPT(C,A,[.8, .2, .1, .9])
dag.addCPT(D,[B,C],[.95, .05, .9, .1, .8, .2, 0, 1])