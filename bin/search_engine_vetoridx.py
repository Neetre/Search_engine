import math
from collections import Counter
import numpy as np
from typing import Dict, List, Tuple
import nltk
nltk.download('punkt')


class VectorSearch:
    def __init__(self) -> None:
        self.magnitude_cache: Dict[int, float] = {}

    def magnitude(self, concordance: Dict[str, int]) -> float:
        return sum(count ** 2 for count in concordance.values())

    def relation(self, concordance1: Dict[str, int], concordance2: Dict[str, int]) -> float:
        common_words = set(concordance1.keys()) & set(concordance2.keys())
        topvalue = sum(concordance1[word] * concordance2[word] for word in common_words)
        
        mag1 = self.magnitude_cache.get(id(concordance1)) or self.magnitude(concordance1)
        mag2 = self.magnitude_cache.get(id(concordance2)) or self.magnitude(concordance2)
        
        self.magnitude_cache[id(concordance1)] = mag1
        self.magnitude_cache[id(concordance2)] = mag2
        
        return topvalue / (math.sqrt(mag1) * math.sqrt(mag2)) if mag1 * mag2 != 0 else 0

    def concordance(self, document: str) -> Dict[str, int]:
        if not isinstance(document, str):
            raise ValueError('Supplied Argument should be of type string')
        return Counter(tokenize(document))

    def auto_index_document(self, document: str) -> Dict[str, int]:
        """Create a concordance from a document, converting it to lowercase."""
        document_lower = document.lower()
        return self.concordance(document_lower)


def tokenize(text: str) -> List[str]:
        return nltk.word_tokenize(text.lower())

def load_documents() -> Dict[int, str]:
    """Load documents into a dictionary."""
    return {
        0: '''At Scale You Will Hit Every Performance Issue I used to think I knew a bit about performance scalability and how to keep things trucking when you hit large amounts of data Truth is I know diddly squat on the subject since the most I have ever done is read about how its done To understand how I came about realising this you need some background''',
        1: '''Richard Stallman to visit Australia Im not usually one to promote events and the like unless I feel there is a genuine benefit to be had by attending but this is one stands out Richard M Stallman the guru of Free Software is coming Down Under to hold a talk You can read about him here Open Source Celebrity to visit Australia''',
        2: '''MySQL Backups Done Easily One thing that comes up a lot on sites like Stackoverflow and the like is how to backup MySQL databases The first answer is usually use mysqldump This is all fine and good till you start to want to dump multiple databases You can do this all in one like using the all databases option however this makes restoring a single database an issue since you have to parse out the parts you want which can be a pain''',
        3: '''Why You Shouldnt roll your own CAPTCHA At a TechEd I attended a few years ago I was watching a presentation about Security presented by Rocky Heckman read his blog its quite good In it he was talking about security algorithms The part that really stuck with me went like this''',
        4: '''The Great Benefit of Test Driven Development Nobody Talks About The feeling of productivity because you are writing lots of code Think about that for a moment Ask any developer who wants to develop why they became a developer One of the first things that comes up is I enjoy writing code This is one of the things that I personally enjoy doing Writing code any code especially when its solving my current problem makes me feel productive It makes me feel like Im getting somewhere Its empowering''',
        5: '''Setting up GIT to use a Subversion SVN style workflow Moving from Subversion SVN to GIT can be a little confusing at first I think the biggest thing I noticed was that GIT doesnt have a specific workflow you have to pick your own Personally I wanted to stick to my Subversion like work-flow with a central server which all my machines would pull and push too Since it took a while to set up I thought I would throw up a blog post on how to do it''',
        6: '''Why CAPTCHA Never Use Numbers 0 1 5 7 Interestingly this sort of question pops up a lot in my referring search term stats Why CAPTCHAs never use the numbers 0 1 5 7 Its a relativity simple question with a reasonably simple answer Its because each of the above numbers are easy to confuse with a letter See the below''',
    }


def index_documents(vs: VectorSearch, documents: Dict[int, str]) -> Dict[int, Dict[str, int]]:
    """Index the documents using the VectorSearch class."""
    return {i: vs.auto_index_document(doc) for i, doc in documents.items()}


def search_documents(vs: VectorSearch, documents: Dict[int, str], index: Dict[int, Dict[str, int]], searchterm: str) -> List[Tuple[float, str]]:
    """Search the documents for the given search term."""
    search_concordance = vs.concordance(searchterm.lower())
    matches = []

    for i, doc_concordance in index.items():
        relation = vs.relation(search_concordance, doc_concordance)
        if relation != 0:
            matches.append((relation, documents[i][:100]))

    matches.sort(reverse=True)
    return matches


def main():
    try:
        vs = VectorSearch()
        documents = load_documents()
        index = index_documents(vs, documents)

        searchterm = input('Enter Search Term: ').strip()
        if not searchterm:
            print("Search term cannot be empty.")
            return

        matches = search_documents(vs, documents, index, searchterm)

        if not matches:
            print("No matches found.")
            return

        for relation, snippet in matches:
            print(f"{relation:.4f} {snippet}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
