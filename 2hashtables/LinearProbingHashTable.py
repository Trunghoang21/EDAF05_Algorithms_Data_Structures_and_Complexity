import sys

class LinearProbingHashTable:
    def __init__(self, size=1):
        """ Initialize the hash table """
        self.size = size
        self.table = [(None, None)] * size  # (key, value) pairs or (None, None) for empty
        self.tombstone = (object(), None)  # Special marker for deleted elements
        self.count = 0
        self.max_load_factor = 0.5  # Lower than separate chaining
        self.min_load_factor = 0.125
        
    def _hash(self, key):
        """ Hash the key to an index in the table """
        return hash(key) % self.size
        
    def _resize(self):
        """ Resize the hash table if load factor is exceeded """
        # Implementation here
        
    def insert(self, key):
        """ Insert a key-value pair into the hash table """
        # Implementation here
        
    def search(self, key):
        """ Search for a key in the hash table """
        # Implementation here
        
    def remove(self, key):
        """ Remove a key from the hash table """
        # Implementation here
        
    def __str__(self):
        return 

def main():
    hash_table = SeparateChainingHashTable(1)
    i = 0

    # Word frequency will be tracked here using your hash table
    for line in sys.stdin:
        word = line.strip()
        remove_it = i % 16 == 0

        if hash_table.search(word):
            if remove_it:
                hash_table.remove(word)
            else:
                hash_table.insert(word)
        elif not remove_it:
            hash_table.insert(word)
        i += 1

    # Find most frequent word and break ties by alphabetical order
    max_count = -1

    # Step 1: Find the max count
    for bucket in hash_table.table:
        for key, value in bucket:
            if value > max_count:
                max_count = value

    # Step 2: Among words with max count, pick the smallest in lexicographical order
    result_word = None
    for bucket in hash_table.table:
        for key, value in bucket:
            if value == max_count:
                if result_word is None or key < result_word:
                    result_word = key

    # Print result
    if result_word is not None:
        print(result_word, max_count)

if __name__ == "__main__":
    main()