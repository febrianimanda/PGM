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
		print 'Total Nodes: %d' % self._nodeCount

	def showAllNode(self):
		# print "Nodes in DAG : %s" % [x['node'].getAlias() for x in self._listNode]
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
		print "Node %s: Node %s sebagai %s berhasil dihubungkan " % (node, connection, status)

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

	def isTrail(self, nodeA, nodeB, visited = []):
		visited = visited[:] if len(visited) == 0 else visited
		if nodeA not in visited:
			visited.append(nodeA)
			if nodeA.isHaveChild():
				for x in nodeA.getChild():
					if x == nodeB :
						return True
					else:
						if self.isTrail(x, nodeB, visited):
							return True
			elif nodeA.isHaveParent():
				for x in nodeA.getParent():
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

	def isHaveParent(self):
		return len(self._parent) != 0

	def showFromNode(self, node, things):
		obj = self.getNode(node)
		if obj != None:
			print 'Child Node %s : %s' % (node, obj[things])
		else:
			print 'Node tidak ditemukan'

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

dag.addNode([a,b,c,d,e])
dag.addConnection(a,[b,c])
dag.addConnection(b,a,'parent')
dag.addConnection(b,d)
dag.addConnection(c,a,'parent')
dag.addConnection(c,d)
dag.addConnection(d,[b,c],'parent')
dag.addConnection(c,e)
dag.addConnection(e,c,'parent')
dag.showAllNode()
dag.showFromNode(a, 'child')

# dag.addCPT(B,A,[.2, .8, .75, .25])
# dag.addCPT(E,C,[.7, .3, 0, 1])
# dag.addCPT(C,A,[.8, .2, .1, .9])
# dag.addCPT(D,[B,C],[.95, .05, .9, .1, .8, .2, 0, 1])