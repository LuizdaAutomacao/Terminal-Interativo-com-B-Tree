import math

class Node:
    def __init__(self, order, is_leaf=False):
        # 'order' define quantas chaves este nó pode conter (capacidade máxima)
        self.order = order
        # indica se este nó é uma folha (True) ou um nó interno (False)
        self.is_leaf = is_leaf
        # lista de chaves armazenadas neste nó
        self.keys = []
        # referência para o nó pai (None se este nó for a raiz)
        self.parent = None

        if is_leaf:
            # em folhas, armazenamos também os valores correspondentes
            self.values = []
            # ponteiros encadeados duplamente para percorrer folhas em sequência
            self.next = None
            self.previous = None
        else:
            # em nós internos, armazenamos ponteiros para filhos
            self.pointers = []


class BplusTree:
    def __init__(self, order=4):
        # a ordem mínima permitida para a árvore é 3
        if order < 3:
            raise ValueError("A ordem da árvore deve ser no mínimo 3")
        # define a ordem (tamanho máximo de chaves) e inicializa com uma folha vazia
        self.order = order
        self.root = Node(order, is_leaf=True)

    def is_empty(self):
        # retorna True se a raiz não contém nenhuma chave
        return not self.root.keys

    def _find_leaf(self, key):
        # caminha da raiz até a folha onde a chave deve residir
        node = self.root
        while not node.is_leaf:
            for i, k in enumerate(node.keys):
                if key < k:
                    # desce pelo ponteiro correspondente
                    node = node.pointers[i]
                    break
            else:
                # se a chave for maior que todas, vai pelo último ponteiro
                node = node.pointers[-1]
        return node

    def search(self, key):
        # encontra a folha e procura a chave dentro dela
        leaf = self._find_leaf(key)
        for i, k in enumerate(leaf.keys):
            if k == key:
                return leaf.values[i]
        # retorna None se não achar
        return None

    def insert(self, key, value):
        # insere um par (chave, valor) ou atualiza se a chave já existir
        leaf = self._find_leaf(key)

        for i, k in enumerate(leaf.keys):
            if k == key:
                # chave existente: atualiza o valor
                leaf.values[i] = value
                return

        # insere de forma ordenada na folha
        for i, k in enumerate(leaf.keys):
            if key < k:
                leaf.keys.insert(i, key)
                leaf.values.insert(i, value)
                break
        else:
            # se maior que todas as chaves atuais, anexa ao final
            leaf.keys.append(key)
            leaf.values.append(value)

        # se a folha extrapolar a capacidade, divide-a
        if len(leaf.keys) == self.order:
            self._split_leaf(leaf)

    def _split_leaf(self, leaf):
        # calcula índice do ponto médio
        mid = self.order // 2

        # cria nova folha com a segunda metade das chaves e valores
        new_leaf = Node(self.order, is_leaf=True)
        new_leaf.parent = leaf.parent
        new_leaf.keys = leaf.keys[mid:]
        new_leaf.values = leaf.values[mid:]

        # ajusta a folha original para manter só a primeira metade
        leaf.keys = leaf.keys[:mid]
        leaf.values = leaf.values[:mid]

        # atualiza ponteiros encadeados entre folhas
        new_leaf.next = leaf.next
        if leaf.next:
            leaf.next.previous = new_leaf
        leaf.next = new_leaf
        new_leaf.previous = leaf

        # insere a nova folha no nó pai, promovendo a primeira chave
        self._insert_in_parent(leaf, new_leaf.keys[0], new_leaf)

    def _insert_in_parent(self, left, key, right):
        parent = left.parent
        if not parent:
            # se left não tiver pai, cria nova raiz interna
            new_root = Node(self.order)
            new_root.keys = [key]
            new_root.pointers = [left, right]
            self.root = new_root
            left.parent = right.parent = new_root
            return

        # insere chave e ponteiro de right no pai
        for i, k in enumerate(parent.keys):
            if key < k:
                parent.keys.insert(i, key)
                parent.pointers.insert(i + 1, right)
                break
        else:
            parent.keys.append(key)
            parent.pointers.append(right)

        right.parent = parent

        # se o pai ficar com muitos ponteiros, divide-o
        if len(parent.pointers) > self.order:
            self._split_internal_node(parent)

    def _split_internal_node(self, node):
        # divisão de um nó interno que extrapolou
        mid = self.order // 2
        promoted = node.keys[mid]

        # cria novo nó interno para a segunda metade
        new_node = Node(self.order)
        new_node.parent = node.parent
        new_node.keys = node.keys[mid + 1:]
        new_node.pointers = node.pointers[mid + 1:]

        # ajusta o nó original para manter a primeira metade
        node.keys = node.keys[:mid]
        node.pointers = node.pointers[:mid + 1]

        # atualiza referência de pai dos filhos movidos
        for child in new_node.pointers:
            child.parent = new_node

        # promove chave ao nó pai
        self._insert_in_parent(node, promoted, new_node)

    def delete(self, key):
        # localiza a folha e remove a chave
        leaf = self._find_leaf(key)
        for i, k in enumerate(leaf.keys):
            if k == key:
                leaf.keys.pop(i)
                leaf.values.pop(i)
                break
        else:
            # se não encontrar, encerra
            return

        # calcula mínimo de chaves permitido (underflow)
        min_keys = math.ceil((self.order - 1) / 2)
        if len(leaf.keys) < min_keys and leaf != self.root:
            self._handle_underflow(leaf)

    def _handle_underflow(self, node):
        # gerencia sobras (empréstimo ou fusão) em nós que ficaram abaixo do mínimo
        if node == self.root:
            # se raiz interna reduzir a um único ponteiro, ajusta raiz
            if not node.is_leaf and len(node.pointers) == 1:
                self.root = node.pointers[0]
                self.root.parent = None
            return

        parent = node.parent
        idx = parent.pointers.index(node)
        min_keys = math.ceil((self.order - 1) / 2)

        # tenta pegar de irmão esquerdo
        if idx > 0:
            left = parent.pointers[idx - 1]
            if len(left.keys) > min_keys:
                self._borrow_from_sibling(node, left, parent, idx, is_left=True)
                return

        # tenta pegar de irmão direito
        if idx < len(parent.pointers) - 1:
            right = parent.pointers[idx + 1]
            if len(right.keys) > min_keys:
                self._borrow_from_sibling(node, right, parent, idx, is_left=False)
                return

        # se nenhum irmão puder emprestar, faz fusão
        if idx > 0:
            self._merge_with_sibling(parent.pointers[idx - 1], node, parent, sep_idx=idx - 1)
        else:
            self._merge_with_sibling(node, parent.pointers[idx + 1], parent, sep_idx=idx)

    def _borrow_from_sibling(self, node, sibling, parent, idx, is_left):
        # reequilibra nós retirando chave do irmão e ajustando pai
        if is_left:
            # retira último item do irmão esquerdo
            k = sibling.keys.pop(-1)
            if node.is_leaf:
                v = sibling.values.pop(-1)
                node.values.insert(0, v)
            child_ptr = None
            if not node.is_leaf:
                child_ptr = sibling.pointers.pop(-1)
                node.pointers.insert(0, child_ptr)
                child_ptr.parent = node
            node.keys.insert(0, parent.keys[idx - 1])
            parent.keys[idx - 1] = k
        else:
            # retira primeiro item do irmão direito
            k = sibling.keys.pop(0)
            if node.is_leaf:
                v = sibling.values.pop(0)
                node.values.append(v)
            child_ptr = None
            if not node.is_leaf:
                child_ptr = sibling.pointers.pop(0)
                node.pointers.append(child_ptr)
                child_ptr.parent = node
            node.keys.append(parent.keys[idx])
            parent.keys[idx] = k

    def _merge_with_sibling(self, left, right, parent, sep_idx):
        # funde dois nós (left e right) removendo a chave separadora do pai
        sep = parent.keys.pop(sep_idx)
        if not left.is_leaf:
            left.keys.append(sep)

        # move todas as chaves e ponteiros de right para left
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

        # remove referência de right em parent
        parent.pointers.remove(right)

        # trata underflow recursivamente, se necessário
        if parent != self.root and len(parent.pointers) < math.ceil(self.order / 2):
            self._handle_underflow(parent)
        elif parent == self.root and not parent.keys:
            # se raiz ficou sem chaves, ajusta nova raiz
            self.root = left
            left.parent = None

    def get_all_values(self):
        # retorna lista de valores de todas as folhas em ordem
        leaf = self.root
        while not leaf.is_leaf:
            leaf = leaf.pointers[0]
        values = []
        while leaf:
            values.extend(leaf.values)
            leaf = leaf.next
        return values

    def get_all_leaf_keys(self):
        # retorna lista de todas as chaves de folhas em ordem
        leaf = self.root
        while not leaf.is_leaf:
            leaf = leaf.pointers[0]
        keys = []
        while leaf:
            keys.extend(leaf.keys)
            leaf = leaf.next
        return keys

    def range_query(self, start_key, end_key):
        # busca pares (chave, valor) entre start_key e end_key
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
