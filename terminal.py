
from arvore import BplusTree


class File:
    #Arquivo simples
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Directory:
    #Diretório que armazena filhos em uma B+ Tree
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = BplusTree(order=4)

    def __str__(self):
        return f"{self.name}/"

    def is_empty(self):
        return self.children.is_empty()


class FileSystem:
    #Simula um sistema de arquivos básico
    def __init__(self):
        self.root = Directory("/")
        self.cwd = self.root

    def prompt_path(self):
        if self.cwd is self.root:
            return "~"
        parts, node = [], self.cwd
        while node is not self.root:
            parts.append(node.name)
            node = node.parent
        return "~/" + "/".join(reversed(parts))

    def mkdir(self, name):
        if self.cwd.children.search(name):
            print(f"mkdir: '{name}' já existe")
        else:
            new_dir = Directory(name, parent=self.cwd)
            self.cwd.children.insert(name, new_dir)

    def touch(self, name):
        if self.cwd.children.search(name):
            print(f"touch: '{name}' já existe")
        else:
            new_file = File(name)
            self.cwd.children.insert(name, new_file)

    def ls(self):
        for item in self.cwd.children.get_all_values():
            print(item)

    def cd(self, name=".."):
        if name == "..":
            if self.cwd.parent:
                self.cwd = self.cwd.parent
            return

        target = self.cwd.children.search(name)
        if isinstance(target, Directory):
            self.cwd = target
        elif isinstance(target, File):
            print(f"cd: '{name}' não é um diretório")
        else:
            print(f"cd: '{name}' não encontrado")

    def rm(self, name):
        target = self.cwd.children.search(name)
        if not target:
            print(f"rm: '{name}' não encontrado")
            return

        if isinstance(target, Directory) and not target.is_empty():
            print(f"rm: '{name}': diretório não está vazio")
            return

        try:
            self.cwd.children.delete(name)
        except NotImplementedError:
            print("rm: delete() não implementado na BplusTree")
        except Exception as e:
            print(f"rm: erro ao remover '{name}': {e}")

    def run(self):
        print("Fakerational Filesystem")
        while True:
            cmd = input(f"fakerational:{self.prompt_path()}$ ").strip().split()
            if not cmd:
                continue

            op, *args = cmd
            if op == "exit":
                break
            elif op == "ls":
                self.ls()
            elif op == "mkdir" and args:
                self.mkdir(args[0])
            elif op == "touch" and args:
                self.touch(args[0])
            elif op == "cd":
                self.cd(args[0] if args else "..")
            elif op == "rm" and args:
                self.rm(args[0])
            else:
                print(f"{op}: comando não encontrado")


if __name__ == "__main__":
    FileSystem().run()
