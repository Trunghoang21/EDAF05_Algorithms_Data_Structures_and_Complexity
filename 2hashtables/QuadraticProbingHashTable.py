import sys

class QuadraticProbingHashTable:
    def __init__(self, size=7):  # Start with a prime number
        """ Initialize the hash table """
        self.size = size
        self.table = [None] * size
        self.count = 0
        self.max_load_factor = 0.5  # Lower for quadratic probing
        self.TOMESTONE = object() # placeholer for deleted elements.
        
    def _hash(self, key):
        """ Hash the key to an index in the table """
        return hash(key) % self.size
        
    def _resize(self):
        """ Resize the hash table if load factor is exceeded """
        load_factor = self.count / self.size
        if load_factor > self.max_load_factor:
            old_size = self.size
            old_table = self.table
            self.size = self.next_Prime(self.size)
            while self.count / self.size > self.max_load_factor:
                self.size = self.next_Prime(self.size) # find next suitable prime number.
            self.table = [None] * self.size # initialize a new table with new size.
            self.count = 0 # Reset count berfore reinserting elements. 
            for element in old_table:
                if element is not None and element is not self.TOMESTONE:
                    key, value = element
                    self._reinsert(key,value)

            #print(f'changed size from {old_size} to {self.size}') # to comment out later
        
        return True 
        
    def _reinsert(self, key, value):
        """ Reinsert a key-value pair into the hash table """
        # Use quadratic probing
        i = 0
        index = (self._hash(key) + i*i) % self.size
        while self.table[index] is not None:
            i += 1
            index = (self._hash(key) + i*i) % self.size
        self.table[index] = (key, value)
        self.count += 1
        
    def insert(self, key):
        """ Insert a key-value pair into the hash table """
        # Use quadratic probing for collisions
        i = 0
        index = (self._hash(key) + i*i )% self.size
        
        existing_key = self.search(key) # check if the key already exists in the table.

        while self.table[index] is not None: 
            if existing_key and self.table[index] is not self.TOMESTONE and self.table[index][0] == key: 
                # Update the value of the key, creating new tuple
                self.table[index] = (key, self.table[index][1] + 1)
                return True
            if not existing_key:
                if self.table[index] is self.TOMESTONE:
                    # Reinsert the key into the table.
                    self.table[index] = (key,1)
                    self.count += 1
                    self._resize()
                    return True
            i += 1
            index = (self._hash(key) + i*i) % self.size
        # encountered an empty slot, insert the key.
        self.table[index] = (key,1)
        self.count += 1
        self._resize()
        return True 

    def search(self, key):
        """ Search for a key in the hash table """
        # Use quadratic probing
        i = 0 
        index = (self._hash(key) + i*i) % self.size
        while self.table[index] is not None:
            if self.table[index] is not self.TOMESTONE and self.table[index][0] == key:
                return True
            i += 1
            index = (self._hash(key) + i*i) % self.size
        return False
    
    def remove(self, key):
        """ Remove a key from the hash table """
        i = 0
        index = (self._hash(key) + i*i) % self.size
        while self.table[index] is not None:
            if self.table[index] is not self.TOMESTONE and self.table[index][0] == key:
                self.table[index] = self.TOMESTONE
                self.count -= 1
                return True  

            i += 1 # continue the search, until reaching an emtpy slot or the key is found. 
            index = (self._hash(key) + i*i) % self.size
        return False
        

    def __str__(self):
        """ String representation of the hash table """
        return str(self.table)
    
    def isPrime(self, n):
        if (n <= 1 ):
            return False
        for i in range(2,n):
            if (n % i == 0):
                return False
        return True
    
    def next_Prime(self, n):
        for i in range(n+1 , 2*n): # the Bertrand's Postulate theorem states that there is always a prime number between n and 2n.
            if (self.isPrime(i)):
                return i

def main():
    hash_table = QuadraticProbingHashTable()
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
        if entry is not None and entry is not hash_table.TOMESTONE:
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
    