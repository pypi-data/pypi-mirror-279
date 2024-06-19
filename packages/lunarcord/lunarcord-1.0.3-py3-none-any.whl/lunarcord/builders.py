#from typing import Any
from os.path import isfile, split
#from .__core__.requests import Manager
from .__core__.addons import Utils
import random

class Path: ...
class Url: ...
class User: ...
class Member: ...

class Color:

    def __init__(self, decimal: int | str):

        self.__decimal__ = int(decimal)
    
    @classmethod
    def fromRGB(cls, red: int | str = 0, green: int | str = 0, blue: int | str = 0):

        if isinstance(red, tuple):

            if len(red) != 3:

                if len(red) == 0:
                    red = (0,)

                red, green, blue = (red[0], 0, 0)
            
            else:
                
                red, green, blue = red
        
        decimal = red * 65536 + green * 256 + blue
        return cls(decimal)
    
    def toRGB(self):
        value = self.__decimal__
        
        red = value // 65536
        green = (value % 65536) // 256
        blue = value % 256
        
        return red, green, blue
    
    @classmethod
    def red(cls):
        return cls(0xE74C3C)
    
    @classmethod
    def green(cls):
        return cls(0x2ECC71)
    
    @classmethod
    def blue(cls):
        return cls(0x3498DB)
    
    @classmethod
    def darkRed(cls):
        return cls(0x992D22)
    
    @classmethod
    def darkGreen(cls):
        return cls(0x1F8B4C)
    
    @classmethod
    def darkBlue(cls):
        return cls(0x206694)
    
    @classmethod
    def blurple(cls):
        return cls(0x5865F2)
    
    @classmethod
    def purple(cls):
        return cls(0x663A82)
    
    @classmethod
    def darkPurple(cls):
        return cls(0x3C1361)
    
    @classmethod
    def lightPurple(cls):
        return cls(0x52307C)
    
    @classmethod
    def yellow(cls):
        return cls(0xFEE75C)
    
    @classmethod
    def gray(cls):
        return cls(0x979C9F)
    
    @classmethod
    def white(cls):
        return cls(0xFFFFFF)
    
    @classmethod
    def black(cls):
        return cls(0x000000)
    
    @classmethod
    def fuchsia(cls):
        return cls(0xFF00FF)
    
    @classmethod
    def lime(cls):
        return cls(0x00FF00)
    
    @classmethod
    def lightRed(cls):
        return cls(0xFF6666)
    
    @classmethod
    def lightBlue(cls):
        return cls(0x6666FF)
    
    @classmethod
    def lightYellow(cls):
        return cls(0xFFFF66)
    
    @classmethod
    def darkYellow(cls):
        return cls(0x999900)
    
    @classmethod
    def lightGreen(cls):
        return cls(0x66FF66)
    
    @classmethod
    def cyan(cls):
        return cls(0x66FFFF)
    
    @classmethod
    def orange(cls):
        return cls(0xFFB84D)
    
    @classmethod
    def brown(cls):
        return cls(0xBC8F8F)
    
    @classmethod
    def random(cls):
        return cls.fromRGB(*(random.randint(0, 255) for x in range(3)))

class EmbedArray:
    
    def __init__(self, *embeds):
        self.container = []
        self.container.extend(embeds)
        
    def __add__(self, embed):
        if isinstance(embed, Embed):
            self.container.append(embed)
        elif isinstance(embed, EmbedArray):
            for x in embed.container:
                if isinstance(x, Embed):
                    self.container.append(x)
                    
        return self
    
    def __or__(self, embed):
        return self.__add__(embed)
    
    def __iter__(self):
        return self.container.__iter__()
    
    def __next__(self):
        return self.container.__next__()
    
    def __len__(self):
        return self.container.__len__()
    
    def __str__(self):
        return 'EmbedArray(' + self.container.__str__().removeprefix('[').removesuffix(']') + ')'
                    
    async def _toJson(self):
        
        jsonified = []
        
        for embed in self:
            embedJson = await embed._toJson()
            jsonified.append(embedJson)
            
        return jsonified
    
class Embed:
    
    def __init__(self, title: str = None, description: str = None, footer: str = None, footerIcon: str = None, thumbnail: str = None, color: Color = None, image: str = None, author: str = None, authorIcon: str = None, authorUrl: str = None, timestamp: int | float | str = None):
        
        self.title = title
        self.description = description
        self.footer = footer
        self.footerIcon = footerIcon
        self.thumbnail = thumbnail
        self.color = color
        self.timestamp = timestamp
        self.image = image
        self.author = author
        self.authorIcon = authorIcon
        self.authorUrl = authorUrl
        self._fields = []
        
    async def _toJson(self):
        
        json = {'footer': {}, 'thumbnail': {}, 'image': {}}
        
        if self.__title__ is not None:
            json['title'] = self.__title__
            
        if self.__description__ is not None:
            json['description'] = self.__description__
            
        if self.__footer__ is not None:
            json['footer']['text'] = self.__footer__
            
        if self.__footericon__ is not None:
            json['footer']['icon_url'] = self.__footericon__
            
        if self.thumbnail is not None:
            json['thumbnail']['url'] = self.thumbnail
            
        if self.__color__ is not None:
            json['color'] = self.__color__.__decimal__

        if self.__timestamp__ is not None:
            json['timestamp'] = self.__timestamp__

        if self.__image__ is not None:
            json['image']['url'] = self.__image__

        if self.__author__:

            json['author'] = {'name': self.__author__}

            if self.__authorIcon__:
                json['author']['icon_url'] = self.__authorIcon__

            if self.__authorUrl__:
                json['author']['url'] = self.__authorUrl__

        if self._fields:
            json['fields'] = self._fields
        
        return json
        
    @property
    def title(self):
        return self.__title__
    
    @title.setter
    def title(self, value):
        self.__title__ = str(value) if type(value) is not str and value is not None else value
        
    @title.deleter
    def title(self):
        self.__title__ = None
        
    @property
    def description(self):
        return self.__description__
    
    @description.setter
    def description(self, value):
        self.__description__ = str(value) if type(value) is not str and value is not None else value
        
    @description.deleter
    def description(self):
        self.__description__ = None
        
    @property
    def footer(self):
        return self.__footer__
    
    @footer.setter
    def footer(self, value):
        self.__footer__ = str(value) if type(value) is not str and value is not None else value
        
    @footer.deleter
    def footer(self):
        self.__footer__ = None
        
    @property
    def footerIcon(self):
        return self.__footericon__
    
    @footerIcon.setter
    def footerIcon(self, value):
        self.__footericon__ = str(value) if type(value) is not str and value is not None else value
        
    @footerIcon.deleter
    def footerIcon(self):
        self.__footericon__ = None
        
    @property
    def color(self):
        return self.__color__
    
    @color.setter
    def color(self, value):
        
        if hasattr(value, '__iter__') and len(value) == 3:
            value = Color.fromRGB(*value)
            
        self.__color__ = value
        
    @color.deleter
    def color(self):
        self.__color__ = None

    @property
    def timestamp(self):
        return self.__timestamp__
    
    @timestamp.setter
    def timestamp(self, new):
        self.__timestamp__: str = Utils.unixToIso(new) if type(new) in (int, float) else str(new) if new is not None else None

    @timestamp.deleter
    def timestamp(self):
        self.__timestamp__ = None

    @property
    def image(self):
        return self.__image__
    
    @image.setter
    def image(self, value):
        self.__image__ = str(value) if type(value) is not str and value is not None else value
        
    @image.deleter
    def image(self):
        self.__image__ = None

    @property
    def thumbnail(self):
        return self.__thumbnail__
    
    @thumbnail.setter
    def thumbnail(self, new):
        self.__thumbnail__ = str(new) if type(new) is not str and new is not None else new

    @thumbnail.deleter
    def thumbnail(self):
        self.__thumbnail__ = None

    @property
    def author(self):
        return self.__author__
    
    @author.setter
    def author(self, new):
        self.__author__ = str(new) if type(new) is not str and new is not None else new

    @author.deleter
    def author(self):
        self.__author__ = None

    @property
    def authorIcon(self):
        return self.__authorIcon__
    
    @authorIcon.setter
    def authorIcon(self, new):
        self.__authorIcon__ = str(new) if type(new) is not str and new is not None else new

    @authorIcon.deleter
    def authorIcon(self):
        self.__authorIcon__ = None

    @property
    def authorUrl(self):
        return self.__authorUrl__
    
    @authorUrl.setter
    def authorUrl(self, new):
        self.__authorUrl__ = str(new) if type(new) is not str and new is not None else new

    @authorUrl.deleter
    def authorUrl(self):
        self.__authorUrl__ = None

    def setAuthor(self, author: User | Member, *, name: bool = True, icon: bool = True, url: bool = True):

        """Sets the `Embed.author`, `Embed.authorIcon` and `Embed.authorUrl` values for you using the provided `User` or `Member`'s data."""

        if name:
            self.author = author.name

        if icon:
            self.authorIcon = author.avatar

        if url:
            self.authorUrl = f"https://discord.com/users/{author.id}"

    def addField(self, name: str, value: str, inline: bool = False):

        """Adds a new field of `name` and `value` in the `Embed`. Don't worry about using strings - Lunarcord will take care of that for you, of course!"""

        self._fields.append({
            "name": name,
            "value": value,
            "inline": inline
        })

        return self

    def __add__(self, embed):
        
        if isinstance(embed, Embed):
            
            return EmbedArray(self, embed)
        
        elif isinstance(embed, EmbedArray):
            
            newArray = EmbedArray()
            newArray.container.append(self)
            newArray.container.extend(embed.container)
            return newArray
        
    def __or__(self, embed):
        
        self.__add__(embed)
        
    def __eq__(self, embed):
        
        if isinstance(embed, Embed):
            
            return (
                self.__title__ == embed.__title__
                and self.__description__ == embed.__description__
                and self.__footer__ == embed.__footer__
                and self.__footericon__ == embed.__footericon__
            )
        
        return False
    
    def __ne__(self, embed):
        return self.__eq__(embed) == False
    
    def __repr__(self):
        
        title = '' if self.title is None else f'title="{self.title}" '
        description = '' if self.description is None else f'description="{self.description}" '
        footer = '' if self.footer is None else f'footer="{self.footer}" '
        
        return ('<Embed ' + title + description + footer).strip() + '>'
    
    def __str__(self):
        
        for x in (
            self.__title__,
            self.__description__,
            self.__footer__
        ):
            
            if x is not None:
                return x
            
        return self.__repr__()
    
class Attachment:
    
    def __init__(self, data: bytes, name: str):
        '''
        Construct a new `lunarcord.Attachment` from the given `data`.
        
        Parameters
        ----------
        data: `bytes`
            The attachment's data, in raw bytes.
            
        name: `str`
            The attachment name that will be visible on Discord.
        '''
        
        self.bot = None

        self._bytes = data
        self._fromurl = None
        self.name = str(name)
    
    @classmethod
    def fromBytes(cls, data: bytes, name: str):
        '''
        Construct a new `lunarcord.Attachment` from the given `data`.
        
        Parameters
        ----------
        data: `bytes`
            The attachment's data, in raw bytes.
            
        name: `str`
            The attachment name that will be visible on Discord.
            
        Returns
        -------
        attachment: `lunarcord.Attachment`
            The newly created attachment.
        '''
        
        return cls(data, name)
        
    @classmethod
    def fromPath(cls, path: Path, name: str = None):
        '''
        Construct a new `lunarcord.Attachment` from the given `path`.
        
        Parameters
        ----------
        path: `Path`
            The path where the target file is located in.
            
        name: `str`
            The attachment name that will be visible on Discord. If not given, it is taken from the path.
            
        Returns
        -------
        attachment: `lunarcord.Attachment`
            The newly created attachment.
        '''
        
        path: str = path
        
        if isfile(path):
            with open(path, 'rb') as file:
                data = file.read()
                head, tail = split(path)
                
                if name is None:
                    name = tail
        else:
            data = b''
            
            if name is None:
                name = 'unknown.png'
            
        return cls(data, name)
    
    @classmethod
    def fromUrl(cls, url: Url, name: str = None):
        '''
        A method that constructs a new `lunarcord.Attachment` from the given `url`.
        
        Parameters
        ----------
        url: `Url`
            The link associated with the attachment to read from.
            
        name: `str`
            The attachment name that will be visible on Discord.
            
        Returns
        -------
        attachment: `lunarcord.Attachment`
            The newly created attachment.
        '''

        if name is None:
            name = Utils.generateString()

        if type(url) is not str:
            url = str(url)
            
        attachment = cls(b'', name)
        attachment._fromurl = url
        return attachment
    
    @classmethod
    def fromID(cls, id: int, name: str):

        url = f"https://cdn.discordapp.com/attachments/{id}"
        return cls.fromUrl(url, name)
    
    @classmethod
    def fromPayload(cls, bot, payload: dict):

        attachment = Attachment.fromUrl(
            url = payload.get("url"),
            name = payload.get("filename")
        )

        attachment.bot = bot
        return attachment
    
    @classmethod
    def fromAvatar(cls, avatar):
        return cls.fromUrl(avatar.url, avatar.name)
    
    @classmethod
    def new(cls, other, name: str = None):

        try:
            return cls.fromAvatar(other)
        except:
            ...

        x = type(other)

        if x is bytes:
            return cls.fromBytes(other, name)
        if x is dict:
            return cls.fromPayload(None, other)
        if x is int:
            return cls.fromID(other, name)
        if x is str:
            path = cls.fromPath(other, name)
            if path:
                return path
            return cls.fromUrl(other, name)
        
        return cls.new(b'', name)

    async def _setBot(self, bot):

        self.bot = bot

        if self._fromurl:

            data = await self.bot._gateway.manager.get(
                self._fromurl,
                customUrl=True,
                returns=bytes
            )
            self._bytes = data
    
    @classmethod
    async def _convert(cls, object: str, default = None, bot = None, source = None):

        from .basetypes import Interaction

        if type(source) is not Interaction:
            return
        
        try:
            payload = source.attachments[object]
            file = cls.fromPayload(bot, payload)
            await file._setBot(bot)
            return file
        except:
            return
    
    def save(self, name: str = ...):

        if name in (None, ...):
            name = self.name

        with open(name, "wb") as file:
            file.write(self._bytes)
    
    def _toJson(self):
        
        json = {self.name: self._bytes}
        return json
    
    def __repr__(self):
        return f"<Attachment name=\"{self.name}\">"
    
    def __str__(self):
        return self.name
    
    fromData = fromBytes
    fromFile = fromPath
    fromLink = fromUrl