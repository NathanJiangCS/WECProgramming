#import sys
import json
from pprint import pprint
#sys.stdin = open("test.txt",'r')

with open('state_matches.json') as data_file:
    data = json.load(data_file)


pprint(data)
##s, e = map(int,raw_input().split())
##
##students = [[]]
##postings = [[]]
##
##sm = [-1 for i in xrange(s+1)]
##em = [-1 for i in xrange(e+1)]
##
##for i in xrange(s):
##    a = map(int,raw_input().split())
##    students.append(a)
##
##for j in xrange(e):
##    a = map(int,raw_input().split())
##    postings.append(a)
##
##matches = 0
##
##while matches != s:
##    for i in xrange(1, s+1):
##        #print i
##        if sm[i] == -1:
##            student_preference = students[i][0]
##            students[i].pop(0)
##            if em[student_preference] == -1:
##                em[student_preference] = i
##                matches += 1
##                sm[i] = student_preference
##            else: #if its already matched
##                current_match = em[student_preference]
##                for j in postings[student_preference]:
##                    if j == current_match:
##                        break
##                    elif j == i:
##                        em[student_preference] = i;
##                        sm[i] = student_preference
##                        sm[current_match] = -1
##                        break
##                        
##print sm
##print em
