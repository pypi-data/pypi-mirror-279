"""
IA Parc Inference data decoder
"""
import operator
from functools import reduce  # forward compatibility for Python 3
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
        self.conf = conf
        self.name = conf["name"]
        self.encoders = {}
        for item in self.conf["items"]:
            if self.conf["type"] == "multimodal":
                self.encoders[item["name"]] = DataEncoder(item)
        self.json_images = self.check_json_images(self.conf["items"])
    
    def check_json_images(self, items: list) -> list:
        elts = []
        for item in items:
            item_name = item.get("name")
            if item_name:
                if item.get("type") in ["image", "file", "binary", "audio", "video"]:
                    elts.append([item.get("name")])
                elif item.get("type") == "json":
                    res = self.check_json_images(item["items"])
                    if len(res) > 0:
                        for k in res:
                            new_elt = [item.get("name")]
                            new_elt.extend(k)
                            elts.append(new_elt)
        return elts
    
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
            match self.conf["type"]:
                case "multimodal":
                    form_data = {}
                    if not isinstance(data, dict):
                        return res, "", ValueError("Data is not a dictionary")
                    for item in self.conf["items"]:
                        if item.get("name") in data:
                            item_name = item.get("name")
                            encoder = self.encoders[item_name]
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
                case "json":
                    res, err = encoders.encode_json(data)
                    if not err:
                        for entry in self.json_images:
                            img_dict = get_by_path(data, entry)
                            keys = img_dict.keys()
                            if len(keys) == 1:
                                set_by_path(data, entry, img_dict[keys[0]])
                    contentType = "application/json"
                case "matrix":
                    res, err = encoders.encode_json(data)
                    contentType = "application/json"
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

        except Exception as e:
            return res, "", ValueError(f"Error encoding data: {e}")
        return res, contentType, err


def get_by_path(root: dict, items: list[str]) -> Any:
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)

def set_by_path(root: dict, items: list[str], value: Any):
    """Set a value in a nested object in root by item sequence."""
    get_by_path(root, items[:-1])[items[-1]] = value

def del_by_path(root: dict, items: list[str]):
    """Delete a key-value in a nested object in root by item sequence."""
    del get_by_path(root, items[:-1])[items[-1]]
