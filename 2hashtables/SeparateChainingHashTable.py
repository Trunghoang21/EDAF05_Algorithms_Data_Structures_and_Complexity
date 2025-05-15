import sys

class SeparateChainingHashTable: 
    def __init__(self, size=1):
        """ initialize the hash table """ 
        self.size = size 
        self.table = [[] for _ in range(size)]
        self.count = 0
        self.max_load_factor = 0.95 # to change later. 
        self.min_load_factor = 0.1 # to change later
    
    def _hash(self, key):
        """ hash the key to an index in the table """
        return hash(key) % self.size
    
    def _resize(self):
        """ resize the hash table if load factor is exceeded """
        old_seize = self.size
        load_factor = self.count / self.size
        if (load_factor > self.max_load_factor) or  (load_factor < self.min_load_factor):
            while (self.count / self.size ) > self.max_load_factor:
                self.size *= 2
                     
            while (self.count / self.size ) < self.min_load_factor and self.size > 1:
                self.size //= 2
        
            #print (f"chang size from {old_seize} to {self.size}") # to comment out later

            new_table = [[] for _ in range(self.size)]
            for bucket in self.table:
                for key, value in bucket:
                    index = hash(key) % self.size
                    new_table[index].append((key, value))
            self.table = new_table
        else:
            #print (f"load factor is {load_factor}, no need to resize")
            return False        
        
        return True 
    
    def insert(self, key):
        """insert a key-value pair into the hash table""" 
        index = self._hash(key)
        bucket = self.table[index]
        if len (bucket) == 0:
            bucket.append((key, 1))
            self.count += 1
        else:
            find_key = False
            for i in range (len(bucket)):
                if bucket[i][0] == key:
                    # update the value of the key, createing new tuple 
                    bucket[i] = (key, bucket[i][1] + 1)
                    find_key = True
                    break
            if not find_key:
                bucket.append((key, 1))
                self.count += 1
        
        _ = self._resize()
        return True
    
    def search(self, key):
        """ search for a key in the hash table"""
        index = self._hash(key)
        bucket = self.table[index]
        for i in range (len(bucket)):
            if bucket[i][0] == key:
                return True
        return False
    
    def remove(self, key):
        """ remove a key from the hash table"""
        index = self._hash(key)
        bucket = self.table[index]
        for i in range (len(bucket)):
            if bucket[i][0] == key:
                # remove the tuple from the bucket by index
                bucket.pop(i)
                self.count -= 1
                _ = self._resize()
                return True 
        return False 
    
    def __str__(self):
        return str(self.table)
    
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