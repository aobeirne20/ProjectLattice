from text_lib import text_preparer_fns


class TX():
    def __init__(self):
        self.primary_pools_dict = {}
        self.backup_pool = []
        self.used_names = []

        self.held_names = []
        self.backup_held_names = []
        self.used_held_names = []

    def get_name(self, pool: str):
        this_pool = self.primary_pools_dict[pool]

        def get_name_inner(this_pool):
            if this_pool:
                self.held_names.append(this_pool.pop())
                return self.held_names[-1]
            elif self.backup_pool:
                self.backup_held_names.append(self.backup_pool.pop())
                return self.backup_held_names[-1]
            else:
                raise RuntimeError("There are no names left in primary or backup pools. Adjust generation parameters")

        this_name = get_name_inner(this_pool)
        while this_name in self.used_names or this_name in self.used_held_names:
            print(f"Found {this_name} already used")
            this_name = get_name_inner(this_pool)
        self.used_held_names.append(this_name)

        spaced_names_list = text_preparer_fns.spacing_preparer(this_name)
        return spaced_names_list

    def finalize_removal(self, actual_used_names, pool):
        self.used_names += actual_used_names
        self.used_held_names = []
        for name in actual_used_names:
            if name in self.held_names:
                self.held_names.remove(name)
            elif name in self.backup_held_names:
                self.backup_held_names.remove(name)

        self.backup_pool += self.backup_held_names
        self.primary_pools_dict[pool] += self.held_names

        self.held_names = []
        self.backup_held_names = []





