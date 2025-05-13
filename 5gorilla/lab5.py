import sys

def main():
  alphabet, matrix, queries = parse()
  gap_score = -4
  for q in queries:
    res = needleman_wunsch(q[0], q[1], gap_score, alphabet, matrix)
    print(res[0] + " " + res[1])
  
def parse():
  inp = sys.stdin.read().strip().split('\n')
  alphabet = inp.pop(0).split()
  matrix = []
  for _ in inp[:len(alphabet)]:
    matrix.append(list(map(int, inp.pop(0).split())))
  num_queries = inp.pop(0)
  queries = []
  for q in inp:
    queries.append(q.split())
  return alphabet, matrix, queries

def precalculate_index(alphabet):
  idx = {}
  for i in range(len(alphabet)):
    idx[alphabet[i]] = i
  return idx

def match_score(c1, c2, idx, matrix):
  return matrix[idx[c1]][idx[c2]]
  
def create_score_matrix(string1, string2, gap_score, idx, matrix):
  score_matrix = []
  for i in range(len(string2) + 1):
    l = []
    for j in range(len(string1) + 1):
      l.append(0)
    score_matrix.append(l)
  for i in range(len(string2) + 1):
    score_matrix[i][0] = gap_score * i
    
  for j in range(len(string1) + 1):
    score_matrix[0][j] = gap_score * j
        
  for i in range(1, len(string2) + 1):
    for j in range(1, len(string1) + 1):
      match = score_matrix[i - 1][j - 1] + match_score(string1[j - 1], string2[i - 1], idx, matrix)
      insert = score_matrix[i][j - 1] + gap_score
      delete = score_matrix[i - 1][j] + gap_score
      score_matrix[i][j] = max(match, insert, delete)
      
  return score_matrix

def needleman_wunsch(string1, string2, gap_score, alphabet, matrix):
  idx = precalculate_index(alphabet)
  score = create_score_matrix(string1, string2, gap_score, idx, matrix)
  res1 = ''
  res2 = ''
  i = len(string2)
  j = len(string1)  
  
  while i > 0 and j > 0:
    score_current = score[i][j]
    score_diagonal = score[i-1][j-1]
    score_up = score[i][j-1]       
    score_left = score[i-1][j]
    
    if score_current == score_diagonal + match_score(string1[j-1], string2[i-1], idx, matrix):
      res1 += string1[j-1]
      res2 += string2[i-1]
      i -= 1
      j -= 1
    elif score_current == score_up + gap_score:
      res1 += string1[j-1]
      res2 += '*'
      j -= 1
    elif score_current == score_left + gap_score:
      res1 += '*'
      res2 += string2[i-1]
      i -= 1

  while j > 0:
    res1 += string1[j-1]
    res2 += '*'
    j -= 1
  while i > 0:
    res1 += '*'
    res2 += string2[i-1]
    i -= 1
    
  res1 = res1[::-1]
  res2 = res2[::-1]
    
  return(res1, res2)

  
main()