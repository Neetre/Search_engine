# Search_engine

## Description

This project is a search engine that uses the vector index and scored index methods. 
The search engine is responsible for searching for documents that contain the terms entered by the user. 
The 'scored index' search engine uses the [Redis](https://redis.io/docs/) database to store the indexes and the documents.

In this package there are two main modules:

- `search_engine_vetoridx.py` - This module is responsible for creating a search engine using the vector index method.

- `search_engine_scoredidx.py` - This module is responsible for creating a search engine using the scored index method.

## Requirements

Make sure to have installed Redis on your machine.

python >= 3.9

To run the project, you need to have Python installed on your machine. You can download Python from the [official website](https://www.python.org/downloads/)

**Setting Up the Environment**

* Windows: `./setup_Windows.bat`
* Linux/macOS: `./setup_Linux.sh`

These scripts will install required dependencies, and build a virtual environment for you if you don't have one.

Also make sure to have installed Redis on your machine. You can download Redis from the [official website](https://redis.io/download)

## Usage

Each module has a main function that can be executed to run the search engine. To run the search engine, you need to execute the main function of the module you want to use.

```bash
cd bin
```

To run the search engine using the vector index method, execute the following command:

```bash
python search_engine_vetoridx.py
```

else to run the search engine using the scored index method, execute the following command:

```bash
python search_engine_scoredidx.py
```

### Note

Before running the "search_engine_vetoridx.py" module, you should insert the document with the terms in the "data/documents.txt" file.
You can look in the "load.py" module to see how the documents are inserted into the search engine, and choose the best function for your case, you have to change it in the "search_engine_vetoridx.py" module.

Example of the search engine using the vector index method:

![input](/data/readme/s_1.png)
![output](/data/readme/s_2.png)

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Author

[Neetre](https://github.com/Neetre)
