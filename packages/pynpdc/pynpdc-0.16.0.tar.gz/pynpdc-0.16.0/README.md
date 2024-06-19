# pynpdc

`pynpdc` is a library for accessing the
[Norwegian Polar Data Centre](https://data.npolar.no/) using Python3. It
provides clients with simple methods for logging in and out as well as fetching
and manipulating datasets and attachments.

It is based on the following REST APIs:

- [NPDC Auth API (Komainu)](https://beta.data.npolar.no/-/docs/auth)
- [NPDC Dataset API (Kinko)](https://beta.data.npolar.no/-/docs/dataset/)

## Getting started

Use

```
pip3 install git+https://gitlab.npolar.no/npdc/core/pynpdc.git
```

to install `pynpdc` into your project.

## Examples for reading datasets

### Get ids and titles from public datasets filtered by a search query

```py
from pynpdc import DatasetClient, DATASET_LIFE_ENTRYPOINT

client = DatasetClient(DATASET_LIFE_ENTRYPOINT)

query = "fimbulisen"
for dataset in client.get_datasets(q=query):
    print(dataset.id, dataset.content["title"])
```

### Get ids and titles from draft datasets for a logged in user

```py
from getpass import getpass
from pynpdc import (
    AUTH_LIFE_ENTRYPOINT,
    DATASET_LIFE_ENTRYPOINT,
    APIException,
    AuthClient,
    DatasetClient,
    DatasetType,
)

auth_client = AuthClient(AUTH_LIFE_ENTRYPOINT)

print("Email: ", end="")
user = input()
password = getpass()

try:
    account = auth_client.login(user, password)
except APIException:
    print("Login failed")
    exit()

client = DatasetClient(DATASET_LIFE_ENTRYPOINT, auth=account)
for dataset in client.get_datasets(type=DatasetType.DRAFT):
    print(dataset.id, dataset.content["title"])
```

### Get metadata for a certain public dataset

```py
import json
from pynpdc import DATASET_LIFE_ENTRYPOINT, DatasetClient

client = DatasetClient(DATASET_LIFE_ENTRYPOINT)

ID = "fdd9eaf1-b426-41af-835d-80b8d55f54db"
dataset = client.get_dataset(ID)
if dataset is None:
    print("dataset not found")
else:
    print(json.dumps(dataset.content, indent=2))
```

## Examples for reading attachments

### Get attachments metadata of a certain public dataset

```py
from pynpdc import DatasetClient, DATASET_LIFE_ENTRYPOINT

client = DatasetClient(DATASET_LIFE_ENTRYPOINT)

ID = "19e96642-8b66-48c7-a66f-50dd05cc6eee"
attachments = client.get_attachments(ID)
for attachment in attachments:
    print(f"{attachment.filename} ({attachment.byte_size} bytes)")
```

### Download all attachments from a certain public dataset as zip file

_The zip file will be downloaded to the same folder as the script_

```py
from os import path
from pynpdc import DATASET_LIFE_ENTRYPOINT, DatasetClient

client = DatasetClient(DATASET_LIFE_ENTRYPOINT)

target_directory = path.dirname(__file__)
ID = "19e96642-8b66-48c7-a66f-50dd05cc6eee"
filepath = client.download_attachments_as_zip(ID, target_directory)
print(filepath)
```

## Examples for creating, updating and deleting datasets and attachments

**:warning: Never use the live endpoints for testing your code because it will
add a lot of noise. Even though it is not possible to publish datasets with
`pytest` this noise should be avoided.**

`urllib3` helps to get rid of the InsecureRequestWarning when you deal with
staging entrypoints. If you get the error

```
ModuleNotFoundError: No module named 'urllib3'
```

install the module with:

```sh
pip3 install urllib3
```

### CRUD dataset (create, read, update, delete)

```py
import urllib3

from pynpdc import (
    AUTH_STAGING_ENTRYPOINT,
    DATASET_STAGING_ENTRYPOINT,
    APIException,
    AuthClient,
    DatasetClient,
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create token by logging in

auth_client = AuthClient(AUTH_STAGING_ENTRYPOINT, verify_ssl=False)
user = "foo@example.org"
password = "1234123412341234"

try:
    account = auth_client.login(user, password)
except APIException as e:
    print("Login failed", e.status_code)
    exit()

# Create a client to talk to the dataset API

dataset_client = DatasetClient(
    DATASET_STAGING_ENTRYPOINT, auth=account, verify_ssl=False
)

# Create a dataset

content = {"title": "pynpdc example from readme"}
dataset = dataset_client.create_dataset(content)
ID = dataset.id

# Read this dataset and show title

dataset = dataset_client.get_dataset(ID)
print(dataset.content["title"])

# Update the dataset

content["title"] = "updated pytest example from readme"
dataset_client.update_dataset(ID, content)

# Read this dataset again and show title

dataset = dataset_client.get_dataset(ID)
print(dataset.content["title"])

# Delete this dataset

dataset_client.delete_dataset(ID)

# Reading this dataset again will return None

dataset = dataset_client.get_dataset(ID)
print(dataset, "is None")
```

### CRUD attachment (create, read, update, delete)

```py
import urllib3

from pynpdc import (
    AUTH_STAGING_ENTRYPOINT,
    DATASET_STAGING_ENTRYPOINT,
    APIException,
    AuthClient,
    DatasetClient,
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create token by logging in

auth_client = AuthClient(AUTH_STAGING_ENTRYPOINT, verify_ssl=False)
user = "foo@example.org"
password = "1234123412341234"

try:
    account = auth_client.login(user, password)
except APIException as e:
    print("Login failed", e.status_code, e.response.request.url)
    exit()

# Create a client to talk to the dataset API

dataset_client = DatasetClient(
    DATASET_STAGING_ENTRYPOINT, auth=account, verify_ssl=False
)

# Create a dataset

content = {"title": "pynpdc example from readme"}
dataset = dataset_client.create_dataset(content)

# Add an attachment

attachment = dataset_client.upload_attachment(
    dataset.id,
    __file__,  # path of this Python script
    title="Optional title",
    description="Optional description",
)

# Read attachment metadata

attachment = dataset_client.get_attachment(dataset.id, attachment.id)
print(f"{attachment.title} ({attachment.filename})")

# Update attachment metadata (all the keys have to be provided)

updated_meta = {
    "description": attachment.description,
    "filename": attachment.filename,
    "title": "Updated title",
}
attachment = dataset_client.update_attachment(dataset.id, attachment.id, **updated_meta)

# Read attachment metadata again

attachment = dataset_client.get_attachment(dataset.id, attachment.id)
print(f"{attachment.title} ({attachment.filename})")

# Delete the attachment

dataset_client.delete_attachment(dataset.id, attachment.id)

# Reading attachment metadata again will return None

attachment = dataset_client.get_attachment(dataset.id, attachment.id)
print(attachment, "is None")

# Delete this dataset

dataset_client.delete_dataset(dataset.id)
```
