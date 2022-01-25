from datetime import datetime


class Embed:
    def __init__(self, title: str = None, description: str = None, url: str = None, color: int = None):
        self._init = {
            'type': 'rich',
            'title': title,
            'description': description,
            'url': url,
            'color': color,
            'fields': [],
        }

    def dict(self):
        return self._init

    def add_field(self, name: str, value: str, inline: bool = False):
        self._init['fields'].append({'name': name, 'value': value, 'inline': inline})

    def set_footer(self, text: str, icon_url: str = None, proxy_icon_url: str = None):
        self._init['footer'] = {'text': text, 'icon_url': icon_url, 'proxy_icon_url': proxy_icon_url}

    def set_thumbnail(self, url: str, height: int = None, width: int = None, proxy_url: str = None):
        self._init['thumbnail'] = {'url': url, 'height': height, 'width': width, 'proxy_url': proxy_url}

    def add_image(self, url: str, height: int = None, width: int = None, proxy_url: str = None):
        self._init['image'] = {'url': url, 'height': height, 'width': width, 'proxy_url': proxy_url}

    def set_author(self, name: str, url: str = None, icon_url: str = None, proxy_icon_url: str = None):
        self._init['author'] = {'name': name, 'url': url, 'icon_url': icon_url, 'proxy_icon_url': proxy_icon_url}

    def set_timestamp(self):
        self._init['timestamp'] = datetime.utcnow().isoformat()
