from parameters.name_styles import NS1_London
from text_lib import text_preparer_fns, TX


class T1_London(TX.TX):
    def __init__(self):
        super().__init__()
        self.primary_pools_dict, self.backup_pool = text_preparer_fns.pools_preparer(NS1_London.import_pool)
