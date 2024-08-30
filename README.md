# database-extractor

## Description

This project intends to create a python package to extract the content of a database and convert it into a python object.
For the moment, this package can only extract the content of SQLite3 databases.

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

## Features to implement

- extractors: sqlite3 WAL
