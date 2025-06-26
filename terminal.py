# terminal.py
# Este arquivo é uma integração de terminal.py, filesystem.py e models.py.
# A dependência 'arvore.py' não foi fornecida.
# UMA CLASSE PROVISÓRIA (PLACEHOLDER) 'BplusTree' FOI ADICIONADA ABAIXO.
# POR FAVOR, SUBSTITUA-A PELA SUA IMPLEMENTAÇÃO REAL PARA FUNCIONALIDADE COMPLETA.

# Conteúdo que deveria estar em 'arvore.py'
# Importa a sua implementação real da Árvore B+
from arvore import BplusTree
# Conteúdo de models.py
class File:
    """Representa um arquivo no sistema."""
    def __init__(self, name):
        self.name = name
        self.type = 'file'

    def __str__(self):
        """Retorna o nome do arquivo para exibição."""
        return self.name

class Directory:
    """
    Representa um diretório, que contém sua própria Árvore B+
    para armazenar seus filhos (arquivos e outros diretórios).
    """
    def __init__(self, name, parent=None):
        self.name = name
        self.type = 'directory'
        self.parent = parent
        
        # A chamada BplusTree(4) usa a classe definida acima.
        # Se sua classe real tiver um construtor diferente, ajuste aqui.
        self.children = BplusTree(4)

    def __str__(self):
        """Retorna o nome do diretório com uma barra no final."""
        return f"{self.name}/"


# Conteúdo de filesystem.py
class FileSystem:
    """
    Gere a estrutura de ficheiros e diretórios utilizando uma Árvore B+.
    """
    def __init__(self):
        """Inicializa o sistema de ficheiros com um diretório raiz."""
        # O diretório raiz é criado automaticamente no arranque.
        self.root = Directory('/')
        self.current_directory = self.root

    def get_path(self):
        """Gera a string do caminho atual para o prompt."""
        if self.current_directory == self.root:
            return "~"
        
        path = []
        dir_ptr = self.current_directory
        while dir_ptr != self.root:
            path.append(dir_ptr.name)
            dir_ptr = dir_ptr.parent
        
        return f"~/{'/'.join(reversed(path))}"

    def mkdir(self, name):
        """Cria um novo diretório no diretório atual."""
        if self.current_directory.children.search(name):
            print(f"mkdir: não é possível criar o diretório '{name}': Ficheiro já existe")
            return
        
        new_dir = Directory(name, parent=self.current_directory)
        self.current_directory.children.insert(name, new_dir)

    def touch(self, name):
        """Cria um novo ficheiro vazio no diretório atual."""
        if self.current_directory.children.search(name):
            print(f"touch: não é possível criar o ficheiro '{name}': Ficheiro já existe")
            return
            
        new_file = File(name)
        self.current_directory.children.insert(name, new_file)

    def ls(self):
        """Lista ficheiros e diretórios por ordem lexicográfica."""
        # A Árvore B+ já mantém os elementos ordenados.
        children = self.current_directory.children.get_all_values()
        for item in children:
            print(item)

    def cd(self, name=".."):
        """Altera o diretório atual."""
        if name == "..":
            if self.current_directory.parent:
                self.current_directory = self.current_directory.parent
            return

        target_node = self.current_directory.children.search(name)
        
        if not target_node:
            print(f"cd: '{name}': Nenhum ficheiro ou diretório com esse nome")
            return
            
        if isinstance(target_node, Directory):
            self.current_directory = target_node
        elif isinstance(target_node, File):
            print(f"cd: '{name}': Não é um diretório")
        else:
            print(f"cd: Erro - a pesquisa por '{name}' retornou um tipo inesperado.")

    def rm(self, name):
        """Remove um ficheiro ou um diretório vazio."""
        target_node = self.current_directory.children.search(name)
        
        if not target_node:
            print(f"rm: não é possível remover '{name}': Nenhum ficheiro ou diretório com esse nome")
            return

        if isinstance(target_node, Directory):
            if not target_node.children.is_empty():
                print(f"rm: falha ao remover '{name}': O diretório não está vazio")
                return

        try:
            self.current_directory.children.delete(name)
            print(f"'{name}' removido.")
        except NotImplementedError:
             print(f"Erro ao apagar '{name}': O método 'delete' ainda não foi implementado na sua BplusTree.")
        except Exception as e:
            print(f"Erro inesperado ao apagar '{name}': {e}")


# Conteúdo original de terminal.py (função principal)
def main():
    """
    Main function to run the interactive terminal simulation.
    """
    fs = FileSystem()
    print("Fakerational Filesystem")
    
    while True:
        # The prompt reflects the current path.
        prompt = f"fakerational:{fs.get_path()}$ "
        try:
            # Commands are read and processed sequentially.
            command_input = input(prompt).strip()
            if not command_input:
                continue

            parts = command_input.split()
            command = parts[0]
            args = parts[1:]

            if command == "exit":
                break
            elif command == "ls":
                fs.ls()
            elif command == "mkdir" and args:
                fs.mkdir(args[0])
            elif command == "touch" and args:
                fs.touch(args[0])
            elif command == "cd":
                fs.cd(args[0] if args else "..")
            elif command == "rm" and args:
                fs.rm(args[0])
            else:
                print(f"{command}: command not found")
        
        # Handles errors like trying to access non-existent directories.
        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()