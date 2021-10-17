from text_lib import text_preparer_fns


class TX():
    def __init__(self):
        self.primary_pools_dict = {}
        self.backup_pool = []
        self.used_names = []

    def get_name(self, pool: str):
        this_pool = self.primary_pools_dict[pool]

        def get_name_inner(this_pool):
            if this_pool:
                return this_pool.pop()
            elif self.backup_pool:
                return self.backup_pool.pop()
            else:
                raise RuntimeError("There are no names left in primary or backup pools. Adjust generation parameters")

        this_name = get_name_inner(this_pool)
        while this_name in self.used_names:
            this_name = get_name_inner(this_pool)
        self.used_names.append(this_name)

        spaced_names_list = text_preparer_fns.spacing_preparer(this_name)
        return spaced_names_list
