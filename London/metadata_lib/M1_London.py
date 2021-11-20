from parameters.StyleGuides import complete_style_guide as csg


class Metadata:
    def __init__(self):
        self.meta_dict = {
            "name": "",
            "description": "Metro Topology, London",
            "image": "",
            "external_url": "",
            "attributes": [],
        }

    def add_gen_attributes(self, num_stations, num_interchanges):
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
        self.meta_dict["attributes"].append(num_stations_dict)
        self.meta_dict["attributes"].append(num_interchanges_dict)

    def add_art_attributes(self, art_style):
        art_style = csg.art_style_guide[art_style]
        if art_style['background'] == 'black':
            setting = "Dark"
        elif art_style['background'] == 'darkblue':
            setting = "Night"
        else:
            setting = "Conventional"

        if art_style['details'] == 'gold' or art_style['details'] == 'inverted gold':
            style = "Gold"
        elif art_style['details'] == 'greyscale' or art_style['details'] == 'inverted greyscale':
            style = "Greyscale"
        elif art_style['details'] == 'line' or art_style['details'] == 'inverted line':
            if art_style['background'] == 'black':
                style = 'Darkline'
            else:
                style = 'Brightline'
        else:
            style = 'Normal'

        background_style_dict = {"trait_type": "Scene", "value": setting}
        style_style_dict = {"trait_type": "Style", "value": style}
        self.meta_dict["attributes"].append(background_style_dict)
        self.meta_dict["attributes"].append(style_style_dict)

        if art_style['details'] == 'inverted gold' or art_style['details'] == 'inverted greyscale' or \
            art_style['details'] == 'inverted' or art_style['details'] == 'inverted line':
            augment_style_dict = {"trait_type": "Augment", "value": 'Inverted'}
            self.meta_dict["attributes"].append(augment_style_dict)
        elif art_style['name'] == 'Signature':
            augment_style_dict = {"trait_type": "Augment", "value": 'Signature'}
            self.meta_dict["attributes"].append(augment_style_dict)




