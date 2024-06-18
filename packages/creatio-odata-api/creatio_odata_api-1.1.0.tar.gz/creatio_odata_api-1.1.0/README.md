![Creatio](https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Creatio_logo.svg/2560px-Creatio_logo.svg.png)

This Python script is designed for testing the OData API of Creatio. It includes functionality for authentication, making generic HTTP requests to the OData service, and performing various operations on object collections.

Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Examples](#examples)
  - [Authentication](#authentication)
  - [Add a Record to a Collection](#add-a-record-to-a-collection)
  - [Modify a Record in a Collection](#modify-a-record-in-a-collection)
  - [Get Data from a Collection](#get-data-from-a-collection)
  - [Delete a Record from a Collection](#delete-a-record-from-a-collection)
  - [Upload Attachment](#upload-attachment)
- [License](#license)

# Features

- **Authentication**: Authenticate and obtain a session cookie for subsequent requests.
- **HTTP Requests**: Make generic HTTP requests (GET, POST, PATCH, DELETE) to the OData service.
- **Collection Operations**: Interact with object collections, including adding, modifying, and deleting records.
- **Attachment Upload**: Upload attachments to specific fields of object collection instances.
- **Logging**: Enable debugging to log detailed information about HTTP requests and responses.

# Installation

Clone the repository:

```sh
git clone https://github.com/YisusChrist/creatio-odata-api
```

# Usage

1. Set up your environment variables by creating a .env file with the following content:

   ```env
   USERNAME=your_username
   PASSWORD=your_password
   ```

2. Run the following command

   ```sh
   poetry run python creatio-odata-api.py
   ```

# Configuration

- `BASE_URL`: The base URL for the Creatio environment.
- `DEBUG`: Set to True to enable detailed debugging information for HTTP requests and responses.

# Examples

## Authentication

```python
response = authenticate()
```

## Add a Record to a Collection

```python
call_payload = {
   "NatIdCreatio": "c0d4aeb6-0860-4e3f-aa2f-812fc4b3bc97",
   "NatIDAgente": "123456789", # ... other fields ...
}

response = add_collection_data("Call", call_payload, cookie=cookie)
```

## Modify a Record in a Collection

```python
modify_collection_data("Call", id=Id, data={"NatCUPS": "ES0026000010952220KG0F"}, cookie=cookie)
```

## Get Data from a Collection

```python
get_collection_data("Call", cookie=cookie, id=Id)
```

## Delete a Record from a Collection

```python
delete_collection_data("Call", id=Id, cookie=cookie)
```

## Upload Attachment

```python
add_attachment("Collection1", id="IdValue", field_name="Field1", file_path="path/to/file", cookie=cookie)
```

# License

This script is licensed under the [GNU General Public License v3.0](https://opensource.org/licenses/GPL-3.0).
