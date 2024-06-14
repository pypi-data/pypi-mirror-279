"""
IA Parc Inference encoders
"""
from PIL.Image import Image
from io import BytesIO

Error = ValueError | None

## Data encoders
def encode_file(file: BytesIO) -> tuple[bytes, Error]:
    """
    Encode file to bytes
    Arguments:
    file: BytesIO
    """
    if not file:
        return b'', ValueError("No data to read")
    if not isinstance(file, BytesIO):
        return b'', ValueError("Data is not a file")
    try:
        data = file.read()
    except Exception as e:
        return b'', ValueError(f"Error encoding file: {e}")
    return data, None

def encode_image(img: Image) -> tuple[bytes, Error]:
    """
    Encode image to bytes
    Arguments:
    img: PIL Image
    """
    from PIL import Image
    data = b''
    if not img:
        return data, ValueError("No data to read")
    if not isinstance(img, Image):
        return data, ValueError("Data is not an image")
    try:        
        data = img.tobytes()
    except Exception as e:
        return data, ValueError(f"Error encoding image: {e}")    
    return data, None

def encode_text(text: str) -> tuple[bytes, Error]:
    """
    Encode text to bytes
    Arguments:
    text: str
    """
    data = b''    
    if not text:
        return data, ValueError("No data to read")
    if not isinstance(text, str):
        return data, ValueError("Data is not a string")
    try:
        data = text.encode("utf-8")
    except Exception as e:
        return data, ValueError(f"Error encoding text: {e}")
    return data, None

def encode_json(in_data: dict) -> tuple[bytes, Error]:
    """
    Encode json to bytes
    Arguments:
    in_data: dict
    """
    data = b''
    from json_tricks import dumps
    if not in_data:
        return data, ValueError("No data to read")
    if not isinstance(in_data, dict):
        return data, ValueError("Data is not a dictionary")
    try:
        s_data = dumps(in_data)
        data = str(s_data).encode("utf-8")                
    except Exception as e:
        return data, ValueError(f"Error encoding json: {e}")
    return data, None

def encode_numpy(in_data: dict) -> tuple[bytes, Error]:
    """
    Encode numpy to bytes
    Arguments:
    in_data: dict
    """
    return encode_json(in_data)

def encode_multipart(data: dict) -> tuple[bytes, str, Error]:
    """
    Encode multi-part data to bytes
    Arguments:
    data: dict
    """
    body = b''
    if not data:
        return body, "", ValueError("No data to read")
    if not isinstance(data, dict):
        return body, "", ValueError("Data is not a dictionary")
    try:
        from urllib3 import encode_multipart_formdata
        body, header = encode_multipart_formdata(data)
        print(body, header)     
    except Exception as e:
        return body, "", ValueError(f"Error encoding multi-part data: {e}")
    return body, header, None

