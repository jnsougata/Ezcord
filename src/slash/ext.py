import types


class Slash:
    def __init__(
            self,
            scmd: dict,
            application_id:int,
            guild_id:int
    ):
        self.json = scmd
        self.app_id = application_id
        self.guild_id = guild_id





class Builder:

    def __init__(self):
        self.json = None
        self._types = {
            3: 1,
            4: 'a',
            5: True,
        }


    def command(self,name:str, description:str):

        self.json = {
                "name": name,
                "description": description,
                "type": 1,
                "options": []
        }

    def add_str_option(self, name:str, description:str, required = True):
        self.json["options"].append(
            {
                "name": name,
                "description": description,
                "type": 3,
                "required": required,
                "choices": []
            }
        )

    def add_int_option(self, name:str, description:str, required = True):
        self.json["options"].append(
            {
                "name": name,
                "description": description,
                "type": 4,
                "required": required,
                "choices": []
            }
        )

    def add_bool_option(self, name:str, description:str, required = True):
        self.json["options"].append(
            {
                "name": name,
                "description": description,
                "type": 5,
                "required": required,
                "choices":[]
            }
        )

    def add_choices(self, index:int, name:str, value):

        self.json["options"][index]["choices"].append(
            {
                "name": name,
                "value": value
            }
        )



