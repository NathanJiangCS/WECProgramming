#import sys
import ujson as json
from collections import OrderedDict
from pprint import pprint
#sys.stdin = open("test.txt",'r')

with open('state_matches.json') as data_file:
    data = json.load(data_file)


if data["states"] == "matching":
    student_map = {} #maps student id to student index
    reverse_student_map = {}
    employer_map = {} #Maps employer index to employer id
    posting_map = {} #Maps posting id to employers

    
    tstudents = data["students"]
    temployers = data["employers"]

    #Setting up the mappings
    for i in xrange(len(tstudents)):
        student_map[tstudents[i]["id"]] = i+1
        reverse_student_map[i+1] = tstudents[i]["id"]
    for i in xrange(len(temployers)):
        employer_map[temployers[i]["emp_id"]] = i+1
        posting_id = temployers[i]["posting_id"]
        posting_map[posting_id] = temployers[i]["emp_id"]

    #Setting up data arrays
    students = [[]]
    postings = [[]]

    for i in tstudents:
        pref = []
        for j in i["preferences"]:
            pref.append(j["posting_id"])
        students.append(pref)

    for i in temployers:
        pref = i["preferences_descending"]
        for j in xrange(len(pref)):
            element = pref[j]
            pref[j] = student_map[element]
        postings.append(pref)
    
        

    s = len(students) - 1;
    e = len(postings) - 1;

    sm = [-1 for i in xrange(s+1)]
    em = [-1 for i in xrange(e+1)]

##    for i in xrange(s):
##        a = map(int,raw_input().split())
##        students.append(a)
##
##    for j in xrange(e):
##        a = map(int,raw_input().split())
##        postings.append(a)

    matches = 0

    while matches != s:
        for i in xrange(1, s+1):
            #print i
            if sm[i] == -1:
                student_preference = students[i][0]
                students[i].pop(0)
                if em[student_preference] == -1:
                    em[student_preference] = i
                    matches += 1
                    sm[i] = student_preference
                else: #if its already matched
                    current_match = em[student_preference]
                    for j in postings[student_preference]:
                        if j == current_match:
                            break
                        elif j == i:
                            em[student_preference] = i;
                            sm[i] = student_preference
                            sm[current_match] = -1
                            break
    answer = []
    with open('output_matches.json', 'w') as output:
        for i in xrange(1, len(sm)):
            tempdict = {
                "employer":posting_map[sm[i]],
                "posting":sm[i],
                "student":reverse_student_map[i]
            }
            #tempdict = OrderedDict(sorted(tempdict.items(), key=lambda t: t[0]))
            #parsed = json.loads(tempdict)
        #json_str = json.dumps(answer)
        
        
            output.write(json.dumps(tempdict, indent=4, sort_keys=True))
            if i != len(sm):
                output.write(',\n')
    
data_file.close()
output.close()