import base64
import datetime
import gzip
import json
from pathlib import Path
import mimetypes

from PIL import Image

import yaml

from quaac import Document, Attachment

# doc = Document.from_yaml_file('qa_data.yaml')

from quaac.models import DataPoint, Equipment, User, BaseModel, ConfigDict, Literal, Field, \
    field_serializer, Document
from quaac.common import HashModel

s = Document.model_json_schema()
m = json.dumps(s, indent=4)
with open('new_schema.json', 'w') as f:
    f.write(m)
a = Attachment.from_file(Path(r"C:\Users\jkern\OneDrive\Pictures\Screenshots\Screenshot 2024-01-16 152432.png"))
# b.to_file('test.png')

# a = Attachment(name="Screenshot 2024-01-16 152432.png", encoding="base64", compression="gzip", content="H4sIAAAAAAAAA...")
e = Equipment(name="TrueBeam 1", type="L", serial_number="12345", manufacturer="Varian", model="TrueBeam")
u = User(name="John Doe", email="j@j.com")
d = DataPoint(name="DP1", perform_datetime=datetime.datetime.now(), measurement_value=3, measurement_unit="cGy", performer=u, primary_equipment=e, ancillary_equipment=[e], attachments=[a], reviewer=u, parameters={'field size': '10x10cm', 'ssd': '100cm'})
doc = Document(version='1', datapoints=[d])

schema = doc.model_json_schema()
with open('schema.json', 'w') as f:
    f.write(json.dumps(schema, indent=4))
doc.to_json_file('example.json')
doc_json = doc.from_json_file('example.json')
#
doc.to_yaml_file('example.yaml')
doc_yaml = doc.from_yaml_file('example.yaml')
# with open('example.json', 'w') as f:
#     f.write(doc.model_dump_json(indent=4))

# with open('example.json') as f:
#     doc2 = Document.model_validate_json(f.read())

# with open('example.yaml', 'w') as f:
#     j = doc.model_dump_json(indent=4)
#     y = yaml.safe_load(j)
#     f.write(yaml.dump(y))

linac = Equipment(name="TrueBeam 1", type="Linac", serial_number="12345", manufacturer="Varian", model="TrueBeam")
catphan = Equipment(name="CatPhan 504", type="Phantom", serial_number="A4321", manufacturer="Image Laboratory", model="504")
data = DataPoint(name="6MV Output", parameters={'field size': '10x10cm', 'ssd': '100cm'}, measurement_value=3, measurement_unit="cGy", performer=u, primary_equipment=linac, ancillary_equipment=[catphan], reviewer=u, perform_datetime=datetime.datetime.now())
doc = Document(version='1', datapoints=[data])
doc.to_yaml_file('qa_data.yaml')
doc2 = Document.from_yaml_file('qa_data.yaml')

with open(r"C:\Users\jkern\OneDrive\Pictures\Screenshots\Screenshot 2024-01-16 152432.png", 'rb') as file:
    content = file.read()
c = gzip.compress(content)
data = {'files': [{'encoding': 'base64', 'compression': 'gzip', 'name': 'Screenshot 2024-01-16 152432.png', 'type': 'image/png', 'content': base64.b64encode(c).decode('utf-8'), }]}
with open('file-example.yaml', 'w') as file:
    yaml.dump(data, file)

with open('file-example.yaml', 'r') as file:
    documents = yaml.safe_load(file)
    e = documents['files'][0]['content']
    d = base64.b64decode(e)
    gz = gzip.decompress(d)
    ttt = 1


def read_file_based_on_mimetype(filepath):
    # Guess the MIME type of the file
    mimetype, _ = mimetypes.guess_type(filepath)

    if mimetype is None:
        raise ValueError("Could not determine the MIME type of the file.")

    # Handle different MIME types
    if mimetype.startswith('text/'):
        # Handle text files
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
    elif mimetype in ['image/jpeg', 'image/png']:
        # Handle image files (as an example)
        with open(filepath, 'rb') as file:
            content = file.read()
        # content = Image.open(fp=filepath)
    else:
        # Add more conditions for other MIME types as needed
        raise ValueError(f"Unsupported MIME type: {mimetype}")

    return content

p = Path(r"C:\Users\jkern\OneDrive\Pictures\Screenshots\Screenshot 2024-01-16 152432.png")
p2 = Path(r"C:\Users\jkern\OneDrive\Pictures\Screenshots\stuff_2.7z")
d = read_file_based_on_mimetype(p)
data = d
# gz = gzip.compress(data)
b = base64.b64encode(gz)
ttt = 1