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

class DAG:
	'Common base class for Directed Acyclid Graph'

	def __init__(self):
		self._nodeCount = 0
		self._listNode = []

	def showNodeCounter(self):
		print 'Total Nodes: %d' % self._nodeCount

	def showAllNode(self):
		print self._listNode

	def addNode(self, node):
		self._nodeCount += 1
		self._listNode.append(node)

class Node:
	'Common base class for Node in DAG'

	def __init__(self, alias, desc, parent = [], child = []):
		self._alias = alias
		self._desc = desc
		self._parent = parent
		self._child = child
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


A = Node('A', 'Winter')
B = Node('B', 'Sprinkler', [A])
C = Node('C', 'Rain', [A])
D = Node('D', 'Wet Grass', [B,C])
E = Node('E', 'Slippery Road', [C])

A.addConnection([B,C])
# B.addConnection(D)
# C.addConnection([D,E])
# D.addConnection([B,C], 'parent')
# E.addConnection(C, 'parent')
D.showParent()



