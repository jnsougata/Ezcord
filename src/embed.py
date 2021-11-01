from datetime import datetime


class Embed:
    def __init__(
            self,
            title:str,
            description:str,
            url:str = None,
            color:int = None
    ):
        self.payload = {
            'type': 'rich',
            'title': title,
            'description': description,
            'url': url,
            'color':color,
            'fields':[],
        }

    def __repr__(self):
        return str(self.payload)

    def add_field(
            self,
            name:str,
            value:str,
            inline:bool = False
    ):
        self.payload['fields'].append(
            {
                'name':name,
                'value':value,
                'inline':inline
            }
        )

    def set_footer(
            self,
            text:str,
            icon_url:str = None,
            proxy_icon_url:str = None
    ):
        self.payload['footer'] = {
            'text':text,
            'icon_url':icon_url,
            'proxy_icon_url':proxy_icon_url
        }

    def set_thumbnail(
            self, url:str,
            height:int = None,
            width:int = None,
            proxy_url:str = None
    ):
        self.payload['thumbnail'] = {
            'url':url,
            'height': height,
            'width': width,
            'proxy_url': proxy_url
        }

    def add_image(
            self, url:str,
            height:int = None,
            width:int = None,
            proxy_url:str = None
    ):
        self.payload['image'] = {
            'url':url,
            'height': height,
            'width': width,
            'proxy_url': proxy_url
        }

    def set_author(
            self,
            name:str,
            url:str = None,
            icon_url:str = None,
            proxy_icon_url:str = None
    ):
        self.payload['author'] = {
            'name':name,
            'url':url,
            'icon_url':icon_url,
            'proxy_icon_url':proxy_icon_url
        }

    def set_timestamp(self):
        time = datetime.now()
        self.payload['timestamp'] = time.isoformat()