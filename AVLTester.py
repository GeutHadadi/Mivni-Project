""" In order to run the tester:
    1.  Make sure your AVLTree.py file and AVLTreeTester2022.py
        file are both in the same directory.
    2.  Run your AVLTree.py file
    3.  Run the AVLTreeTester2022.py file
    4.  Your grade should be written in the terminal.
        Only failed tests will be presented in the terminal,
        together with the AssertionError that made them fail.
    5. MAKE SURE YOU HAVE GET FUNCTIONS ADDED!
        
        
    Note: if you want to see the time each test took, add the following commands:
    1. Add this to def setUp(cls) method - cls.start_time = time.time()
    2. Add this method:
        def tearDown(self):
            t = time.time() - self.start_time
            print("%s: %.3f " % (self.id()[31:], t))
"""

import time
import unittest, random
import numpy as np

from AVLTree import AVLTree, AVLNode


GRADE = 0
MAX_GRADE = 70
NUMBER_OF_TESTS = 32
PASSED_TESTS = 0


class AVLTreeTester2022(unittest.TestCase):

    @staticmethod
    def add_points(x: float, is_the_test_finished=True):
        global GRADE, PASSED_TESTS
        GRADE += x
        if is_the_test_finished:
            PASSED_TESTS += 1

    # @staticmethod
    # def in_order(tree: AVLTree):
    #     lst = []

    #     def in_order_rec(node: AVLNode, in_order_lst: list[str]):
    #         if node is not None and node.is_real_node():
    #             in_order_rec(node.left, in_order_lst)
    #             in_order_lst.append(node.value)
    #             in_order_rec(node.right, in_order_lst)

    #     in_order_rec(tree.root, lst)
    #     return lst

    @classmethod
    def setUp(cls):
        cls.tree = AVLTree()
        cls.tree_2 = AVLTree()

    @staticmethod
    def create_tree(values, random_order=False):
        if random_order:
            random.shuffle(values)
        tree = AVLTree()
        for val in values:
            tree.insert(val, str(val))
        return tree

    def test_basic_avl_node_get(self):
        self.tree.insert(2, "2")
        self.tree.insert(1, "1")  #    '2'
        self.tree.insert(3, "3")  # '1'   '3'
        root = self.tree.root
        self.assertTrue(root.is_real_node(), "FAIL - root should be a real node")
        self.assertEqual(root.height, 1)
        self.assertTrue(root.left.is_real_node())
        self.assertTrue(root.right.is_real_node())
        self.assertEqual(root.left.height, 0)
        self.assertEqual(root.right.height, 0)
        self.assertEqual(root.left.parent, root)
        self.assertEqual(root.right.parent, root)
        self.add_points(20)

    def test_empty_tree(self):
        self.assertTrue(
            self.tree.size() == 0,
            "FAIL - tree.empty() on a new tree should return True",
        )
        self.add_points(2)

    def test_left_rotation_after_deletion(self):
        # Example from slide 84 in AVL tree presentation from moodle
        avl_tree = self.create_tree([30, 25, 35, 40])
        self.assertEqual(
            1,
            avl_tree.delete(avl_tree.search(25)),
            "FAIL in left rotation after deletion",
        )
        self.add_points(0.5)

    def test_right_left_rotation_after_deletion(self):
        # Example from slide 84 in AVL tree presentation from moodle
        avl_tree = self.create_tree([9, 8, 11, 10])
        self.assertEqual(
            2,
            avl_tree.delete(avl_tree.search(8)),
            "FAIL in right-left rotation after deletion",
        )
        self.add_points(0.5)

    def test_left_right_rotation_after_deletion(self):
        # Example from slide 84 in AVL tree presentation from moodle
        avl_tree = self.create_tree([10, 8, 11, 9])
        self.assertEqual(
            2,
            avl_tree.delete(avl_tree.search(11)),
            "FAIL in left-right rotation after deletion",
        )
        self.add_points(0.5)

    def test_right_rotation_after_deletion(self):
        # Example from slide 84 in AVL tree presentation from moodle
        avl_tree = self.create_tree([3, 2, 4, 1])
        self.assertEqual(
            1,
            avl_tree.delete(avl_tree.search(4)),
            "FAIL in right rotation after deletion",
        )
        self.add_points(0.5)

    def test_single_rotations_on_linear_insertions_and_deletions(
        self,
    ):  # TODO CHECK THIS

        avl_tree = AVLTree()

        self.assertEqual(
            0,
            avl_tree.insert(1, "1"),
            "FAIL - after inserting one node into an empty tree, zero rotations should be done",
        )
        self.assertEqual(
            1,
            avl_tree.insert(2, "2"),
            "FAIL - after inserting 1 ,2  into an empty tree, zero rotations and one height change should be done",
        )
        self.assertEqual(
            2,
            avl_tree.insert(3, "3"),
            "FAIL - after inserting 1 ,2 , 3 into an empty tree, 1 rotation and one height changeshould be done",
        )
        self.assertEqual(
            2,
            avl_tree.insert(4, "4"),
            "FAIL - after inserting 4 into a tree that had 1 ,2 ,3 inserted prior, zero rotations and 2 height changes should be done",
        )
        self.assertEqual(
            2,
            avl_tree.insert(5, "5"),
            "FAIL - after inserting 5 into a tree that had 1 ,2 ,3 ,4 inserted prior, 1 rotation should be done and one height change should be done",
        )
        self.add_points(0.5, False)

        for i in range(6, 13):
            avl_tree.insert(i, str(i))

        avl_tree.delete(avl_tree.search(9))
        self.assertEqual(
            0,
            avl_tree.delete(avl_tree.search(11)),
            "FAIL - after inserting 1 ,2 ,3 ,4 ,5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 and then deleting 9 and 11, zero rotations should be done on second deletion",
        )
        self.add_points(0.5)

    def test_delete_operations_simple_1(self):
        self.tree.insert(2, "2")
        self.tree.insert(1, "1")
        self.tree.insert(3, "3")
        #   2
        # 1   3
        self.assertEqual(
            self.tree.delete(self.tree.search(1)),
            0,
            "FAIL - deleting '1' should cost 0 re-balancing op",
        )
        self.assertEqual(
            self.tree.delete(self.tree.search(3)),
            1,
            "FAIL - deleting '3' should cost 1 re-balancing op",
        )
        self.assertEqual(
            self.tree.delete(self.tree.search(2)),
            0,
            "FAIL - deleting '2' should cost 0 re-balancing op",
        )
        self.add_points(0.5)

    def test_delete_operations_simple_2(self):
        # From slide 90 in AVL presentatin from moodle
        avl_tree = self.create_tree([15, 8, 22, 4, 20, 11, 24, 2, 18, 9, 12, 13])

        self.assertEqual(
            avl_tree.size(),
            12,
            "FAIL - Before deletion, size of tree from slide 90 in AVL presentation should be 12",
        )
        self.assertEqual(
            15,
            avl_tree.root.key,
            "FAIL - Before deletion, root of tree from slide 90 in AVL presentation should be 15",
        )

        self.add_points(1, False)

        # Delete root
        self.assertEqual(3, avl_tree.delete(avl_tree.search(24)))
        self.assertEqual(
            avl_tree.root.key,
            11,
            "FAIL - After deleting 24 in tree from slide 90 in AVL presentation, root should be 11",
        )
        self.add_points(1, False)

        self.assertEqual(
            3,
            avl_tree.root.height,
            "FAIL - After deleting 24 in tree from slide 90 in AVL presentation, root height should be 3",
        )
        self.add_points(1)

    def test_do_10000_insertions_and_deletions(self):
        avl_tree = AVLTree()
        for i in range(10000):
            avl_tree.insert(i, "num" + str(i))

        # Check tree size after insertions
        self.assertEqual(
            avl_tree.size(),
            10000,
            "FAIL - after 10000 insertions, size should be 10000",
        )

        for i in range(10000):
            avl_tree.delete(avl_tree.root)

        self.assertEqual(
            avl_tree.size(), 0, "FAIL - after deleting all nodes size should be 0"
        )
        self.add_points(2)

    def test_order_after_insertions(self):
        test_list = [23, 4, 60, 999, 33, 2, 1, 1000]
        avl_tree = AVLTree()
        for num in test_list:
            avl_tree.insert(num, str(num))

        self.assertEqual(
            avl_tree.root.height,
            3,
            "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 - height of root should be 3",
        )
        self.assertEqual(
            avl_tree.root.key,
            23,
            "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 - root should be 23",
        )
        self.assertEqual(
            avl_tree.root.left.key,
            2,
            "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 - root's left son should be 2",
        )
        self.assertEqual(
            avl_tree.root.right.key,
            60,
            "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 - root's right son should be 60",
        )
        self.add_points(3)

    def test_order_after_deletions(self):
        test_list = [23, 4, 60, 999, 33, 2, 1, 1000]

        avl_tree = AVLTree()
        for num in test_list:
            avl_tree.insert(num, str(num))

        self.assertEqual(
            avl_tree.delete(avl_tree.search(1)),
            0,
            "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 and then deleting 1 , zero rotations should be done",
        )
        self.assertEqual(
            avl_tree.delete(avl_tree.search(2)),
            1,
            "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 and then deleting 1 and 2 , 1 rotation should be done",
        )
        self.assertEqual(
            avl_tree.root.height,
            2,
            "FAIL -  after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 and then deleting 1 ,2 - height should be 2",
        )

        self.assertEqual(
            avl_tree.delete(avl_tree.search(999)),
            0,
            "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 and then deleting 1 , 2 and 999, zero rotations should be done",
        )
        self.assertEqual(
            avl_tree.delete(avl_tree.search(33)),
            0,
            "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 and then deleting 1 , 2 , 999 and 33, zero rotations should be done",
        )
        self.add_points(3)

    def test_delete_first_check_size(self):
        real_length = 0
        for i in range(100):
            self.tree.insert(i, str(i))
            real_length += 1
            self.assertEqual(real_length, self.tree.size(), "FAIL: Tree size incorrect")
        for i in range(99):
            self.tree.delete(self.tree.search(i))
            real_length -= 1
            self.assertEqual(real_length, self.tree.size(), "FAIL: Tree size incorrect")

        self.add_points(1)

    def test_list_to_array_empty(self):
        self.assertEqual(
            self.tree.avl_to_array(),
            [],
            "FAIL - avl_to_array() should return [] for an empty tree",
        )
        self.tree.insert(1, "1")
        self.assertNotEqual(
            self.tree.avl_to_array(),
            [],
            "FAIL - avl_to_array() should not return [] for a non-empty tree",
        )
        self.add_points(1)

    def test_avl_to_array_identical_vals(self):
        lst = [i for i in range(1000)]
        copy = []
        for i in range(1000):
            copy.append((i, str(i)))
        random.shuffle(lst)
        T = self.create_tree(lst)
        self.assertEqual(
            copy,
            T.avl_to_array(),
            "FAIL - avl_to_array() is not consistent with the insertion order provided",
        )
        self.add_points(1)

    def test_avl_to_array_random(self):

        python_list_numbers = []

        for i in range(50):
            random_number = random.randint(0, 10000)
            while random_number in python_list_numbers:
                random_number = random.randint(0, 10000)
            python_list_numbers.append(random_number)
            self.tree.insert(random_number, str(random_number))

        python_list_numbers.sort()
        python_list = []
        for num in python_list_numbers:
            python_list.append((num, str(num)))
        avl_list = self.tree.avl_to_array()
        self.assertEqual(python_list, avl_list, "FAIL - problem in avl_to_array")
        self.add_points(2)

    def test_size_of_empty_tree(self):
        self.assertEqual(
            self.tree.size(), 0, "FAIL - tree.size() on an empty tree should return 0"
        )
        self.tree.insert(0, "0")
        self.assertNotEqual(
            self.tree.size(),
            0,
            "FAIL - tree.length() on a non-empty tree should not return 0",
        )
        self.assertEqual(
            self.tree.size(),
            1,
            "FAIL - tree.size() a tree with one node should return 1",
        )
        self.add_points(1)

    def test_length_after_insert(self):
        length = 0
        for i in range(10):
            self.tree.insert(10 - i, "insert_number_" + str(i))
            length += 1
            self.assertEqual(
                length,
                self.tree.size(),
                "FAIL - Length error, first loop, iteration {}".format(str(i)),
            )
        more_to_add = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        for i in more_to_add:
            self.tree.insert(i, "insert_number_" + str(i))
            length += 1
            self.assertEqual(
                length,
                self.tree.size(),
                "FAIL - Length error, second loop, iteration {}".format(str(i)),
            )
        self.add_points(1)

    def test_length_after_many_insertions(self):
        length = 0
        avl_tree = AVLTree()
        in_tree = []

        for i in range(100):

            rand_num = random.randint(0, 10000)

            while rand_num in in_tree:
                rand_num = random.randint(0, 10000)

            avl_tree.insert(rand_num, str(rand_num))
            in_tree.append(rand_num)
            length += 1
            self.assertEqual(
                length,
                avl_tree.size(),
                "FAIL - Length error, third loop, iteration {}".format(str(i)),
            )

        self.add_points(1)

    def test_size_after_delete(self):
        for i in range(1000):
            self.tree.insert(i, str(i))
        for j in range(999):
            self.tree.delete(self.tree.root)
            self.assertEqual(self.tree.size(), 999 - j, "FAIL - Length error")
        self.tree.delete(self.tree.root)
        self.assertEqual(
            self.tree.size(),
            0,
            "FAIL - Length error after deleting all the nodes from the list",
        )
        self.add_points(2)

    def calc_height_diff(self, tree_1: AVLTree, tree_2: AVLTree):
        if tree_1.empty() and tree_2.empty():
            return 0
        elif tree_1.empty():
            return tree_2.root.height + 1
        elif tree_2.empty():
            return tree_1.root.height + 1
        return abs(tree_1.root.height - tree_2.root.height)

    def test_double_rotation_1(self):
        avl_tree = AVLTree()
        avl_tree.insert(4, str(4))
        avl_tree.insert(6, str(6))
        self.assertEqual(
            3,
            avl_tree.insert(5, str(5)),
            "FAIL: inserting 4 ,6 ,5 into an empty tree should result in a double rotation and a height change",
        )
        self.add_points(1)

    def test_double_rotation_2(self):
        avl_tree = AVLTree()
        avl_tree.insert(6, str(6))
        avl_tree.insert(4, str(4))

        self.assertEqual(
            3,
            avl_tree.insert(5, str(5)),
            "FAIL: inserting 4 ,6 ,5 into an empty tree should result in a double rotation and a height change",
        )
        self.add_points(1)

    def test_non_succesful_search(self):
        self.assertEqual(
            self.tree.search(0),
            None,
            "FAIL - tree.search() on an empty tree should return -1",
        )
        for i in range(10):
            self.tree.insert(i, str(i))
        self.assertEqual(
            self.tree.search(11),
            None,
            "FAIL - tree.search() should return None "
            "whenever val is not in the tree",
        )
        self.add_points(1)

    def test_search(self):
        for i in range(100):
            self.tree.insert(i, str(i))
        for i in range(100):
            self.assertEqual(self.tree.search(i).key, i)
            self.assertEqual(self.tree.search(i).value, str(i))
        self.add_points(1)

    # def test_search_complex(self):
    #     N = 100
    #     T = self.create_tree([i for i in range(N)], random_order=True)
    #     in_order = self.in_order(T)
    #     lst = [str(i) for i in range(N)]
    #     for i in range(N):
    #         lst[T.search(i).key] = str(i)
    #     self.assertEqual(in_order, lst)
    #     self.add_points(2)

    def test_search_after_delete(self):
        N = 100
        T = self.create_tree([i for i in range(N)], random_order=True)
        for i in range(N):
            self.assertNotEqual(
                T.search(i),
                None,
                "FAIL - search should return None iff str({}) is not in the tree".format(
                    i
                ),
            )
            T.delete(T.search(i))
            self.assertEqual(
                T.search(i),
                None,
                "FAIL - search should return None iff str({}) is not in the tree".format(
                    i
                ),
            )
        self.add_points(1.5)

    def test_inserts_and_avl_node_functions(self):
        # Example from https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99
        node_list = [41, 20, 65, 11, 29, 50, 91, 31, 72, 99]
        avl_tree = self.create_tree(node_list)

        # Check key and get_value
        for i in node_list:
            self.assertEqual(i, avl_tree.search(i).key, "FAIL - get key")
            self.assertEqual(str(i), avl_tree.search(i).value, "FAIL - get value")
        self.add_points(1.5, False)

        # Check root properties
        self.assertEqual(
            41,
            avl_tree.root.key,
            "FAIL - In https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99 root should be 41",
        )
        self.assertNotEqual(False, avl_tree.root.is_real_node())
        self.assertIsNone(
            avl_tree.root.parent, "FAIL - Root should have no parent"
        )

        self.add_points(1, False)

        # Check get parent
        roots_right_son = avl_tree.root.right
        roots_left_son = avl_tree.root.left
        self.assertEqual(
            avl_tree.root, roots_right_son.parent, "FAIL in get parent"
        )
        self.assertEqual(
            avl_tree.root, roots_left_son.parent, "FAIL in get parent"
        )
        self.add_points(1, False)

        # Check heights
        roots_right_right_grandson = roots_right_son.right
        self.assertEqual(
            1, roots_right_right_grandson.height, "FAIL in tree heights"
        )
        self.assertEqual(3, avl_tree.root.height, "FAIL in tree heights")
        self.assertEqual(2, roots_right_son.height, "FAIL in tree heights")
        self.add_points(1, False)

        # Check is real node on real nodes
        self.assertNotEqual(False, roots_right_son.is_real_node())
        self.assertNotEqual(False, roots_left_son.is_real_node())
        self.add_points(1, False)

        # Check tree formation
        self.assertEqual(
            65,
            roots_right_son.key,
            "FAIL - In https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99 root's right son is 65",
        )
        # self.assertEqual(5 , roots_right_son.size , "FAIL - tree formation incorrect in https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99") Test removed for 2024A
        self.assertEqual(
            20,
            roots_left_son.key,
            "FAIL - tree formation incorrect in https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99",
        )
        # self.assertEqual(4 , roots_left_son.size , "FAIL - tree size incorrect in https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99") #Test removed for 2024A

        self.assertEqual(
            91,
            roots_right_right_grandson.key,
            "FAIL - tree formation incorrect in https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99",
        )
        self.add_points(1, False)

        # Check virtual node properties
        childless_nodes = [
            avl_tree.search(11),
            avl_tree.search(31),
            avl_tree.search(50),
            avl_tree.search(72),
            avl_tree.search(99),
        ]
        for node in childless_nodes:
            self.assertFalse(
                node.right.is_real_node(),
                "FAIL - is_real_node returns true for virtual node",
            )
            self.assertFalse(
                node.left.is_real_node(),
                "FAIL - is_real_node returns true for virtual node",
            )
            self.assertEqual(
                None,
                node.right.right,
                "FAIL - get_right should return None for a virtual node",
            )
            self.assertEqual(
                None,
                node.right.left,
                "FAIL - get_left should return None for a virtual node",
            )
            self.assertEqual(
                None,
                node.left.right,
                "FAIL - get_right should return None for a virtual node",
            )
            self.assertEqual(
                None,
                node.left.left,
                "FAIL - get_left should return None for a virtual node",
            )
        self.add_points(1)

    @classmethod
    def tearDownClass(self):
        super()
        # print("\n\n")
        # print("==Tester Results:==")
        # print("  # Of Tests: {}    ".format(NUMBER_OF_TESTS))
        # print("Successful Tests: {}".format(PASSED_TESTS))
        # print(" Failed Tests: {}   ".format(NUMBER_OF_TESTS - PASSED_TESTS))
        # print("The Final Grade is: ")
        # print("  {} out of {}      ".format(round(GRADE,1), MAX_GRADE))
        # print("\n\n")
        print(GRADE)


if __name__ == "__main__":
    unittest.main(verbosity=0)
    # Change verbosity = 0 or verbosity = 2 for less/more details from tests
