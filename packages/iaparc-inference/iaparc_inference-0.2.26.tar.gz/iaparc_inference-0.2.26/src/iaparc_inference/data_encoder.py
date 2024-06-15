"""
IA Parc Inference data decoder
"""
from calendar import c
from tkinter import E
from typing import Any
import iaparc_inference.encoders as encoders

Error = ValueError | None


class DataEncoder():
    """
    Data Encoder
    This a read-only class that encodes the data
    """

    def __init__(self, conf: dict,):
        """
        Constructor
        Arguments:
        
        """
        self._conf = conf
        self._name = conf["name"]
        self._conf = conf
        
    def encode(self, data: Any) -> tuple[bytes, str, Error]:
        """
        Decode data
        Arguments:
        data: Any
        """
        res = ''.encode()
        contentType = ""
        err = None
        if data is None:
            return res, "", ValueError("No data to encode")
        try:
            match self._conf["type"]:
                case "multimodal":
                    form_data = {}
                    if not isinstance(data, dict):
                        return res, "", ValueError("Data is not a dictionary")
                    for item in self._conf["items"]:
                        if item.get("name") in data:
                            item_name = item.get("name")
                            encoder = DataEncoder(item)
                            res, ct , err = encoder.encode(data[item_name])
                            if err: 
                                return res, "", ValueError(f"{item_name}: {str(err)}")
                            match item["type"]:
                                case "file" | "image" | "binary" | "audio" | "video":
                                    field = (f"{item_name}.bin", res, ct)
                                    form_data[item_name] = field
                                case _:
                                    form_data[item_name] = res                            
                    res, _ct, err = encoders.encode_multipart(form_data)
                    ct_items = _ct.split(":")
                    if len(ct_items) == 1:
                        contentType = ct_items[0].strip()
                    elif len(ct_items) > 1:
                        contentType = ct_items[1].strip()
                    else:
                        contentType = "multipart/form-data"
                    
                case "file" | "binary" | "audio" | "video":
                    res, err = encoders.encode_file(data)
                    contentType = "application/octet-stream"
                case "image":
                    res, err = encoders.encode_image(data)
                    if not err:
                        contentType = f"image/{data.format.lower()}"
                    else:
                        contentType = "image/*"
                case "text" | "string":
                    res, err = encoders.encode_text(data)
                    contentType = "text/plain"
                case "json" | "matrix":
                    res, err = encoders.encode_json(data)
                    contentType = "application/json"
        except Exception as e:
            return res, "", ValueError(f"Error encoding data: {e}")
        return res, contentType, err