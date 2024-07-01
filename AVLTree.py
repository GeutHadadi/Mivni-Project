#username - complete info
#id1      - complete info 
#name1    - complete info 
#id2      - complete info
#name2    - complete info  



"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int or None
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		self.size = 0
		

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return False



"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self):
		self.root = None
		self.size = 0


	"""searches for a node in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key
	"""
	def search(self, key):
		p = self.root
		while p is not None:
			if p.key == key:
				return p
			if p.key < key:
				p = p.right
			else:
				p = p.left
		return None


	"""inserts a new node into the dictionary with corresponding key and value

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string 
	@param val: the value of the item
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""

	def left_rotation(self, criminal):
		new_root = criminal.right
		new_root.parent = criminal.parent
		criminal.parent = new_root
		criminal.right = new_root.left
		criminal.right.parent = criminal
		new_root.left = criminal

		criminal.height = max(criminal.left.height, criminal.right.height) + 1
		new_root.height = max(new_root.left.height, new_root.right.height) + 1

		return new_root


	def right_rotation(self, criminal):
		new_root = criminal.left
		new_root.parent = criminal.parent
		criminal.parent = new_root
		criminal.left = new_root.right
		criminal.left.parent = criminal
		new_root.right = criminal

		criminal.height = max(criminal.left.height, criminal.right.height)+1
		new_root.height = max(new_root.left.height, new_root.right.height)+1

		return new_root


	def bst_insert(self, key, val):
		cur = self.root
		while True: # Reach final non leaf node
			if key < cur.key and cur.left.key != "":
				cur = cur.left
			elif key > cur.key and cur.right.key != "":
				cur = cur.right
			else: # Key is assumed not to exist in tree thus only option is one of the children's keys is ""
				break

		if key > cur.key:
			cur.right = AVLNode(key,val)
		else:
			cur.left = AVLNode(key,val)

		return


	def insert(self, key, val):
		rotation = 0


		return -1


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, node):
		return -1


	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		return None


	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return -1	


	"""compute the rank of node in the dictionary

	@type node: AVLNode
	@pre: node is in self
	@param node: a node in the dictionary to compute the rank for
	@rtype: int
	@returns: the rank of node in self
	"""
	def rank(self, node):
		return -1


	"""finds the i'th smallest item (according to keys) in the dictionary

	@type i: int
	@pre: 1 <= i <= self.size()
	@param i: the rank to be selected in self
	@rtype: AVLNode
	@returns: the node of rank i in self
	"""
	def select(self, i):
		return None


	"""finds the node with the largest value in a specified range of keys

	@type a: int
	@param a: the lower end of the range
	@type b: int
	@param b: the upper end of the range
	@pre: a<b
	@rtype: AVLNode
	@returns: the node with maximal (lexicographically) value having a<=key<=b, or None if no such keys exist
	"""
	def max_range(self, a, b):
		return None


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return None
