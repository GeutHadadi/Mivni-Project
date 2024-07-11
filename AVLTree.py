#username - noamelron
#id1      - 209864123
#name1    - נעם אלרון 
#id2      - 209913623
#name2    - גאות הדדי  



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
        return None
    
    def create_virtual_child(self, dir):
        if dir == 0:
            self.left = AVLNode(None, "")
            self.left.parent = self
        elif dir == 1:
            self.right = AVLNode(None, "")
            self.right.parent = self
        return None

    def __repr__(self):
        return f"AVLNode({self.key}, '{self.value}')"

"""
A class implementing an AVL tree.
"""

class AVLTree(object):

    """
    Constructor, you are allowed to add more fields.  

    """
    def __init__(self):
        self.root = None

    """inserts a new node into the dictionary with corresponding key and value

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string 
    @param val: the value of the item
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """
    # Time complexity: O(logn), created using algorithm from class which we've confirmed to be this time complexity
    def insert(self, key, val):
        rotation = 0
        cur = self.bst_insert(key, val)
        prev = cur
        while cur != None and cur.is_real_node():
            bf = self.get_bf(cur)

            
            if abs(bf)<2 and cur.height == (max(cur.left.height, cur.right.height)+1):
                cur.size += 1
                cur = cur.parent
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
                    rotation += 1
                    cur.left = self.left_rotation(prev)
                    cur = self.right_rotation(cur)
                else: # rotate RL
                    rotation += 1
                    cur.right = self.right_rotation(prev)

                    cur = self.left_rotation(cur)

                if cur.parent is not None:
                    if cur.parent.left == last:
                        cur.parent.left = cur
                    elif cur.parent.right == last:
                        cur.parent.right = cur
                if last == self.root:
                    self.root = cur
                
                break
        while cur != None and cur.is_real_node():
            cur.size = cur.left.size + cur.right.size + 1
            cur.height = max(cur.left.height, cur.right.height) + 1
            cur = cur.parent
        return rotation

    # Time complexity: O(logn), simply iterates down the tree to the designated spot as a leaf, this is O(h) but as an AVL tree h=logn
    def bst_insert(self, key, val):
        if not self.root:
            self.root = AVLNode(key, val)
            self.root.fill_virtual_children()

            return self.root

        cur = self.root
        parent = cur
        while cur != None and cur.is_real_node(): # Reach final non leaf node
            parent = cur
            if cur.left.is_real_node() and key < cur.key:
                cur = cur.left
            elif cur.right.is_real_node and key > cur.key:
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

    def determine_rotation(self, child, criminal_bf):
        prev_bf = self.get_bf(child)
        if criminal_bf == -2: # Coming from criminals's right child
            if prev_bf == -1 or prev_bf == 0: # Coming from prev's right child aka need left rotation , 0 case refers to unique deletion case where prev is balanced but parents only left child got deleted
                return 1 
            else: # Coming from prev's left child aka right left rotation
                return 4
        
        else: # bf is 2, coming from criminals's left child 
            if prev_bf == 1 or prev_bf == 0: # Coming from prev's left child aka perform right rotation , 0 case refers to unique deletion case where prev is balanced but parents only right child got deleted
                return 2
            else: # coming from prev's right child aka left right rotation
                return 3
        

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """
    # Time complexity: O(logn), created using algorithm from class which we've confirmed to be this time complexity
    def delete(self, node):
        rotations = 0
        last = node

        if node == self.root and not node.left.is_real_node() and not node.right.is_real_node():
            self.root = None
            return rotations

        cur = self.delete_bst(node) # Given parent of physically deleted node.
            
        while cur != None and cur.is_real_node():
            bf = self.get_bf(cur)

            if abs(bf)<2 and (cur.height == max(cur.left.height, cur.right.height) + 1): # If height hasnt changed then neither has height of anyone above
                cur.size -= 1
                cur = cur.parent
                break

            elif abs(bf) < 2 and (cur.height != max(cur.left.height, cur.right.height) + 1): # If height has changed but no rotation needed go up
                cur.height = max(cur.left.height, cur.right.height) + 1
                cur.size -= 1
                cur = cur.parent

            else:
                rotations += 1
                
                if bf == -2:
                    prev = cur.right
                elif bf == 2:
                    prev = cur.left

                rot = self.determine_rotation(prev, bf)
                last = cur
                if rot == 1: # rotate left
                    cur = self.left_rotation(cur)
                elif rot == 2: # rotate right
                    cur = self.right_rotation(cur)
                elif rot == 3: # rotate LR
                    rotations += 1
                    cur.left = self.left_rotation(prev)
                    cur = self.right_rotation(cur)
                else: # rotate RL
                    rotations += 1
                    cur.right = self.right_rotation(prev)
                    cur = self.left_rotation(cur)
                if cur.parent != None:
                    if cur.parent.left == last:
                        cur.parent.left = cur
                    elif cur.parent.right == last:
                        cur.parent.right = cur
                    
                if last == self.root:
                    self.root = cur
                cur = cur.parent
        while cur != None and cur.is_real_node():
            cur.size = cur.left.size + cur.right.size + 1
            cur.height = max(cur.left.height, cur.right.height) + 1
            cur = cur.parent
        return rotations
                 
    # Time complexity: O(logn), worst case is in use of Succesor-case 3 which costs O(logn), rest of the function is O(1) so total is O(logn) worst case
    def delete_bst(self, node):
        # Given node is a real node in a tree(precondition) no need to check if node/his siblings are not None as they have to be virtual children as their parent is a real node
        parent = node.parent
        parent_physically_deleted = parent

        # Case 1, node to be deleted is a leaf, solution: simply delete node.
        if parent is not None and not node.left.is_real_node() and not node.right.is_real_node(): # Both of node's children are virtual nodes, aka node is a leaf
            node.parent = None 
            if parent.right == node: 
                parent.create_virtual_child(1)
            elif parent.left == node:
                parent.create_virtual_child(0)

        # Case 2, either only left or only right child.
        elif node.left.is_real_node() and not node.right.is_real_node(): # if it only has a left child
            if parent is not None and parent.right == node: # if node is a right child
                parent.right = node.left # stick its left child as parent's right child

            elif parent is not None and parent.left == node: # if node only has a right child
                parent.left = node.left # stick its left child as parent's left child\
            
            node.left.parent = parent
            
            if node == self.root:
                self.root = node.left

        elif not node.left.is_real_node() and node.right.is_real_node(): # if it only has a right child

            if parent is not None and parent.right == node: # if node is a right child
                parent.right = node.right # stick its right child as parent's right child
            elif parent is not None and parent.left == node: # if node only has a right child
                parent.left = node.right # stick its right child as parent's left child
            
            node.right.parent = parent

            if node == self.root:
                self.root = node.right

        elif node.left.is_real_node() and node.right.is_real_node(): # node has 2 children
            suc = self.succesor(node)
            if suc != node.right: # If succesor is the minimum node in his right child's left subtree
                parent_physically_deleted = suc.parent

                suc.parent.left = suc.right # Replace succesor with his right child, if right child doesn't exist then it must be virtual node and still works.
                suc.right.parent = suc.parent # Make succesor's right child point to suc's parent

                suc.right = node.right # Replaces node indirectly so nodes right children must be his right children
                suc.right.parent = suc # After having succesor point to node's right child, have child point to succesor 

            elif suc == node.right: # AKA Parent of physically deleted node is actually Succesor when succesor is "deleted".
                parent_physically_deleted = suc # If succesor is deleted nodes right child then succesor is effectivly their own parent

            suc.size = node.size
            suc.height = node.height

            suc.parent = parent # Successor replaces node so his new parent is nodes parent
            suc.left = node.left # Regardless of if node is directly nodes right child or not his left children(which he previously had none as successor is the minimum child) must be nodes left children
            suc.left.parent = suc

            if parent is not None:
                if parent.right == node:
                    parent.right = suc
                else:
                    parent.left = suc
            
            if node == self.root:
                self.root = suc

        return parent_physically_deleted



    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """
    # O(n) append costs O(1) amortized, theres O(n) iterations as were traveling in order over all nodes, thus total is O(n)
    def avl_to_array(self):
        arr = []
        self.avl_to_array_rec(self.root, arr)
        return arr
    
    def avl_to_array_rec(self, cur, arr):
        if(cur != None and cur.is_real_node()):
            self.avl_to_array_rec(cur.left, arr)
            arr.append((cur.key, cur.value))
            self.avl_to_array_rec(cur.right, arr)
    

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """
    def size(self):
        if self.root is not None:
            return self.root.size
        else:
            return 0


    """compute the rank of node in the dictionary

    @type node: AVLNode
    @pre: node is in self
    @param node: a node in the dictionary to compute the rank for
    @rtype: int
    @returns: the rank of node in self
    """
    # Time complexity: O(logn), created using algorithm from class which we've confirmed to be this time complexity
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
    # Time complexity: O(logn), created using algorithm from class which we've confirmed to be this time complexity
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
    # Time complexity: O(n), O(n) for calling avl_to_array and then at worst an additional O(n) if iterating over entire array, aka range is from min node key to max node key.  Total O(n)
    def max_range(self, a, b):
        max_lexi = ""
        max_key = 0
        arr = self.avl_to_array()
        i = 0
        while arr[i][0] < a:
            i += 1

        while arr[i][0] <= b:
            if arr[i][1] > max_lexi:
                max_lexi = arr[i][1]
                max_key = arr[i][0]
            i += 1

        return self.search(max_key)

    """searches for a node in the dictionary corresponding to the key

    @type key: int
    @param key: a key to be searched
    @rtype: AVLNode
    @returns: node corresponding to key
    """
    # O(logn), simply iterating at worst case from root to deepest leaf
    def search(self, key):
        p = self.root
        while p is not None and p.is_real_node():
            if p.key == key:
                return p
            if p.key < key:
                p = p.right
            else:
                p = p.left
        return None



    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """
    def get_root(self):
        return self.root

    def find_min(self, node):
        while node.is_real_node():
            node = node.left
        
        return node.parent

    # Time complexity: O(logn), created using algorithm from class which we've confirmed to be this time complexity
    def succesor(self, prev):
        if prev.right != None and prev.right.is_real_node():
            return self.find_min(prev.right)
        
        cur = prev.parent
        while cur != None and cur.is_real_node() and prev == cur.right:
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

        criminal.size = criminal.left.size + criminal.right.size + 1 # Could possibly maintain size using method in lecture 4a slide 41 for marginal improvement.
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

   
    @staticmethod
    def get_bf(node):
        return node.left.height - node.right.height

