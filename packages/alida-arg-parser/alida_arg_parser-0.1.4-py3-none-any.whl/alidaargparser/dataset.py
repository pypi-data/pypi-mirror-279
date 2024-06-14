from .assets_utils import get_asset_properties

class Dataset:
    def __init__(self, name=None, description=None, mode=None, columns_type=None, data_type=None):
        self.name = name
        self.description = description
        self.columns_type = columns_type
        self.data_type = data_type
        self.info = get_asset_properties(name)
        
        assert mode=="batch" or mode=="streaming"
        self.mode = mode
        

