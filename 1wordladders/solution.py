import fileinput
from collections import Counter
from collections import deque
import sys

def read_word_list():
    """ Read input from standard input """""
    first_line = True
    nbr_of_words_to_read = 0
    nbr_of_search = 0
    words =[]
    searches =[]
    for line in fileinput.input():
        if first_line:
            # Read the first line to get the number of words and searches. 
            first_line_in = line.split()
            nbr_of_words_to_read = int(first_line_in[0])
            nbr_of_search = int(first_line_in[1])
            first_line = False
        else:
            # Read the words and the searches.
            if nbr_of_words_to_read > 0:
                # Read the words
                words.append(line.strip())
                nbr_of_words_to_read -= 1
            else:
                # Read the searches    
                read_line = line.split()
                searches.append([read_line[0], read_line[1]])
                nbr_of_search -= 1
    # Check the indata.                   
    if nbr_of_words_to_read != 0 or nbr_of_search != 0: 
        # Thorw an error when the underlined data is incorrect. 
        raise ValueError("The number of words and searches are not correct.")
    return words, searches

def construct_graph(words):
    """
    Construct a graph from the given word list. 
    The graph is represented as a dictionary where the keys are words and the values are sets of adjacent words.
    """
    graph = {}
    character_frequency_map ={}
    
    for word in words:
        # create nodes
        graph[word] = set()
        character_frequency_map[word] = dict(Counter(word))
    
    #create directed edges
    for word in graph: 
        for other_word in character_frequency_map: 
            if word != other_word:
                if contains_all_characters(dict(Counter(word[-4:])), character_frequency_map[other_word]):
                    # add an edge from word to other_word
                    graph[word].add(other_word)
    return graph

def contains_all_characters(word1, word2):
    """
    Check if word 2 contains all characters from word 1. 
    """
    for char, count in word1.items():
        if char not in word2 or word2[char] < count:
            return False
    return True

def bfs(graph, start, end):
    """ Perform a breadth-first search to find the shortest path from start to end. """
    if start == end:
        return 0
    
    my_queue = deque()
    visited = set()
    my_queue.extend((node, 1) for node in graph[start])
    visited.add(start)
    
    while my_queue:
        (current_word, path_length) = my_queue.popleft()
        if current_word == end:
            return path_length
        else:
            my_queue.extend((node, path_length + 1) for node in graph[current_word] if node not in visited)
            visited.add(current_word)
    return 'Impossible'

def main():
    # Read the word list from the standard input
    read = read_word_list()
    # Construct the graph from the word list
    graph = construct_graph(read[0])
    #print data and searches
    #print(f'data: {read[0]}')
    #print (f'searches: {read[1]}')
    #print graph
    #print(f'graph: {graph}')
    # test the bfs function:
    for search in read[1]:
        print(bfs(graph, search[0], search[1])) 
            
if __name__ == "__main__":
    main()