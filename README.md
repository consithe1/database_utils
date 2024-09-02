# database-extractor

## Description

This project intends to create a python package to extract the content of a database and convert it into a python object.
For the moment, this package can only extract the content of SQLite3 databases.

In this implementation, a row is represented as a python dictionary object. 

Since the goal of this package is to extract the content of a database, BLOB fields will be decoded if possible if they
represent a protobuf or a json. In order to facilitate the data readability, nested protobuf/json objects will be converted to 
unidimensional objects (cf. image below).

![Example of nested-object conversion to unidimensional object](images/transformation.png "Nested-object to unidimensional object")

## Export format

A database can be exported as a JSON or as an XML at the moment. A short exemple of both implementation is given below.

### XML

```xml
<?xml version='1.0' encoding='utf-8'?>
<database name="resources/dummy.db">
    <table name="Tab1">
        <row>
            <column type="str" key="userId" value="C2V6" />
            <column type="NoneType" key="convId" value="None" />
            <column type="str" key="sent" value="0" />
        </row>
    </table>
    <table name="Tab2">
        <row>
            <column type="str" key="convId" value="uaz-57" />
            <column type="int" key="messageId" value="1" />
            <column type="str" key="extKey" value="chat" />
        </row>
        <row>
            <column type="str" key="convId" value="r2d-2a" />
            <column type="int" key="messageId" value="3" />
            <column type="str" key="extKey" value="27FwAPH4QapLXF5fhDcs7" />
        </row>
        <row>
            <column type="str" key="convId" value="av7-dp" />
            <column type="int" key="messageId" value="5" />
            <column type="bytes" key="extKey" value="0000040f" />
        </row>
    </table>
</database>
```

### JSON

```json
{
    "resources/dummy.db": {
        "Tab1": [
            {
                "userId": {
                    "value": "C2V6",
                    "type": "str"
                },
                "convId": {
                    "value": null,
                    "type": "NoneType"
                },
                "sent": {
                    "value": 0,
                    "type": "int"
                }
            }
        ],
        "Tab2": [
            {
                "convId": {
                    "value": "uaz-57",
                    "type": "str"
                },
                "messageId": {
                    "value": 1,
                    "type": "int"
                },
                "extKey": {
                    "value": "chat",
                    "type": "str"
                }
            },
            {
                "convId": {
                    "value": "r2d-2a",
                    "type": "str"
                },
                "messageId": {
                    "value": 3,
                    "type": "int"
                },
                "extKey": {
                    "value": "27FwAPH4QapLXF5fhDcs7",
                    "type": "str"
                }
            },
            {
                "convId": {
                    "value": "av7-dp",
                    "type": "str"
                },
                "messageId": {
                    "value": 5,
                    "type": "int"
                },
                "extKey": {
                    "value": "0000040f",
                    "type": "bytes"
                }
            }
        ]
    }
}
```

## Example

```python
from database_converter.converters.sqlite3.db import SQLite3DatabaseFileConverter
import database_converter.writers.json as json
import database_converter.writers.xml as xml

if __name__ == '__main__':
    # Convert the content of the database into a python object
    extractor = SQLite3DatabaseFileConverter('DB1.db')
    content = extractor.convert()

    # Save as a XML
    xml.write('extraction.xml', content)
    # Save as a JSON
    json.write('extraction.json', content)
```

## Features to implement

- extractors: sqlite3 WAL
