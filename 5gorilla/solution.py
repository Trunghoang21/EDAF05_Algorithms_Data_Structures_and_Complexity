import sys

class DP:
    def __init__(self, character_set, scoring_matrix, queries):
        self.character = character_set # contain the sequences of characters
        self.queries = queries # contains the gain matrix matching the sequences of characters.
        self.results = []
        self.scoring_matrix = scoring_matrix
        #self.table = []
        self.gap_penalty = -4
    
    def create_table(self, string):
        st1, st2 = map(list,string.split())
        table = [[0 for _ in range(len(st2) + 1)] for _ in range(len(st1) + 1)]
        # base case values
        table[0][0] = 0
        for i in range(1, len(table[0])):
            table[0][i] = self.gap_penalty * i
        for j in range(1, len(table)):
            table[j][0] = self.gap_penalty * j
        
        #fill the table
        for i in range(1, len(table)):
            for j in range(1, len(table[0])):
                align_score = table[i-1][j-1] + self.get_score(st1[i-1], st2[j-1])
                gap_score1 = table[i-1][j] + self.gap_penalty
                gap_score2 = table[i][j-1] + self.gap_penalty
                table[i][j] = max(align_score, gap_score1, gap_score2)
        return table
    
    def get_score(self, char1, char2):
        return self.scoring_matrix[self.character.index(char1)][self.character.index(char2)]

    def string_alignment(self, table, str):
        st1, st2 = map(list,str.split())
        str1 = []
        str2 = []
        i = len(table)  -1
        j = len(table[0]) -1
        while i > 0 and j > 0:
            if table[i][j] == table[i-1][j-1] + self.get_score(st1[i-1],st2[j-1]):
                str1.append(st1[i-1])
                str2.append(st2[j-1])
                i -= 1
                j -= 1
            elif table[i][j] == table[i-1][j] + self.gap_penalty:
                str1.append(st1[i-1])
                str2.append('*')
                i -= 1
            else:
                str2.append(st2[j-1])
                str1.append('*')
                j -= 1
        while i > 0:  # Handle remaining characters in string1
            str1.append(st1[i-1])
            str2.append('*')
            i -= 1
    
        while j > 0:  # Handle remaining characters in string2
            str1.append('*')
            str2.append(st2[j-1])
            j -= 1
        return (''.join(reversed(str1)), ''.join(reversed(str2)))

    def get_results(self, strings):
        results = []
        for str in strings:
            table = self.create_table(str)
            result = self.string_alignment(table, str)
            results.append(result)

        return results

def main():
    character_set = sys.stdin.readline().split()
    matrix = [[] for _ in range(len(character_set))]

    # create a matrix for the scoring. 
    for i in range(len(character_set)):
        ws = list(map(int, sys.stdin.readline().split()))
        matrix[i] = ws
    
    # read the number of queries
    number_of_queries = int(sys.stdin.readline().strip())
    
    # read the queries
    queries = []
    for i in  range(number_of_queries):
        queries.append(sys.stdin.readline().strip())

    dp = DP(character_set, matrix, queries)
    results = dp.get_results(queries)
    for i in range(len(results)):
        print(results[i][0] + " " + results[i][1])


if __name__ == "__main__":
    main()
    
    