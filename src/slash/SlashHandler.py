class Slash:

    def __init__(
            self,
            application_id: int,
            guild_id: int,
    ):
        self.app_id = application_id
        self.guild_id = guild_id
        self.json = None



    def create_command(self, name: str, description: str):

        self.json = {
                "name": name,
                "description": description,
                "type": 1,
                "options": []
            }


    def add_string_option(
            self, name:str,
            description: str,
            required:bool
    ):

        self.json["options"].append(
            {
                "name": name,
                "description": description,
                "type": 3,
                "required": required,
            }
        )

    def add_bool_option(
            self, name:str,
            description: str,
            required:bool
    ):

        self.json["options"].append(
            {
                "name": name,
                "description": description,
                "type": 5,
                "required": required,
            }
        )










