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
		return self.key != None

	def fill_virtual_children(self):
		self.left = AVLNode(None, "")
		self.right = AVLNode(None, "")
		self.left.parent = self
		self.right.parent = self

	def __repr__(self):
		return f"AVLNode({self.key}, {self.value})"

"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self):
		self.root = None


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
		return p


	"""inserts a new node into the dictionary with corresponding key and value

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string 
	@param val: the value of the item
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""

	def insert(self, key, val):
		rotation = 0
		cur = self.bst_insert(key, val)
		prev = cur
		while cur != None and cur.is_real_node():
			bf = self.get_bf(cur)
			if abs(bf)<2 and cur.height == (max(cur.left.height, cur.right.height)+1):
				break
			elif abs(bf) < 2 and cur.height != (max(cur.left.height, cur.right.height)+1):
				cur.height = (max(cur.left.height, cur.right.height)+1)
				cur.size += 1
				prev = cur
				cur = cur.parent
			else:
				rotation += 1
				rot = self.determine_rotation(prev, bf)
				last = cur
				if rot == 1: # rotate left
					cur = self.left_rotation(cur)
				elif rot == 2: # rotate right
					cur = self.right_rotation(cur)
				elif rot == 3: # rotate LR
					cur.left = self.left_rotation(prev)
					cur = self.right_rotation(cur)
				else: # rotate RL
					cur.right = self.right_rotation(prev)

					cur = self.left_rotation(cur)
				
				if last == self.root:
					self.root = cur

				if cur.parent != None:
					if cur.parent.left == last:
						cur.parent.left = cur
					elif cur.parent.right == last:
						cur.parent.right = cur

				break
		
		self.root.size = self.root.left.size + self.root.right.size + 1
		self.root.height = max(self.root.left.height, self.root.right.height) + 1
		return rotation


	def determine_rotation(self, child, criminal_bf):
		prev_bf = self.get_bf(child)
		if criminal_bf == -2: # Coming from criminals's right child
			if prev_bf == -1: # Coming from prev's right child aka need left rotation
				return 1 
			else: # Coming from prev's left child aka right left rotation
				return 4
		
		else: # bf is 2, coming from criminals's left child 
			if prev_bf == 1: # Coming from prev's left child aka perform right rotation
				return 2
			else: # coming from prev's right child aka left right rotation
				return 3
		

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
	def avl_to_array_rec(self, cur, arr):
		if(cur.is_real_node()):
			self.avl_to_array_rec(cur.left, arr)
			print(cur)
			arr.append(cur)
			self.avl_to_array_rec(cur.right, arr)
		
	def avl_to_array(self):
		arr = []
		self.avl_to_array_rec(self.root, arr)
		return arr


	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return self.root.size


	"""compute the rank of node in the dictionary

	@type node: AVLNode
	@pre: node is in self
	@param node: a node in the dictionary to compute the rank for
	@rtype: int
	@returns: the rank of node in self
	"""
	def rank(self, node):
		count=(node.left.size+1)
		prev= node
		cur = node.parent
		if node.parent == None:
			return count


		while cur != None and cur.is_real_node():
			if (prev == cur.right):
				count += (cur.left.size+1)	
			prev = cur
			cur = cur.parent
		return count


	"""finds the i'th smallest item (according to keys) in the dictionary

	@type i: int
	@pre: 1 <= i <= self.size()
	@param i: the rank to be selected in self
	@rtype: AVLNode
	@returns: the node of rank i in self
	"""
	def select(self, i):
		return self.select_rec(self.root, i)
	
	def select_rec(self, cur, i):
		small_or_eq = cur.left.size+1
		if i==small_or_eq: # than there are small_or_eq items <= i as needed
			return cur
		elif i<small_or_eq: # than there are still some items that are > i
			return self.select_rec(cur.left, i) # maybe in the left subtree
		else: # i>rk - there are too few items that are <= i
			return self.select_rec(cur.right, i-small_or_eq) # maybe in the right subtree we can increse the number
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
		max_lexi = ""
		max_key = 0
		arr = self.avl_to_array()
		i=0
		while arr[i][0]<a:
			i+=1

		while arr[i][0]<=b:
			if arr[i][1] > max_lexi:
				max_lexi = arr[i][1]
				max_index = arr[i][0]
			i+=1

		return self.search(max_key)

	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root
	
	def predecessor(self, prev):
		if prev.left != None and prev.left.is_real_node():
			return self.find_max(prev.left)
		
		cur = prev.parent
		while cur.is_real_node() and prev == cur.left:
			prev = cur
			cur = cur.parent
		
		return cur
	
	def find_max(self, node):
		while node.is_real_node()	:
			node = node.max
		
		return node.parent
	
	def find_min(self, node):
		while node.is_real_node():
			node = node.left
		
		return node.parent

	
	def succesor(self, prev):
		if prev.right != None and prev.right.is_real_node():
			return self.find_min(prev.right)
		
		cur = prev.parent
		while cur.is_real_node() and prev == cur.right:
			prev = cur
			cur = cur.parent
		
		return cur

	def left_rotation(self, criminal):
		new_root = criminal.right
		new_root.parent = criminal.parent
		criminal.parent = new_root
		criminal.right = new_root.left
		criminal.right.parent = criminal
		new_root.left = criminal

		criminal.height = max(criminal.left.height, criminal.right.height) + 1
		new_root.height = max(new_root.left.height, new_root.right.height) + 1

		criminal.size = criminal.left.size + criminal.right.size + 1
		new_root.size = new_root.left.size + new_root.right.size + 1
		
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
		
		criminal.size = criminal.left.size + criminal.right.size + 1
		new_root.size = new_root.left.size + new_root.right.size + 1

		return new_root


	def bst_insert(self, key, val):
		if self.root == None:
			self.root = AVLNode(key, val)
			self.root.fill_virtual_children()

			return self.root

		cur = self.root
		parent = cur
		while cur.is_real_node(): # Reach final non leaf node
			parent = cur
			if cur.left != None and cur.left.is_real_node() and key < cur.key:
				cur = cur.left
			elif cur.right != None and cur.right.is_real_node and key > cur.key:
				cur = cur.right
			else: # Key is assumed not to exist in tree thus only option is one of the children's keys is ""
				break
		
		cur = parent
		if key > cur.key:
			cur.right = AVLNode(key,val)
			cur.right.parent = cur
			cur.right.fill_virtual_children()
			return cur.right
		else:
			cur.left = AVLNode(key,val)
			cur.left.parent = cur
			cur.left.fill_virtual_children()
			return cur.left


	@staticmethod
	def change__height(self, cur):
		parent = cur.parent
		height_changed = True
		while parent.key != "" and height_changed:
			"""
			Three options before insertion for height changes:
			1) Left and right children have same height, thus if coming from left child it must be that
			"""
			if cur == parent.left: 
				if parent.left.height > parent.right.height:
					parent.height+=1
				else:
					height_changed = False
			else: # came from the right
				if parent.right.height > parent.left.height:
					parent.height+=1
				else:
					height_changed = False


	@staticmethod
	def get_bf(node):
		return node.left.height - node.right.height


def printree(root):
	if not root:
		return ["#"]

	root_key = str(root.key)
	left, right = printree(root.left), printree(root.right)

	lwid = len(left[-1])
	rwid = len(right[-1])
	rootwid = len(root_key)

	result = [(lwid + 1) * " " + root_key + (rwid + 1) * " "]

	ls = len(left[0].rstrip())
	rs = len(right[0]) - len(right[0].lstrip())
	result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "\\" + rs * "_" + (rwid - rs) * " ")

	for i in range(max(len(left), len(right))):
		row = ""
		if i < len(left):
			row += left[i]
		else:
			row += lwid * " "
			
		row += (rootwid + 2) * " "

		if i < len(right):
			row += right[i]
		else:
			row += rwid * " "

		result.append(row)

		return result

	return '\n'.join(printree(self.root))

	

if __name__ == "__main__":
    avltree = AVLTree()
    # printree(avltree.root)
    avltree.insert(5, "Node 1")
    #print(avltree.size())
    avltree.insert(7, "Node 2")
    #print(avltree.size())
    avltree.insert(4, "Node 3")
    #print(avltree.size())
    avltree.insert(8, "Node 4")
    #print(avltree.size())
    avltree.insert(10, "Node 5")
    #print(avltree.size())
    print(avltree.avl_to_array())
    #print(avltree.size())
    # print()
    # print("avl tree search 8 output:")
    # node = avltree.search(8)

    # print(avltree.rank(node))
    # print(f"Root: {avltree.root}, size: {avltree.root.size}")
    # print(f"Root left: {avltree.root.left} size: {avltree.root.left.size}")
    # print(f"Root right: {avltree.root.right} size: {avltree.root.right.size}")
    # print(f"Root right.left: {avltree.root.right.left} size: {avltree.root.right.left.size}")
    # print(f"Root right.right: {avltree.root.right.right} size: {avltree.root.right.right.size}")
    