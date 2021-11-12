class Metadata:
    def __init__(self):
        self.meta_dict = {
            "name": "",
            "description": "Metro Topology, London",
            "image": "",
            "external_url": "",
            "attributes": [],
        }

    def add_gen_attributes(self, num_stations, num_interchanges, len_trackage):
        num_stations_dict = {
            "display_type": "number",
            "trait_type": "No. Stations",
            "value": num_stations
        }
        num_interchanges_dict = {
            "display_type": "number",
            "trait_type": "No. Interchanges",
            "value": num_interchanges
        }
        len_trackage_dict = {
            "display_type": "number",
            "trait_type": "Total System Length",
            "value": len_trackage
        }
        self.meta_dict["attributes"].append(num_stations_dict)
        self.meta_dict["attributes"].append(num_interchanges_dict)
        self.meta_dict["attributes"].append(len_trackage_dict)

    def add_art_attributes(self, art_style):
        art_style_dict = {
            "trait_type": "Art Style",
            "value": str(art_style)
        }
        self.meta_dict["attributes"].append(art_style_dict)

