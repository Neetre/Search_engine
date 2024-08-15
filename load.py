import os
from typing import Dict
import csv
import json
import requests
import sqlite3


class Loader:
    def __init__(self):
        self.documents = {}
        self.i = 0

    def load_documents_from_directory(self, directory: str) -> Dict[int, str]:
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                self.load_txt(self.i, os.path.join(directory, filename))
            self.i += 1
        return self.documents


    def load_txt(self, i, filename):
        with open(filename, "r", encoding="utf-8") as file:
            self.documents[i] = file.read()
    
    def load_csv(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 0:
                    self.documents[self.i] = row[0]

        return self.documents

    def load_json(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            self.documents.append(json.load(file))
        return self.documents

    def load_db(self, db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, content FROM documents")
        for row in cursor.fetchall():
            self.documents[row[0]] = row[1]
        conn.close()
        return documents

    def load_api(self, api_url):
        pass