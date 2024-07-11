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
        return None
    
    def create_virtual_child(self, dir):
        if dir == 0:
            self.left = AVLNode(None, "")
            self.left.parent = self
        elif dir == 1:
            self.right = AVLNode(None, "")
            self.right.parent = self
        return None

    def __str__(self): # Change to str
        return f"AVLNode({self.key}, {self.value}, Height: {self.height}, Size: {self.size})"

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


    def __repr__(self):  # you don't need to understand the implementation of this method
        def printree(root):
            if not root or not root.is_real_node():
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
            #print(f"cur node: {cur}, bf: {bf}, height: {cur.height}, legit height: {max(cur.left.height, cur.right.height)+1}")

            
            if abs(bf)<2 and cur.height == (max(cur.left.height, cur.right.height)+1):
                cur.size += 1
                cur = cur.parent
                break
            elif abs(bf) < 2 and cur.height != (max(cur.left.height, cur.right.height)+1):
                #print(f"cur node: {cur}, going up to {cur.parent}")
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

    def delete(self, node):
        rotations = 0
        last = node

        if node == self.root and not node.left.is_real_node() and not node.right.is_real_node():
            self.root = None
            return rotations

        cur = self.delete_bst(node) # Given parent of physically deleted node.

        #print()
        #print(f"Deleting {node}, parent of whos actually being deleted {cur}")
            
        while cur != None and cur.is_real_node():
            bf = self.get_bf(cur)
            #print(f"cur: {cur}, bf: {bf}")
            #print(f"cur height: {cur.height}, legit height: {max(cur.left.height, cur.right.height) + 1}")

            if abs(bf)<2 and (cur.height == max(cur.left.height, cur.right.height) + 1): # If height hasnt changed then neither has height of anyone above
                #print(f"stopping at {cur}")
                cur.size -= 1
                cur = cur.parent
                break

            elif abs(bf) < 2 and (cur.height != max(cur.left.height, cur.right.height) + 1): # If height has changed but no rotation needed go up
                #print(f"going to {cur} parent {cur.parent}")
                cur.height = max(cur.left.height, cur.right.height) + 1
                cur.size -= 1
                cur = cur.parent

            else:

                #print(f"performing rotation on {cur}")
                #print(f"cur left height: {cur.left}, cur right height: {cur.right}")
                rotations += 1
                
                if bf == -2:
                    prev = cur.right
                elif bf == 2:
                    prev = cur.left
                
                rot = self.determine_rotation(prev, bf)
                #print(f"\n\nRotation: {rot}")
                #print(cur)
                #print(self.root)
                last = cur
                if rot == 1: # rotate left
                    cur = self.left_rotation(cur)
                    #print(cur)
                elif rot == 2: # rotate right
                    cur = self.right_rotation(cur)
                elif rot == 3: # rotate LR
                    rotations += 1
                    #print(f"\nPerforming LR rotation.")
                    cur.left = self.left_rotation(prev)
                    #print(f"{cur.left}\n")
                    cur = self.right_rotation(cur)
                    #print(cur)
                else: # rotate RL
                    rotations += 1
                    cur.right = self.right_rotation(prev)
                    cur = self.left_rotation(cur)
                    #print(f"AFTER ROTATION: {cur}")
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
                 
        
    def delete_bst(self, node):
        # Given node is a real node in a tree(precondition) no need to check if node/his siblings are not None as they have to be virtual children as their parent is a real node
        parent = node.parent
        parent_physically_deleted = parent

        #print(f"Node: {node}, left child: {node.left}, right child: {node.right}")


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
                #print(f"new root is {node.left}")
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
    def avl_to_array_rec(self, cur, arr):
        if(cur != None and cur.is_real_node()):
            self.avl_to_array_rec(cur.left, arr)
            arr.append((cur.key, cur.value))
            self.avl_to_array_rec(cur.right, arr)
        
    def avl_to_array(self):
        arr = []
        self.avl_to_array_rec(self.root, arr)
        return arr


    def size(self):
        return self.root.size


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
    
    def find_min(self, node):
        while node.is_real_node():
            node = node.left
        
        return node.parent

    
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
        
    def search(self, key):
        p = self.root
        while p is not None and p.is_real_node():
            if p.key == key:
                return p
            elif p.key < key:
                p = p.right
            else:
                p = p.left
        return p
    @staticmethod
    def get_bf(node):
        return node.left.height - node.right.height


def build_balanced(n):
    tree = AVLTree()
    create_balanced_tree(tree, 2**(n-1), 0, 2**n)
    return tree

def create_balanced_tree(tree, n, depth, orig):
    if 2**depth == orig:
        return
    tree.insert(n, f"Node {n}")
    #print(f"n: {n}, orig: {orig}, depth: {depth}, n-orig//2**depth: {n-(orig//(2**(depth+2)))}, n+orig//2**depth: {n+(orig//(2**(depth+2)))}")
    create_balanced_tree(tree, n-(orig//(2**(depth+2))), depth + 1, orig)
    create_balanced_tree(tree, n+(orig//(2**(depth+2))), depth + 1, orig)


def test():
    tree = build_balanced(3)
    tree.insert(8, "Node 8")
    tree.insert(0, "Node 0")
    print("\n\n\n")
    print(tree)
    avl_array = tree.avl_to_array()
    for node in avl_array:
        print(node)

def test2():
    tree = AVLTree()
    operations = [
    ('insert', 0, 1), ('insert', 0, 2)
]

    # Perform operations on the AVL tree
    for operation in operations:
        action, _, value = operation
        if action == 'insert':
            tree.insert(value, "")
        elif action == 'delete':
            node = tree.search(value)
            if node:
                tree.delete(node)

        # Print tree and array representation after each operation
        print()
        print(tree)
        print(tree.avl_to_array())
        print()

    
if __name__ == "__main__":
    # avltree = AVLTree()
    # # printree(avltree.root)
    # avltree.insert(5, "Node 1")
    # #print(avltree.size())
    # avltree.insert(7, "Node 2")
    # #print(avltree.size())
    # avltree.insert(4, "Node 3")
    # #print(avltree.size())
    # avltree.insert(8, "Node 4")
    # #print(avltree.size())
    # avltree.insert(10, "Node 5")
    # #print(avltree.size())
    # avltree.delete(avltree.search(10))
    # print(avltree)
    # avl_array = avltree.avl_to_array()
    # for node in avl_array:
    #     print(f"Node: {node}, size: {node.size}, height: {node.height}")
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
    test2()