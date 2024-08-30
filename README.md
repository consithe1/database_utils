# database-utils

## Description

This project intends to create a python package to convert a database into another format like XML, Excel, etc.
In order to do so, the following submodules are available:

### decoders

Subpackages used to convert strings, bytes or bytearrays into python objects. 

#### json

Convert a json element stored as a string, a bytearray or bytes into a python object.

#### protobuf

Convert a protobuf element stored as bytes into a python object. 

### extractors

Subpackages used to extract the content of a database. 

#### SQLite3

Specific extractor used for SQLite3 databases. 

### utils

### writers

## Features to implement

- extractors: sqlite3 WAL
- writers: excel, csv, json
