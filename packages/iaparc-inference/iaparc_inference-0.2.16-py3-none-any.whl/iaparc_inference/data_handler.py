"""
IA Parc Inference data handler
"""
import os
import io
import logging
import logging.config
from tkinter import E
from PIL.Image import Image
from io import BytesIO
import iaparc_inference.decoders as decoders

Error = ValueError | None

LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=LEVEL,
    force=True,
    format="%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
LOGGER = logging.getLogger("Inference")
LOGGER.propagate = True


class DataHandler():
    """
    Data Handler
    This a read-only class that handles the data
    """

    def __init__(self, data: bytes, content_type: str, parameters: dict, conf: dict, uid: str, source: str, is_input: bool = True):
        """
        Constructor
        Arguments:
        
        """
        self._raw = data
        self._content_type = content_type
        self._conf = conf
        self._name = conf["name"]
        self._parameters = parameters
        self._uid = uid
        self._source = source
        self._items = {}       
        ## Init to None data kinds
        self._file: BytesIO | None = None
        self._text: str | None = None
        self._image: Image | None = None
        # self._audio  | None= None
        # self._video | None= None
        self._json: dict | None = None
        #self._table = None
        self._is_multi = self._conf["type"] == "multimodal"
        self.error: Error = None
        self.init_items()
    
    def init_items(self):
        self.items
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def items(self) -> dict:
        if self._is_multi:
            if not self._items:
                raw_items, self.error = decoders.decode_multipart(self._raw, self._conf["items"], self._content_type)
                for item in self._conf["items"]:
                    item_data = raw_items.get(item["name"])
                    if item_data:
                        self._items[item["name"]] = DataHandler(item_data, self._content_type, self._parameters, item, self._uid, self._source, False)
            return self._items
        else:
            if not self._items:
                match self._conf["type"]:
                    case "file", "binary", "audio", "video":
                        self._items[self.name] = self.file
                    case "text", "string":
                        self._items[self.name] = self.text
                    case "image":
                        self._items[self.name] = self.image
                    case "json", "matrix":
                        self._items[self.name] = self.json
                    case _:
                        self._items[self.name] = self._raw
                self._items[self.name] = self
            return self._items
    
    @property
    def raw_data(self) -> bytes:
        return self._raw
    @property
    def parameters(self) -> dict:
        return self._parameters
    
    @property
    def file(self) -> BytesIO | None:
        if self._is_multi or self._conf["type"] not in ["file", "image", "binary", "audio", "video"]:
            return None
        if not self._file:
            self._file, self.error = decoders.decode_file(self._raw)
        return self._file
        
    @property
    def text(self) -> str | None:
        if self._is_multi or self._conf["type"] not in ["text", "string"]:
            return None
        if not self._text:
            self._text, self.error = decoders.decode_text(self._raw)
        return self._text
    
    @property
    def image(self) -> Image | None:
        if self._is_multi or self._conf["type"] != "image":
            return None
        if not self._image:
            self._image, self.error = decoders.decode_image(self._raw)
        return self._image
    
    @property
    def json(self) -> dict | None:
        if self._is_multi or self._conf["type"] != "json":
            return None
        if not self._json:
            self._json, self.error = decoders.decode_json(self._raw)
        return self._json



