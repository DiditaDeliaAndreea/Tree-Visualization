import sys
import PySimpleGUI as sg
import os.path

# RBTree
class Node():
    def __init__(self, item):
        self.item = item
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1


class RedBlackTree():
    def __init__(self):
        self.TNULL = Node(0)
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    def pre_order_helper(self, node):
        if node != TNULL:
            sys.stdout.write(node.item + " ")
            self.pre_order_helper(node.left)
            self.pre_order_helper(node.right)

    def in_order_helper(self, node):
        if node != TNULL:
            self.in_order_helper(node.left)
            sys.stdout.write(node.item + " ")
            self.in_order_helper(node.right)

    def post_order_helper(self, node):
        if node != TNULL:
            self.post_order_helper(node.left)
            self.post_order_helper(node.right)
            sys.stdout.write(node.item + " ")

    def search_tree_helper(self, node, key):
        if node == TNULL or key == node.item:
            return node

        if key < node.item:
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)

    def delete_fix(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 0

    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete_node_helper(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.item == key:
                z = node

            if node.item <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            print("Cannot find key in the tree")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif (z.right == self.TNULL):
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:
            self.delete_fix(x)

    def fix_insert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    def __print_helper(self, node, indent, last):
        if node != self.TNULL:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            s_color = "RED" if node.color == 1 else "BLACK"
            print(str(node.item) + "(" + s_color + ")")
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)

    def preorder(self):
        self.pre_order_helper(self.root)

    def inorder(self):
        self.in_order_helper(self.root)

    def postorder(self):
        self.post_order_helper(self.root)

    def searchTree(self, k):
        return self.search_tree_helper(self.root, k)

    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def maximum(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node

    def successor(self, x):
        if x.right != self.TNULL:
            return self.minimum(x.right)

        y = x.parent
        while y != self.TNULL and x == y.right:
            x = y
            y = y.parent
        return y

    def predecessor(self,  x):
        if (x.left != self.TNULL):
            return self.maximum(x.left)

        y = x.parent
        while y != self.TNULL and x == y.left:
            x = y
            y = y.parent

        return y

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.item = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.item < x.item:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.item < y.item:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 0
            return

        if node.parent.parent == None:
            return

        self.fix_insert(node)

    def get_root(self):
        return self.root

    def delete_node(self, item):
        self.delete_node_helper(self.root, item)

    def print_tree(self):
        self.__print_helper(self.root, "", True)

    def find(self, node, key):
        ok=0
        while node != self.TNULL:
            if node.item == key:
                print('Found', key)
                ok=1

            if node.item <= key:
                node = node.right
            else:
                node = node.left
        if ok == 0:
            print("Cannot find")


# B-Tree
class Node:
    def __init__(self, data, par=None):
        # print ("Node __init__: " + str(data))
        self.data = list([data])
        self.parent = par
        self.child = list()

    def __str__(self):
        if self.parent:
            return str(self.parent.data) + ' : ' + str(self.data)
        return 'Root : ' + str(self.data)

    def __lt__(self, node):
        return self.data[0] < node.data[0]

    def _isLeaf(self):
        return len(self.child) == 0

    def _add(self, new_node):
        for child in new_node.child:
            child.parent = self
        self.data.extend(new_node.data)
        self.data.sort()
        self.child.extend(new_node.child)
        if len(self.child) > 1:
            self.child.sort()
        if len(self.data) > 2:
            self._split()

    def _insert(self, new_node):

        if self._isLeaf():
            self._add(new_node)

        elif new_node.data[0] > self.data[-1]:
            self.child[-1]._insert(new_node)
        else:
            for i in range(0, len(self.data)):
                if new_node.data[0] < self.data[i]:
                    self.child[i]._insert(new_node)
                    break


    def _split(self):
        left_child = Node(self.data[0], self)
        right_child = Node(self.data[2], self)
        if self.child:
            self.child[0].parent = left_child
            self.child[1].parent = left_child
            self.child[2].parent = right_child
            self.child[3].parent = right_child
            left_child.child = [self.child[0], self.child[1]]
            right_child.child = [self.child[2], self.child[3]]

        self.child = [left_child]
        self.child.append(right_child)
        self.data = [self.data[1]]

        if self.parent:
            if self in self.parent.child:
                self.parent.child.remove(self)
            self.parent._add(self)
        else:
            left_child.parent = self
            right_child.parent = self


    def _find(self, item):
        if item in self.data:
             print("Found", item)
        elif self._isLeaf():
            print('Cannot find')
            return False
        elif item > self.data[-1]:
            return self.child[-1]._find(item)
        else:
            for i in range(len(self.data)):
                if item < self.data[i]:
                    return self.child[i]._find(item)

    def remove(self, item):
        self.root.remove(item)

    def _preorder(self):
        print(self)
        for child in self.child:
            child._preorder()

class Tree:
    def __init__(self):

        self.root = None

    def insert(self, item):
        if self.root is None:
            self.root = Node(item)
        else:
            self.root._insert(Node(item))
            while self.root.parent:
                self.root = self.root.parent
        return True

    def find(self, item):
        return self.root._find(item)

    def remove(self, item):
        self.root.remove(item)

    def childrenList(self, temp, node):
        for child in node.child:
            temp.append(child)

    def printdata(self, temp):
        for i in temp:
            print(i.data, end=' ')
        print(' ')

    def print_help(self, temp):
        x = []
        for i in temp:
            tree.childrenList(x, i)
        tree.printdata(x)
        temp = x
        return temp

    def print(self, node):
        temp = []
        tree.childrenList(temp, node)
        tree.printdata(temp)
        print(' ')
        x = tree.print_help(temp)
        while len(x) != 0:
            tree.print_help(x)
            x = tree.print_help(x)

    def preorder(self):
        print('----Preorder----')
        self.root._preorder()

#Max Heap Tree

class MaxHeap:

    def __init__(self, maxsize):

        self.maxsize = maxsize
        self.size = 0
        self.Heap = [0] * (self.maxsize + 1)
        self.Heap[0] = sys.maxsize
        self.FRONT = 1

    def parent(self, pos):

        return pos // 2

    def leftChild(self, pos):

        return 2 * pos

    def rightChild(self, pos):

        return (2 * pos) + 1

    def isLeaf(self, pos):

        if pos >= (self.size // 2) and pos <= self.size:
            return True
        return False

    def swap(self, fpos, spos):

        self.Heap[fpos], self.Heap[spos] = (self.Heap[spos],
                                            self.Heap[fpos])

    def maxHeapify(self, pos):

        if not self.isLeaf(pos):
            if (self.Heap[pos] < self.Heap[self.leftChild(pos)] or
                    self.Heap[pos] < self.Heap[self.rightChild(pos)]):

                if (self.Heap[self.leftChild(pos)] >
                        self.Heap[self.rightChild(pos)]):
                    self.swap(pos, self.leftChild(pos))
                    self.maxHeapify(self.leftChild(pos))

                else:
                    self.swap(pos, self.rightChild(pos))
                    self.maxHeapify(self.rightChild(pos))

    def insert(self, element):

        if self.size >= self.maxsize:
            return
        self.size += 1
        self.Heap[self.size] = element

        current = self.size

        while (self.Heap[current] >
               self.Heap[self.parent(current)]):
            self.swap(current, self.parent(current))
            current = self.parent(current)

    def Print(self):

        for i in range(1, (self.size // 2) + 1):
            print(" PARENT : " + str(self.Heap[i]) +
                  " LEFT CHILD : " + str(self.Heap[2 * i]) +
                  " RIGHT CHILD : " + str(self.Heap[2 * i + 1]))

    def extractMax(self):

        popped = self.Heap[self.FRONT]
        self.Heap[self.FRONT] = self.Heap[self.size]
        self.size -= 1
        self.maxHeapify(self.FRONT)

        return popped


#Interfata

sg.theme('Dark')
if __name__ == "__main__":
    bst = RedBlackTree()
    tree = Tree()
    maxHeap = MaxHeap(15)

    tab1_layout = [
                   [sg.InputText(size=(6, 1),key='rbin1'), sg.Button("Insert", font=(15), key='rbinsert'), sg.Input(size=(6, 1),key='rbin2'), sg.Button("Delete", font=(15),key='rbdel'),sg.Input(size=(6, 1),key='rbin3'), sg.Button("Find", font=(15),key='rbfind'),
            sg.Button("Print", font=(15),key='rbprint'),sg.Button("Clear", font=(15),key='rbclear')
            ]
                   ]

    tab2_layout = [
                   [sg.InputText(size=(6, 1),key='bin1'), sg.Button("Insert", font=(15), key='binsert'),sg.Input(size=(6, 1),key='bin3'), sg.Button("Find", font=(15),key='bfind'),
            sg.Button("Print", font=(15),key='bprint'),sg.Button("Clear", font=(15),key='bclear')
            ]]

    tab3_layout = [
                   [sg.InputText(size=(6, 1),key='hin1'), sg.Button("Insert", font=(15), key='hinsert'), sg.Button("Show Max Value", font=(15),key='hmax'),
            sg.Button("Print", font=(15),key='hprint'),sg.Button("Clear", font=(15),key='hclear')
            ]]


    layout = [[sg.TabGroup([[sg.Tab('Red-Black Tree', tab1_layout, key='rbtree'), sg.Tab('B-Tree', tab2_layout,key='btree'),sg.Tab('Max Heap Tree', tab3_layout,key='htree')]],
                           key='_group1_', tab_location='topleft')],
              [sg.Output(size=(90, 30),key='output')],[sg.Button("Exit", font=(15),key='exit')]]
    window = sg.Window("Tree Visualization", layout)


    while True:
        event, values = window.Read()
        if event in (None, 'exit'):
            break
        if event == 'rbinsert':
            bst.insert(int(values["rbin1"]))
        elif event == 'rbdel':
            bst.delete_node(int(values["rbin2"]))
        elif event == 'rbfind':
            bst.find(bst.root,int(values["rbin3"]))
        elif event == 'rbprint':
            print(bst.print_tree())
        elif event=='rbclear':
            window.FindElement('output').Update('')
        elif event == 'binsert':
            tree.insert(int(values["bin1"]))
        elif event == 'bfind':
            tree.find(int(values["bin3"]))
        elif event == 'bprint':
            print(tree.root)
            print(' ')
            tree.print(tree.root)
        elif event=='bclear':
            window.FindElement('output').Update('')
        elif event=='hinsert':
            maxHeap.insert(int(values["hin1"]))
        elif event=='hmax':
            print(maxHeap.extractMax())
        elif event=='hprint':
            maxHeap.Print()
        elif event=='hclear':
            window.FindElement('output').Update('')


    window.close()



