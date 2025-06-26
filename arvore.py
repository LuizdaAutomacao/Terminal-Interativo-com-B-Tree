# arvore.py
# Implementação da Árvore B+ com nós folha duplamente encadeados

import math

class Node:
    def __init__(self, order, is_leaf=False):
        self.order = order
        self.is_leaf = is_leaf
        self.keys = []
        self.parent = None

        if is_leaf:
            self.values = []
            self.next = None
            self.previous = None  # Encadeamento duplo
        else:
            self.pointers = []

class BplusTree:
    def __init__(self, order=4):
        if order < 3:
            raise ValueError("A ordem da árvore deve ser no mínimo 3")
        self.order = order
        self.root = Node(order, is_leaf=True)

    def is_empty(self):
        return not self.root.keys

    def _find_leaf(self, key):
        node = self.root
        while not node.is_leaf:
            for i, k in enumerate(node.keys):
                if key < k:
                    node = node.pointers[i]
                    break
            else:
                node = node.pointers[-1]
        return node

    def search(self, key):
        leaf = self._find_leaf(key)
        for i, k in enumerate(leaf.keys):
            if k == key:
                return leaf.values[i]
        return None

    def insert(self, key, value):
        leaf = self._find_leaf(key)

        for i, k in enumerate(leaf.keys):
            if k == key:
                leaf.values[i] = value
                return

        for i, k in enumerate(leaf.keys):
            if key < k:
                leaf.keys.insert(i, key)
                leaf.values.insert(i, value)
                break
        else:
            leaf.keys.append(key)
            leaf.values.append(value)

        if len(leaf.keys) == self.order:
            self._split_leaf(leaf)

    def _split_leaf(self, leaf):
        mid = self.order // 2

        new_leaf = Node(self.order, is_leaf=True)
        new_leaf.parent = leaf.parent
        new_leaf.keys = leaf.keys[mid:]
        new_leaf.values = leaf.values[mid:]

        leaf.keys = leaf.keys[:mid]
        leaf.values = leaf.values[:mid]

        new_leaf.next = leaf.next
        if leaf.next:
            leaf.next.previous = new_leaf
        leaf.next = new_leaf
        new_leaf.previous = leaf

        self._insert_in_parent(leaf, new_leaf.keys[0], new_leaf)

    def _insert_in_parent(self, left, key, right):
        parent = left.parent
        if not parent:
            new_root = Node(self.order)
            new_root.keys = [key]
            new_root.pointers = [left, right]
            self.root = new_root
            left.parent = right.parent = new_root
            return

        for i, k in enumerate(parent.keys):
            if key < k:
                parent.keys.insert(i, key)
                parent.pointers.insert(i + 1, right)
                break
        else:
            parent.keys.append(key)
            parent.pointers.append(right)

        right.parent = parent

        if len(parent.pointers) > self.order:
            self._split_internal_node(parent)

    def _split_internal_node(self, node):
        mid = self.order // 2
        promoted = node.keys[mid]

        new_node = Node(self.order)
        new_node.parent = node.parent
        new_node.keys = node.keys[mid + 1:]
        new_node.pointers = node.pointers[mid + 1:]

        node.keys = node.keys[:mid]
        node.pointers = node.pointers[:mid + 1]

        for child in new_node.pointers:
            child.parent = new_node

        self._insert_in_parent(node, promoted, new_node)

    def delete(self, key):
        leaf = self._find_leaf(key)
        for i, k in enumerate(leaf.keys):
            if k == key:
                leaf.keys.pop(i)
                leaf.values.pop(i)
                break
        else:
            return  # Chave não encontrada

        min_keys = math.ceil((self.order - 1) / 2)
        if len(leaf.keys) < min_keys and leaf != self.root:
            self._handle_underflow(leaf)

    def _handle_underflow(self, node):
        if node == self.root:
            if not node.is_leaf and len(node.pointers) == 1:
                self.root = node.pointers[0]
                self.root.parent = None
            return

        parent = node.parent
        idx = parent.pointers.index(node)
        min_keys = math.ceil((self.order - 1) / 2)

        if idx > 0:
            left = parent.pointers[idx - 1]
            if len(left.keys) > min_keys:
                self._borrow_from_sibling(node, left, parent, idx, True)
                return

        if idx < len(parent.pointers) - 1:
            right = parent.pointers[idx + 1]
            if len(right.keys) > min_keys:
                self._borrow_from_sibling(node, right, parent, idx, False)
                return

        if idx > 0:
            self._merge_with_sibling(parent.pointers[idx - 1], node, parent, idx - 1)
        else:
            self._merge_with_sibling(node, parent.pointers[idx + 1], parent, idx)

    def _borrow_from_sibling(self, node, sibling, parent, idx, is_left):
        if is_left:
            k = sibling.keys.pop(-1)
            v = sibling.values.pop(-1) if node.is_leaf else None
            node.keys.insert(0, parent.keys[idx - 1])
            parent.keys[idx - 1] = k
            if node.is_leaf:
                node.values.insert(0, v)
            else:
                ptr = sibling.pointers.pop(-1)
                node.pointers.insert(0, ptr)
                ptr.parent = node
        else:
            k = sibling.keys.pop(0)
            v = sibling.values.pop(0) if node.is_leaf else None
            node.keys.append(parent.keys[idx])
            parent.keys[idx] = k
            if node.is_leaf:
                node.values.append(v)
            else:
                ptr = sibling.pointers.pop(0)
                node.pointers.append(ptr)
                ptr.parent = node

    def _merge_with_sibling(self, left, right, parent, sep_idx):
        sep = parent.keys.pop(sep_idx)

        if not left.is_leaf:
            left.keys.append(sep)

        left.keys.extend(right.keys)
        if left.is_leaf:
            left.values.extend(right.values)
            left.next = right.next
            if right.next:
                right.next.previous = left
        else:
            left.pointers.extend(right.pointers)
            for child in right.pointers:
                child.parent = left

        parent.pointers.remove(right)

        if parent != self.root and len(parent.pointers) < math.ceil(self.order / 2):
            self._handle_underflow(parent)
        elif parent == self.root and not parent.keys:
            self.root = left
            left.parent = None

    def get_all_values(self):
        leaf = self.root
        while not leaf.is_leaf:
            leaf = leaf.pointers[0]
        values = []
        while leaf:
            values.extend(leaf.values)
            leaf = leaf.next
        return values

    def get_all_leaf_keys(self):
        leaf = self.root
        while not leaf.is_leaf:
            leaf = leaf.pointers[0]
        keys = []
        while leaf:
            keys.extend(leaf.keys)
            leaf = leaf.next
        return keys

    def range_query(self, start_key, end_key):
        results = []
        leaf = self._find_leaf(start_key)
        while leaf:
            for i, key in enumerate(leaf.keys):
                if key > end_key:
                    return results
                if start_key <= key:
                    results.append((key, leaf.values[i]))
            leaf = leaf.next
        return results