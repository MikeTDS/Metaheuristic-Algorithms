class Node():
    def __init__(self, key):
        self.key = key
        self.right = self
        self.left = self
        self.parent = self
        self.color = 'r'

class RBT():
    def __init__(self):
        self.nil = Node(None)
        self.nil.left = self.nil
        self.nil.right = self.nil
        self.nil.parent = self.nil
        self.nil.color = 'b'
        self.root = self.nil
    
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
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
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
    
    def insertt(self, z):
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == self.nil:
            self.root = z
        elif z.key < y.key:
            y.left = z 
        else:
            y.right = z 
        z.left = self.nil
        z.right = self.nil
        z.color = 'r'
        self.insert_fixup(z)
    
    def insert_fixup(self, z):
        while z.parent.color == 'r':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == 'r':
                    z.parent.color = 'b'
                    y.color = 'b'
                    z.parent.parent.color = 'r'
                    z = z.parent.parent
                else: 
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = 'b'
                    z.parent.parent.color = 'r'
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == 'r':
                    z.parent.color = 'b'
                    y.color = 'b'
                    z.parent.parent.color = 'r'
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = 'b'
                    z.parent.parent.color = 'r'
                    self.left_rotate(z.parent.parent)

        self.root.parent = self.nil
        self.root.color = 'b'

    def transplant(self, u, v):
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
    
    def tree_minimum(self, x):
        while x.left != self.nil:
            x = x.left
        return x
    
    def tree_maximium(self, x):
        while x.right != self.nil:
            x = x.right
        return x

    def successorr (self, node):
        if (node.right != self.nil):
            return self.tree_minimum(node.right)

        tmp = node.parent
        while (tmp != self.nil and node == tmp.right):
            node = tmp
            tmp = tmp.parent

        return tmp

    def select(self, node, key):
        if node.key == key or node == self.nil:
            return node
        if node.key < key:
            return self.select(node.right, key)
        return self.select(node.left, key)

    def inorderr(self, node):
        order = []
        if node != self.nil:
            order += self.inorderr(node.left)
            order.append(node.key)
            order += self.inorderr(node.right)
        return order
########################   
    def insert(self, key):
        if key != '':
            node = Node(key)
            node.parent = self.nil
            node.left = self.nil
            node.right = self.nil
            self.insertt(node)

    def find(self, key):
        node = self.select(self.root, key)
        if node != self.nil:
            return True
        return False

    def inorder(self):
        return self.inorderr(self.root)

