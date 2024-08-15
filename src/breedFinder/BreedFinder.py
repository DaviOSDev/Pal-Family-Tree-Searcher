from BreedsCalculator import Breeding_calculator
    
class Breed():

    def __init__(self, parent1: str, parent2: str) -> None:
        self.parent1 : str = parent1
        self.parent2 : str = parent2

    def __str__(self) -> str:
        return f"[{self.parent1}, {self.parent2}]"
    
    def __repr__(self) -> list:
        return [self.parent1, self.parent2]
    
    def equal_parents(self) -> bool:
        return self.breed.parent1 == self.breed.parent2

class Node:
    """
    A node of the tree.
    """
    def __init__(self, pal: str, husband = None, child = None) -> None:
        self.child : Node | None = child
        self.husband : Node | None = husband
        self.pal : str = pal

    def __str__(self) -> str:
        return self.pal

    def __repr__(self) -> str:
        return self.pal
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return False
        return self.pal == other.pal

    def __hash__(self) -> int:
        return hash(self.pal)

class ParentsNode(Node):

    def __init__(self, pal: str, husband = None, child = None) -> None:
        super().__init__(pal, husband, child)
        self.fathers = []

    def __repr__(self) -> str:
        return self.pal

    def add_father(self, father: Node, *args) -> None:
        self.fathers.append(father)
        for arg in args:
            self.add_father(arg)

class Frontier():
    
        def __init__(self, strategy: str = "BFS") -> None:
            
            self.frontier = []
            self.strategy = strategy
        
        def pop(self) -> Node:
            if self.strategy == "DFS":
                return self.frontier.pop(-1)
            return self.frontier.pop(0)

        def add(self, node: Node) -> Node:
            self.frontier.append(node)

        def is_empty(self) -> bool:
            return len(self.frontier) == 0

        def hasPal(self, node: Node) -> bool:
            return any(node.pal == n.pal for n in self.frontier)

class Solver():

    def __init__(self) -> None:
        self.calculator = Breeding_calculator()
        self.solution = None

    def get_couples(self, pal: str) -> list[Breed]:
        """
        Get the neighbors of a node.
        """
        couples = []

        for breed in self.calculator.get_parents_by_pal_name(pal.pal):
            parent1 = breed[0]
            parent2 = breed[1]
            couples.append(Breed(parent1, parent2))
        
        return couples
    
    def has_all_pals(self, pals: set) -> bool:
        """
        Check if all the pals are in the set.
        """
        for pal in self.calculator.DATA["pals"]:
            if pal not in pals:
                return False
        
        return True
    
    def get_pal_by_breed_result(self, parent1: Node | ParentsNode, parent2: Node | ParentsNode) -> Node | ParentsNode:
        """
        Get the pal that is closest to the breeding result of the two parents.
        """
        return Node(self.calculator.get_pal_by_breed_result(parent1.pal, parent2.pal))


    def get_list_of_permutations(self, pal_list: list) -> list[tuple[int]]:
        """
        Get all the possibilities of results of a list of pals.
        """
        pal_list_indexes = []
        for i in range(len(pal_list)):
            pal_list_indexes.append(i)

        permutations_list = []
        from itertools import permutations
        for permutation in permutations(pal_list_indexes):
            if len(permutation) == len(pal_list):
                permutations_list.append(permutation)

        return permutations_list

    def get_pals_by_permutations(self, pal_list: list[ParentsNode], permutations: list[tuple[int]]) -> list[Node]:
        """
        Get the pals by the permutations.
        """

        def get_pal(parent1 : Node, parent2: Node) -> ParentsNode:
            return ParentsNode(self.calculator.get_pal_by_breed_result(parent1.pal, parent2.pal))
        
        pals : list[ParentsNode] = []
        for permutation in permutations:
            father1 = pal_list[permutation[0]]
            father2 = pal_list[permutation[1]]
            father1.husband = father2
            father2.husband = father1
            result : ParentsNode = get_pal(father1, father2)
            result.add_father(father1, father2)
            for pal in permutation[2:]:
                antique_result = result
                result = get_pal(result, pal_list[pal])
                result.add_father(antique_result, pal_list[pal])
            append = True
            for pal in pals:
                if result.pal == pal.pal:
                    append = False
            if append:
                pals.append(result)
        for pal in pals:
            print(pal.pal + " At ", id(pal))
        return pals
    
    def solve_tree(self, root_pal: Node, pals_to_find: list[ParentsNode]) -> Node:
        
        def defineParentsNodes(firstParent : Node, secondParent : Node, child : Node) -> None:
            firstParent.child = child
            secondParent.child = child
            first_parent.husband = second_parent
            second_parent.husband = first_parent

        def pal_in_pals_to_find(pal : str, pals_to_find: list[ParentsNode]) -> Node:
            for parent in pals_to_find:
                if parent.pal == pal:
                    return parent
            return None

        if root_pal.pal not in self.calculator.DATA["pals"]:
            raise ValueError("The pal is not in the database")
        root : Node = root_pal
        pals_on_tree = set()
        frontier = Frontier(strategy="BFS")
        frontier.add(root)
        pals_on_tree.add(root.pal)
        tryies = 1
        while not self.has_all_pals(pals_on_tree):
            print("try number", tryies)
            tryies += 1
            if frontier.is_empty():
                return None
            node = frontier.pop()
            couples = self.get_couples(node)
            for couple in couples:
                if pal_in_pals_to_find(couple.parent1, pals_to_find):
                    returnPal = pal_in_pals_to_find(couple.parent1, pals_to_find)
                    returnPal.child = node
                    returnPal.husband = self.calculator.get_second_parent(node.pal, returnPal.pal)
                    print("Found!!")
                    return returnPal
                if pal_in_pals_to_find(couple.parent2, pals_to_find):
                    returnPal = pal_in_pals_to_find(couple.parent2, pals_to_find)
                    returnPal.husband = self.calculator.get_second_parent(node.pal, returnPal.pal)
                    print("Found!!")
                    returnPal.child = node
                    return returnPal
                first_parent = Node(couple.parent1)
                second_parent = Node(couple.parent2, husband=first_parent)
                defineParentsNodes(first_parent, second_parent, node)
                if first_parent.pal not in pals_on_tree:
                    frontier.add(first_parent)
                if second_parent.pal not in pals_on_tree:
                    frontier.add(second_parent)
                pals_on_tree.add(first_parent.pal)
                pals_on_tree.add(second_parent.pal)
        
        return None

    def solve(self, root_pal: str, parents_list: list[str]) -> None | list[Node]:
        """
        Solve the problem.
        """

        def transform_to_node(pal_list: list[str]) -> list[Node]:
            return [Node(pal) for pal in pal_list]
        
        def printsolution(solution : Node, end : Node):

            pointer = solution
            while pointer != end:
                print(pointer, "⟺ ", pointer.husband if pointer.husband else "None")
                print("↓")
                pointer = pointer.child
            print(pointer)

        root = Node(root_pal)
        permutations = self.get_list_of_permutations(parents_list)
        parents_list = transform_to_node(parents_list)
        parents_list = self.get_pals_by_permutations(parents_list, permutations)
        tree = self.solve_tree(root, parents_list)
        if tree == None:
            print("Could not find the way.")
            return None

        self.solution = tree
        printsolution(self.solution, root)
        return tree        

    def create_img(self):
        import PIL
        pass

if __name__ == "__main__":
    solve = Solver()
    root_pal = "Teafant"
    parents_list = ["Chikipi", "Teafant", "Faleris", "Pyrin", "Quivern"]
    solve.solve(root_pal, parents_list)
