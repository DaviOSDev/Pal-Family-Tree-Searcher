from BreedsCalculator import Breeding_calculator

class Breed():

    def __init__(self, parent1: str, parent2: str) -> None:
        self.parent1 : str = parent1
        self.parent2 : str = parent2

    def __str__(self) -> str:
        return f"[{self.parent1} + {self.parent2}]"
    
    def __repr__(self) -> list:
        return f"{self.parent1} + {self.parent2}"
    
    def equal_parents(self) -> bool:
        return self.breed.parent1 == self.breed.parent2

class Node:
    """
    A node of the tree.
    """
    def __init__(self, pal: str, husband = None, child = None) -> None:
        self.child : Node | None = child
        self.husband : Node | ParentsNode | None = husband
        self.pal : str = pal

    def __str__(self) -> str:
        return f"{self.pal} At {id(self)}"

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
        return f"{self.pal} At {id(self)},"
    
    def __str__(self) -> str:
        return f"{self.pal} At {id(self)}"

    def add_father(self, father: Node, *args) -> None:
        self.fathers.append(father)
        for arg in args:
            self.add_father(arg)

class Frontier():
    
        def __init__(self) -> None:
            
            self.frontier = []
        
        def pop(self) -> Node:
            return self.frontier.pop(0)

        def add(self, node: Node) -> Node:
            self.frontier.append(node)

        def is_empty(self) -> bool:
            return len(self.frontier) == 0

        def hasPal(self, node: Node) -> bool:
            return any(node.pal == n.pal for n in self.frontier)

class Solver():

    def __init__(self, canBeOnGraph = True) -> None:
        self.calculator = Breeding_calculator()
        self.solution = None
        self.canBeOnGraph = canBeOnGraph

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

        if len(pal_list) < 2:
            return [ParentsNode(pal_list[0].pal)]
        
        if len(pal_list) == 2:
            return [ParentsNode(self.calculator.get_pal_by_breed_result(pal_list[0].pal, pal_list[1].pal))]
        
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
            sliced_permutation : tuple[int] = permutation[2:]
            if len(sliced_permutation) < 1:
                continue

            print(f"husbands: {father1} {father2}")
            for pal_index in sliced_permutation:
                print(f"pal_index: {pal_index}")
                print(f"Pal: {pal_list[pal_index]}")
                print(f"Result: {result}")
                print(f"Antique result: {result}")
                antique_result = result
                next_parent = pal_list[pal_index]
                result.husband = next_parent
                print(f"result husband: {result.husband}")
                result = get_pal(result, next_parent)
                result.add_father(antique_result, next_parent)
            print(f"father1: {father1} father2: {father2}")
            print_fathers(result)
            if all(result.pal != pal.pal for pal in pals):
                print(f"Adding to pals: {result}")
                pals.append(result)
            print_fathers(result)
        print("-"*100)
        print("Pals:")
        print(pals)
        for pal in pals:
            print_fathers(pal)
        return pals
    
    def solve_tree(self, root_pal: Node, pals_to_find: list[ParentsNode]) -> Node:
        def defineParentsNodes(first_parent : Node, second_parent : Node, child : Node) -> None:
            first_parent.child, second_parent.child = child, child
            first_parent.husband, second_parent.husband = second_parent, first_parent
            print(f"First parent: {first_parent} Second parent: {second_parent} Child: {child}")

        def pal_in_pals_to_find(pal : str, pals_to_find: list[ParentsNode]) -> ParentsNode:
            for parent in pals_to_find:
                if parent.pal == pal:
                    return parent
            return None

        if root_pal.pal not in self.calculator.DATA["pals"]:
            raise ValueError("The pal is not in the database")

        pals_on_tree = set()
        frontier = Frontier()
        frontier.add(root_pal)
        pals_on_tree.add(root_pal.pal)
        while not self.has_all_pals(pals_on_tree):
            if frontier.is_empty():
                return None
            node = frontier.pop()
            couples = self.get_couples(node)
            for couple in couples:
                print(f"Checking {couple}")
                if (not self.canBeOnGraph) and root_pal.pal in [couple.parent1, couple.parent2]:
                    continue
                if pal_in_pals_to_find(couple.parent1, pals_to_find):
                    returnPal = pal_in_pals_to_find(couple.parent1, pals_to_find)
                    print(f"\033[032mFound!! {returnPal}\033[0m")
                    returnPal.child = node
                    returnPal.husband = self.calculator.get_second_parent(node.pal, returnPal.pal)
                    return returnPal
                if pal_in_pals_to_find(couple.parent2, pals_to_find):
                    returnPal = pal_in_pals_to_find(couple.parent2, pals_to_find)
                    returnPal.husband = self.calculator.get_second_parent(node.pal, returnPal.pal)
                    print("\033[032mFound!!\033[0m]")
                    returnPal.child = node
                    return returnPal
                print("\033[91mNot found \033[0m")
                first_parent = Node(couple.parent1)
                second_parent = Node(couple.parent2, husband=first_parent)
                defineParentsNodes(first_parent, second_parent, node)
                if first_parent.pal not in pals_on_tree:
                    frontier.add(first_parent)
                    pals_on_tree.add(first_parent.pal)
                if second_parent.pal not in pals_on_tree:
                    frontier.add(second_parent)
                    pals_on_tree.add(second_parent.pal)

        return None

    def solve(self, root_pal: str, parents_list: list[str], CanBeOnGraph : bool) -> None | list[Node]:
        """
        Solve the problem.
        """
        self.canBeOnGraph = CanBeOnGraph

        def transform_to_node(pal_list: list[str]) -> list[ParentsNode]:
            return [ParentsNode(pal) for pal in pal_list]
        
        root = Node(root_pal)
        permutations = self.get_list_of_permutations(parents_list)
        parents_list = transform_to_node(parents_list)
        parents_list = self.get_pals_by_permutations(parents_list, permutations)
        print(root)
        graph = self.solve_tree(root, parents_list)
        if graph == None:
            print("Could not find the way.")
            return None

        self.solution = graph
        print_solution(self.solution, root)
        
        return graph      

    def create_img(self):
        pass

def print_solution(solution : ParentsNode, end : Node):
            is_first = True
            pointer = solution
            while pointer != end:
                if is_first:
                    print_fathers(pointer)
                    pointer = pointer.child
                    is_first = False
                    continue
                print(pointer, "⟺ ", pointer.husband if pointer.husband else "")
                print("↓")
                pointer = pointer.child
            print(pointer)

def print_fathers(root : ParentsNode):
    printl : list[tuple[ParentsNode, ParentsNode]]= []
    while root != None:
        try:
            printl.append((root, root.husband))
            root = root.fathers[0] if root.fathers else None
        except IndexError as error:
            print("Error", error)
            break
    printl = printl[::-1]
    for print_ in printl:
        print(print_[0], "⟺ ", print_[1])
        print("↓")
    print("End\n\n")

if __name__ == "__main__":
    solver = Solver()
    list_of_parents = ["Frostallion", "Teafant", "Azurobe", "Anubis"]
    solver.solve("Blazamut", list_of_parents, True)