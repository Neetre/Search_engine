import math
from collections import Counter

class VectorSearch():
    def __init__(self) -> None:
        pass
    
    def magnitude(self, concordance):
        if not isinstance(concordance, dict):
            raise ValueError("Supplied Argument should be of type dict")
        total = 0
        for word, count in concordance.items():
            total += count ** 2
        return math.sqrt(total)
    
    def relation(self, concordance1, concordance2):
        if not isinstance(concordance1, dict):
            raise ValueError("Supplied Argument 1 should be of type dict")
        if not isinstance(concordance2, dict):
            raise ValueError("Supplied Argument 2 should be of type dict")
        relevance = 0
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        magnitude1 = self.magnitude(concordance1)
        magnitude2 = self.magnitude(concordance2)
        if magnitude1 * magnitude2 != 0:
            return topvalue / (magnitude1 * magnitude2)
        else:
            return 0

    def concordance(self, document):
        if not isinstance(document, str):
            raise ValueError('Supplied Argument should be of type string')
        return Counter(document.split())
    
    def auto_index_document(self, document):
        document_lower = document.lower()
        return self.concordance(document_lower)


def main():
    v = VectorSearch()

    documents = {
    0:'''At Scale You Will Hit Every Performance Issue I used to think I knew a bit about performance scalability and how to keep things trucking when you hit large amounts of data Truth is I know diddly squat on the subject since the most I have ever done is read about how its done To understand how I came about realising this you need some background''',
    1:'''Richard Stallman to visit Australia Im not usually one to promote events and the like unless I feel there is a genuine benefit to be had by attending but this is one stands out Richard M Stallman the guru of Free Software is coming Down Under to hold a talk You can read about him here Open Source Celebrity to visit Australia''',
    2:'''MySQL Backups Done Easily One thing that comes up a lot on sites like Stackoverflow and the like is how to backup MySQL databases The first answer is usually use mysqldump This is all fine and good till you start to want to dump multiple databases You can do this all in one like using the all databases option however this makes restoring a single database an issue since you have to parse out the parts you want which can be a pain''',
    3:'''Why You Shouldnt roll your own CAPTCHA At a TechEd I attended a few years ago I was watching a presentation about Security presented by Rocky Heckman read his blog its quite good In it he was talking about security algorithms The part that really stuck with me went like this''',
    4:'''The Great Benefit of Test Driven Development Nobody Talks About The feeling of productivity because you are writing lots of code Think about that for a moment Ask any developer who wants to develop why they became a developer One of the first things that comes up is I enjoy writing code This is one of the things that I personally enjoy doing Writing code any code especially when its solving my current problem makes me feel productive It makes me feel like Im getting somewhere Its empowering''',
    5:'''Setting up GIT to use a Subversion SVN style workflow Moving from Subversion SVN to GIT can be a little confusing at first I think the biggest thing I noticed was that GIT doesnt have a specific workflow you have to pick your own Personally I wanted to stick to my Subversion like work-flow with a central server which all my machines would pull and push too Since it took a while to set up I thought I would throw up a blog post on how to do it''',
    6:'''Why CAPTCHA Never Use Numbers 0 1 5 7 Interestingly this sort of question pops up a lot in my referring search term stats Why CAPTCHAs never use the numbers 0 1 5 7 Its a relativity simple question with a reasonably simple answer Its because each of the above numbers are easy to confuse with a letter See the below''',
    }

    index = {
        0:v.auto_index_document(documents[0]),
        1:v.auto_index_document(documents[1]),
        2:v.auto_index_document(documents[2]),
        3:v.auto_index_document(documents[3]),
        4:v.auto_index_document(documents[4]),
        5:v.auto_index_document(documents[5]),
        6:v.auto_index_document(documents[6]),
    }

    searchterm = input('Enter Search Term: ')
    matches = []

    for i in range(len(index)):
        relation = v.relation(v.concordance(searchterm.lower()),index[i])
        if relation != 0:
            matches.append((relation,documents[i][:100]))

    matches.sort(reverse=True)

    for i in matches:
        print(i[0],i[1])
        
if __name__ == "__main__":
    main()
