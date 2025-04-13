import sys

# read words from input, one word per line
# then use a array to store the words and the count. 

# the size of the array is 16 
size = 16
# create fixed size array: 
my_array = [{} for _ in range(size)]

# the hash function: 
def hash_function(word):
    # hash function to get index
    return hash(word) % size


i = 0

for line in sys.stdin:
	word = line.strip()
	#is_present = word in d
	remove_it = i % 16 == 0
	index = hash_function(word)
	if word in my_array[index]:
		if remove_it:
			del my_array[index][word]
		else:
			count = my_array[index][word]
			my_array[index][word] = count + 1
	else:
		if not remove_it:
			my_array[index][word] = 1
	i += 1

# Find the most frequent word
max_count = 0
max_word = None

# First find the maximum count
for bucket in my_array:
    for word, count in bucket.items():
        if count > max_count:
            max_count = count
            max_word = word
        elif count == max_count and word < max_word:
            max_word = word

# Print the result
print(max_word, max_count)
