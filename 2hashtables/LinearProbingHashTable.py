import sys

class LinearProbingHashTable:
    def __init__(self, size=1):
        """ Initialize the hash table """
        self.size = size
        self.table = [None] * size  # Using None to indicate empty slots
        self.count = 0
        self.max_load_factor = 0.75  # Lower than separate chaining


        
    def _hash(self, key):
        """ Hash the key to an index in the table """
        return hash(key) % self.size
        
    def _resize(self):
        """ Resize the hash table if load factor is exceeded """
        load_factor = self.count / self.size
        if load_factor > self.max_load_factor:
            old_size = self.size # Uncomment when implementing resizing
            old_table = self.table
            self.size *= 2
            self.table = [None] * self.size
            self.count = 0  # Reset count to reinsert elements
            for element in old_table: 
                if element is not None: 
                    key, value = element
                    self._reinsert(key,value)
            #print (f"changed size from {old_size} to {self.size}") # to comment out later 
            return True
        return False
    
    def _reinsert(self, key, value):
        """ Reinsert a key-value pair into the hash table"""
        index= self._hash(key)
        while self.table[index] is not None:
            index = (index + 1) % self.size
        self.table[index] = (key, value)
        self.count += 1
        
    def insert(self, key):
        """ Insert a key-value pair into the hash table """
        index = self._hash(key) # rewrite the code. 
        if  self.table[index] is None:
            self.table[index] = (key,1)
            self.count += 1
            self._resize()
            return True
        if self.table[index][0] == key:
            # update the value of the key, creating new tuple
            self.table[index] = (key, self.table[index][1] + 1)
            return True
        # handle collisions using linear probing
        while self.table[index] is not None:
            index = (index + 1) % self.size # Linear probing
            if self.table[index] is not None and self.table[index][0] == key:
                # update the value of the key, creating new tuple
                self.table[index] = (key, self.table[index][1] + 1)
                return True
        self.table[index] = (key,1)
        self.count += 1
        self._resize()
        return True

        
        
    def search(self, key):
        """ Search for a key in the hash table """
        # counter implented for prevting the infinite loops. 
        counter = 1
        index = self._hash(key)
        while self.table[index] is not None and counter < self.size:
            if self.table[index][0] == key:
                return True
            #if self.table[index] is None:
            #    return False
            counter += 1
            index = (index + 1) % self.size
        return False

        
    def remove(self, key):
        """ Remove a key from the hash table """
        # Implementation here
        index = self._hash(key)
    
        while self.table[index] is not None:
            if self.table[index][0] == key:
                # Delete the key by setting the slot to None
                self.table[index] = None
                self.count -= 1

                # Start backward shifting
                j = index
                while True:
                    index = (index + 1) % self.size
                    if self.table[index] is None:
                        return  # Done shifting
                    k = self._hash(self.table[index][0])
                    # Check if this entry should be moved back to j
                    if not (j < k <= index or (index < j < k ) or (k <= index < j)):
                        self.table[j] = self.table[index]
                        self.table[index] = None
                        j = index
            else:
                index = (index + 1) % self.size
        
    def __str__(self):
        return str(self.table)

def main():
    hash_table = LinearProbingHashTable(1)
    i = 0

    # Word frequency will be tracked using LinearProbingHashTable
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
    result_word = None

    for entry in hash_table.table:
        if entry is not None:
            key, value = entry
            if value > max_count:
                max_count = value
                result_word = key
            elif value == max_count:
                if key < result_word:
                    result_word = key
    if result_word is not None:
        print(result_word, max_count)

if __name__ == "__main__":
    main()
