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