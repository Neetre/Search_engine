import os
from typing import Dict
import csv
import json
import requests
import sqlite3
import pandas as pd
import csv
from tqdm import tqdm

class Loader:
    def __init__(self):
        pass

    def load_documents_from_directory(self, directory: str) -> Dict[int, str]:
        documents = {}
        for i, filename in enumerate(os.listdir(directory)):
            if filename.endswith(".txt"):
                data = self.load_txt(os.path.join(directory, filename))
                documents[i] = data
        return documents


    def load_txt(self, filename) -> str:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read() # ?
    
    def load_csv(self, filename)  -> Dict[int, str]:
        documents = {}
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if len(row) > 0:
                    documents[i] = row[0]

        return documents

    def load_json(self, filename)  -> Dict[int, str]:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    def load_db(self, db_path)  -> Dict[int, str]:
        documents = {}
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, content FROM documents")
        for row in cursor.fetchall():
            documents[row[0]] = row[1]
        conn.close()
        return documents

    def load_api(self, api_url)  -> Dict[int, str]:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to load document from API: {response.status_code}")
        
    def load_parquet(self, filename: str, n_lines: int) -> Dict[int, str]:
        try:
            parquet_data = pd.read_parquet(filename, engine="pyarrow")
        except Exception as e:
            print(f"An error occoured while reading the parquet file {filename}: {e}")
    
        title = parquet_data["title"]
        texts = parquet_data["text"]
        documents = {}
        print(f"Tot rows: {n_lines}")
        for c, text in enumerate(texts):
            if n_lines != 0:
                if c == n_lines:
                    print(c)
                    documents[c] = text
                    return documents
                documents[c] = text
            else:
                documents[c] = text
            
            if c % 10000:
                print(f"Row {c} done")
        
        return documents
