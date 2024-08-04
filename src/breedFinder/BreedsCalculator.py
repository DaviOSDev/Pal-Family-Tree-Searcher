class Breeding_calculator():
    """
    A class to calculate the breeds of the pals.

    if the hash_data is True, the hash data will be used to find the breeds.
    else, the data will be used to calculate the breeds.

    """

    def __init__(self, dataPath = 'src\data\data.json', use_hash_data = True) -> None:
        """
        use_hash_data: bool -> If True, the hash data will be used to calculate the breeds.
        """
        with open(dataPath, 'r') as file:
            from json import loads
            self.DATA = loads(file.read())

        self.special_breedings: list = self.DATA["special-breedings"]["parents"]
        
        if use_hash_data:
            self.hash_data : dict = None
            self.create_parents_hash_data()
            self.create_breeds_hash_data()

    def get_pal_info(self, wanted_pal) -> list[str, int, int]:
        """
        wanted_pal: str -> The name of the pal you want to get the information of.
        return: list -> [pal_name, breeding_power, tie_break]
        """
        try:    
            index = self.DATA["pals"].index(wanted_pal)
            return [self.DATA["pals"][index], self.DATA["breed-power"][index], self.DATA["tie-break"][index]]
        
        except:
            print("Pal not found.")
            return None

    def get_breed_result(self, parent1: str, parent2: str) -> int:
        """
        Calculate the breeding result of two parents.

        parent1: str -> The name of the first parent.
        parent2: str -> The name of the second parent.

        return: int -> The breeding result of the two parents.
        """
        try:
            from math import floor
            self.parent1: str = parent1
            self.parent2: str = parent2
            self.is_special_breed: bool = False

            if [parent1, parent2] in self.special_breedings:
                self.is_special_breed = True
                self.breed_result = self.DATA["special-breedings"]["childs"][self.special_breedings.index([parent1, parent2])]
                return
            elif [parent2, parent1] in self.special_breedings:
                self.is_special_breed = True
                self.breed_result = self.DATA["special-breedings"]["childs"][self.special_breedings.index([parent2, parent1])]
                return
            
            parent1_info = self.get_pal_info(parent1)
            parent2_info = self.get_pal_info(parent2)

            self.breed_result =  floor((parent1_info[1] + parent2_info[1] + 1)  / 2)
            return self.breed_result
        
        except ValueError:
            print("Pal not found.")
            return None

    def get_pal_by_breed_result(self, parent1, parent2) -> str:

        """
        get the pal that is closest to the breeding result of the two parents.

        parent1: str -> The name of the first parent.
        parent2: str -> The name of the second parent.

        return: str -> The name of the pal that is closest to the breeding result of the two parents.

        """

        if self.breeds_hash_data:
            return self.breeds_hash_data[parent1][parent2]
        
        self.get_breed_result(parent1, parent2)

        distance_to_breed_result_dict = {}

        if [parent1, parent2] in self.special_breedings or [parent2, parent1] in self.special_breedings:
            try:
                pal = self.DATA["special-breedings"]["childs"][self.special_breedings.index([parent1, parent2])]
                index = self.DATA["breed-power"].index(pal)
                return self.DATA["pals"][index]

            except:
                pal = self.DATA["special-breedings"]["childs"][self.special_breedings.index([parent2, parent1])]
                index = self.DATA["breed-power"].index(pal)
                return self.DATA["pals"][index]
        
        for i in range(0, len(self.DATA["pals"])):
            if self.DATA["breed-power"] not in self.DATA["special-breedings"]["childs"]:
                distance_to_breed_result_dict[pal] = [abs(self.breed_result - self.get_pal_info(self.DATA["pals"][i])[1]), self.get_pal_info(self.DATA["pals"][i])[2]]
        
        min_distance = min(distance_to_breed_result_dict.values(), key=lambda x: x[0])[0]
        ties = [[pal, distance_to_breed_result_dict[pal][1]] for pal in distance_to_breed_result_dict if distance_to_breed_result_dict[pal][0] == min_distance]

        if len(ties) > 1:
            return min(ties, key=lambda x: x[1])[0]
        
        return ties[0][0]
        
    
    def get_parents_by_pal_name(self, child) -> list[tuple[str, str]]:

        """
        get the possible parents of a child.

        child: str -> The name of the child.

        return: list -> A list of tuples with possible breeds of the child.
        """

        possible_parents = []
        
        if self.parents_hash_data:
            return self.parents_hash_data[child]


        for i in range (0, len(self.DATA["pals"])):
            for j in range(i, len(self.DATA["pals"])):
                if self.get_pal_by_breed_result(self.DATA["pals"][i], self.DATA["pals"][j]) == child:
                    print("found a breed!")
                    possible_parents.append((self.DATA["pals"][i], self.DATA["pals"][j]))
                                    
        return possible_parents
    
    def get_childs_by_pal_name(self, parent) -> list[str]:

        """
        get the possible childs of a pal.

        parent: str -> The name of the parent.

        return: list -> A list of possible childs of the parent.
        """

        possible_childs = []
        
        for pal in self.DATA["pals"]:
            possible_childs.append(self.get_pal_by_breed_result(parent, pal))

        return possible_childs
    
    def create_parents_hash_data(self) -> dict:
        """
        Istanciate the hash table of the data.

        return: dict -> the hash table of the data.
        """
        try:
            with open('src\data\parents_hash_data.json', 'r') as file:
                from json import loads
                self.parents_hash_data = loads(file.read())
            
            return self.parents_hash_data

        except OSError:
            pass

    def get_second_parent(self, child, parent) -> list[str]:
        """
        Get the second parent of a child's breed.

        child: str -> The name of the child.
        parent: str -> The name of the first parent.

        return: str -> The name of the parent that is the pair for the child's breed.
        """

        possible_parents = []

        if self.parents_hash_data:
            for pair in self.parents_hash_data[child]:
                if parent in pair:
                    possible_parents.append(pair[0] if pair[0] != parent else pair[1])
        
            return possible_parents if possible_parents else None
        
        child_breeds = self.get_parents_by_pal_name(child)
        for pair in child_breeds:
            if parent in pair:
                possible_parents.append(pair[0] if pair[0] != parent else pair[1])
        
        return possible_parents if possible_parents else None

    def create_breeds_hash_data(self) -> dict:
        """
        Istanciate the hash table of the data.

        return: dict -> the hash table of the data.
        """
        self.breeds_hash_data = {}

        with open('src/data/breeds_hash_data.json', 'r') as file:
            from json import loads
            self.breeds_hash_data = loads(file.read())
                    
        return self.breeds_hash_data

# Path: src/breed-finder/BreedFinder.py
