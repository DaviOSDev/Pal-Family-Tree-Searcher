from BreedsCalculator import Breeding_calculator
from sys import getsizeof

class Pal():

    def __init__(self, pal: str) -> None:
        self.pal = pal

    def __str__(self) -> str:
        return self.pal

    def __repr__(self) -> str:
        return self.pal
    
class Breed():

    def __init__(self, parent1: Pal, parent2: Pal) -> None:
        self.parent1 : Pal= parent1
        self.parent2 : Pal= parent2

    def __str__(self) -> str:
        return f"[{self.parent1}, {self.parent2}]"
    
    def __repr__(self) -> list:
        return [self.parent1, self.parent2]
    
class Node:
    """
    A node of the tree.
    """
    def __init__(self, obj, **kargs) -> None:

        if isinstance(obj, Pal):
            self.child : Pal = kargs["child"]
            self.husband : Pal = kargs["husband"]
            self.pal : Pal = obj
        
        elif isinstance(obj, Breed):
            self.breed : Breed= obj

        else:
            raise ValueError("A node must be a Pal or a Breed.")
    
    def __str__(self) -> str:
        if hasattr(self, "pal"):
            return str(self.pal)
        
        elif hasattr(self, "breed"):
            return str(self.breed)
        
    def __repr__(self) -> str:
        if hasattr(self, "pal"):
            return str(self.pal)
        
        elif hasattr(self, "breed"):
            return str(self.breed)
    
    def type(self) -> str:
        if hasattr(self, "pal"):
            return "Pal"
        
        elif hasattr(self, "breed"):
            return "Breed"

class Frontier():
    
        def __init__(self, strategy: str = "BFS") -> None:
            
            self.frontier = []

            if strategy == "BFS":
                self.add = lambda node: self.frontier.append(node)
                self.pop = lambda: self.frontier.pop(0)
            
            elif strategy == "DFS":
                self.add = lambda node: self.frontier.append(node)
                self.pop = lambda: self.frontier.pop(-1)
    
        def is_empty(self) -> bool:
            return len(self.frontier) == 0

        def hasPal(self, node: Node) -> bool:
            return any(node.pal == n.pal for n in self.frontier)

class BreedingSolver():

    def __init__(self) -> None:
        self.calculator = Breeding_calculator()
        
        self.solution = None

    def get_couples(self, pal: Pal) -> list:
        """
        Get the neighbors of a node.
        """
        neighbors = []

        for breed in self.calculator.get_parents_by_pal_name(pal.pal):
            parent1 = Pal(breed[0])
            parent2 = Pal(breed[1])
            neighbors.append(Node(Breed(parent1, parent2)))
        
        return neighbors
    
    def has_all_pals(self, pals: set) -> bool:
        """
        Check if all the pals are in the set.
        """
        for pal in self.calculator.DATA["pals"]:
            if pal not in pals:
                return False
        
        return True

    def solve(self, pal: Pal, parents_in_tree: list) -> None:

        if pal.pal not in self.calculator.DATA["pals"]:
            raise ValueError("The pal is not in the database")
            
        start = Node(pal)
        frontier = Frontier("BFS")
        frontier.add(start)
        in_tree = set()

        """def delete_useless_breeds(couples: list, parents_in_tree: list) -> list:
            return [couple for couple in couples if couple[0] in parents_in_tree or couple[1] in parents_in_tree]"""
        
        while not self.has_all_pals(in_tree):
            current_node = frontier.pop()
            
            if current_node.type() == "Pal":
                pass