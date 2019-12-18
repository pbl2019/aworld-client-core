from aworld_client_core.terrain import Terrain


class Mutations:
    def __init__(self):
        data_inst = Data()
        for name in data_inst.__dict__.keys():
            setattr(self, name, False)


class Data:
    def __init__(self):
        self.character_id = ""
        self.terrain = Terrain()
        self.characters = {}
        self.items = {}

    def update(self, character_id=None, terrain=None,
            characters=None, items=None):
        mutations = Mutations()
        if character_id is not None:
            self.character_id = character_id
            mutations.character_id = True
        if characters is not None:
            for character in characters:
                self.characters[character['character_id']] = character
            mutations.characters = True
        if terrain is not None:
            width = terrain["width"]
            height = terrain["height"]
            #  origin_x = terrain["origin"]["x"]
            #  origin_y = terrain["origin"]["y"]
            data = terrain["data"]
            if width != self.terrain.width or height != self.terrain.height:
                self.terrain = Terrain(width=width, height=height, data=data)
                mutations.terrain = True
            else:
                pass
        if items is not None:
            for item in items:
                self.items[item["item_id"]] = item
            mutations.items = True
        return mutations

