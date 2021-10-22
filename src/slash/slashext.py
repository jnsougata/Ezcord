
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

    def ismatched(self, index:int, value):

        TARGET = self.json["options"][index]['type']

        if TARGET == 4 and (type(value) is int):
            return True
        elif TARGET == 3 and isinstance(value, str):
            return True
        elif TARGET == 5 and (type(value) is bool):
            return True
        else:
            return None





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

        if self.ismatched(index = index, value = value):

            self.json["options"][index]["choices"].append(
                {
                    "name": name,
                    "value": value
                }
            )
        else:
            print(index)
            raise ValueError("Type of value of choice must be same as the type of option that it belongs to")



