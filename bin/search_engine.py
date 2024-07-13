import re
import collections
import math
import os
import redis
 
NON_WORDS = re.compile("[^a-z0-9' ]")
 
# stop words pulled from the below url
# http://www.textfixer.com/resources/common-english-words.txt
STOP_WORDS = set('''a able about across after all almost also am
among an and any are as at be because been but by can cannot
could dear did do does either else ever every for from get got
had has have he her hers him his how however i if in into is it
its just least let like likely may me might most must my neither
no nor not of off often on only or other our own rather said say
says she should since so some than that the their them then
there these they this tis to too twas us wants was we were what
when where which while who whom why will with would yet you
your'''.split())
 
class ScoredIndexSearch(object):
    def __init__(self, prefix, *redis_settings):
        self.prefix = prefix.lower().rstrip(':') + ':'
        self.connection = redis.Redis(*redis_settings)
    
    @staticmethod
    def get_index_keys(content, add=True):
        words = NON_WORDS.sub(' ', content.lower()).split()
        words = [word.strip("'") for word in words]
        words = [word for word in words
                    if word not in STOP_WORDS and len(word) > 1]
        # Apply the Porter Stemmer here if you would like that
        # functionality.
    
        # Apply the Metaphone/Double Metaphone algorithm by itself,
        # or after the Porter Stemmer.
    
        if not add:
            return words
        counts = collections.defaultdict(float)
        for word in words:
            counts[word] += 1
        wordcount = len(words)
        tf = dict((word, count / wordcount)
                    for word, count in counts.iteritems())
        return tf

    def handle_content(self, id, content, add=True):
        keys = self.get_index_keys(content)
        prefix = self.prefix
        pipe = self.connection.pipeline(False)
        if add:
            pipe.sadd(prefix + 'indexed:', id)
            for key, value in keys.iteritems():
                pipe.zadd(prefix + key, id, value)
        else:
            pipe.srem(prefix + 'indexed:', id)
            for key in keys:
                pipe.zrem(prefix + key, id)
    
        # Execute the insertion/removal.
        pipe.execute()
    
        # Return the number of keys added/removed.
        return len(keys)

    
    def search(self, connection, prefix, query_string, offset=0, count=10):
        # Get our search terms just like we did earlier...
        keys = [prefix + key
                for key in self.get_index_keys(query_string, False)]
    
        if not keys:
            return [], 0
    
        total_docs = max(
            connection.scard(prefix + 'indexed:'), 1)
    
        # Get our document frequency values...
        pipe = self.connection.pipeline(False)
        for key in keys:
            pipe.zcard(key)
        sizes = pipe.execute()
    
        # Calculate the inverse document frequencies...
        def idf(count):
            # Calculate the IDF for this particular count
            if not count:
                return 0
            return max(math.log(total_docs / count, 2), 0)
        idfs = map(idf, sizes)
    
        # And generate the weight dictionary for passing to
        # zunionstore.
        weights = dict((key, idfv)
                for key, size, idfv in zip(keys, sizes, idfs)
                    if size)
    
        if not weights:
            return [], 0
    
        # Generate a temporary result storage key
        temp_key = prefix + 'temp:' + os.urandom(8).encode('hex')
        try:
            # Actually perform the union to combine the scores.
            known = connection.zunionstore(temp_key, weights)
            # Get the results.
            ids = connection.zrevrange(
                temp_key, offset, offset+count-1, withscores=True)
        finally:
            # Clean up after ourselves.
            self.connection.delete(temp_key)
        return ids, known