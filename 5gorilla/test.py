import sys

class DP:
    def __init__(self, character_set, scoring_matrix, queries):
        self.queries = queries
        # Create character-to-index lookup dictionary - avoid repeated index lookups
        self.char_to_index = {char: i for i, char in enumerate(character_set)}
        self.scoring_matrix = scoring_matrix
        self.gap_penalty = -4
    
    def get_score(self, char1, char2):
        # Direct index lookup using dictionary - much faster than list.index()
        return self.scoring_matrix[self.char_to_index[char1]][self.char_to_index[char2]]

    def create_table(self, string):
        st1, st2 = string.split()
        len1, len2 = len(st1), len(st2)
        # Preallocate the table with known dimensions
        table = [[0 for _ in range(len2 + 1)] for _ in range(len1 + 1)]
        
        # Precompute gap penalties - avoid repeated multiplication
        for i in range(1, len2 + 1):
            table[0][i] = self.gap_penalty * i
        for j in range(1, len1 + 1):
            table[j][0] = self.gap_penalty * j
        
        # Fill the table - use local variables to avoid attribute lookups
        gap_penalty = self.gap_penalty
        for i in range(1, len1 + 1):
            c1 = st1[i-1]
            for j in range(1, len2 + 1):
                c2 = st2[j-1]
                align_score = table[i-1][j-1] + self.get_score(c1, c2)
                gap_score1 = table[i-1][j] + gap_penalty
                gap_score2 = table[i][j-1] + gap_penalty
                table[i][j] = max(align_score, gap_score1, gap_score2)
        
        return table, st1, st2
    
    def string_alignment(self, table, st1, st2):
        # Preallocate lists with estimated capacity
        str1, str2 = [], []
        i, j = len(st1), len(st2)
        
        # Optimize backtracking - use direct string insertion
        while i > 0 and j > 0:
            current = table[i][j]
            diag = table[i-1][j-1] + self.get_score(st1[i-1], st2[j-1])
            
            if current == diag:
                str1.append(st1[i-1])
                str2.append(st2[j-1])
                i -= 1
                j -= 1
            elif current == table[i-1][j] + self.gap_penalty:
                str1.append(st1[i-1])
                str2.append('*')
                i -= 1
            else:
                str1.append('*')
                str2.append(st2[j-1])
                j -= 1
        
        # Handle remaining characters more efficiently
        while i > 0:
            str1.append(st1[i-1])
            str2.append('*')
            i -= 1
        
        while j > 0:
            str1.append('*')
            str2.append(st2[j-1])
            j -= 1
        
        # Reverse and join in one operation each
        return (''.join(reversed(str1)), ''.join(reversed(str2)))

    def get_results(self):
        results = []
        # Process each query only once
        for query in self.queries:
            table, st1, st2 = self.create_table(query)
            result = self.string_alignment(table, st1, st2)
            results.append(result)
        return results

def main():
    character_set = sys.stdin.readline().split()
    
    # Read scoring matrix with list comprehension - more efficient
    scoring_matrix = [list(map(int, sys.stdin.readline().split())) 
                     for _ in range(len(character_set))]
    
    # Read queries directly into a list
    number_of_queries = int(sys.stdin.readline().strip())
    queries = [sys.stdin.readline().strip() for _ in range(number_of_queries)]

    # Process all alignments
    dp = DP(character_set, scoring_matrix, queries)
    results = dp.get_results()
    
    # Print results efficiently
    for result in results:
        print(f"{result[0]} {result[1]}")

if __name__ == "__main__":
    main()