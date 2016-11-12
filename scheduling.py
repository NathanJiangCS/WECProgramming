import json
import dateutil.parser as dp
import time
from datetime import datetime
from math import floor, ceil
import os

script_dir = os.path.dirname(__file__) 
rel_path = "WECTestCases/tc3/"

with open(os.path.join(script_dir, rel_path+'employers.json')) as emp_file:    
    emp = json.load(emp_file)

with open(os.path.join(script_dir, rel_path+'students.json')) as students_file:    
    students = json.load(students_file)


with open(os.path.join(script_dir, rel_path+'state.json')) as state_file:    
    state = json.load(state_file)


def stringToUnix(ISOTime):
    return time.mktime(dp.parse(ISOTime).timetuple())

if state["state"] == "scheduling":
        CHUNKSIZE = 1800


        compSched = {}
        studentSched = {}
        studentPosting = {}
        schedule = []

        for i in emp:
            compSched[i['id']] = []
            for times in i["interviewer_schedule"]:
                a = stringToUnix(times["start_time"])
                b = stringToUnix(times["end_time"])        
                compSched[i['id']].append( (a,b) )

        for i in students:
            studentSched[i["id"]] = []
            for times in i["schedule"]:
                if times['event'] == "lecture":
                    a,b = stringToUnix(times["start_time"]), stringToUnix(times["end_time"])
                    studentSched[i['id']].append( (a,b) )

            studentPosting[i['id']] = {}
            for employer in compSched:
                for posting in state["jobs"]:
                    if (i['id'] in posting["students"]):
                        if not (posting["emp_id"] in studentPosting[i['id']]):
                            studentPosting[i['id']][posting["emp_id"]] = [posting["posting_id"]]
                        elif (not posting["posting_id"] in studentPosting[i['id']][posting["emp_id"]]):
                            studentPosting[i['id']][posting["emp_id"]].append(posting["posting_id"])


        for compID in compSched:
            chunks = {}
            companyAvlbl = compSched[compID]
            candidates = []
            studentPref = {}
            studentsAssigned = {}
            
            
            for job in state["jobs"]:
                if job["emp_id"] == compID:
                    candidates += job["students"]

            for times in companyAvlbl:
                start = times[0]; end = times[1]
                chunks[times[0]] = []
                while start+ CHUNKSIZE <= end:
                    chunks[times[0]].append(-1)
                    start+= CHUNKSIZE

            
            for student in candidates:
                studentsAssigned[student] = False
                
                studentPref[student] = {}
                studentPref[student]["total"] = 0
                
                for startTime in chunks:
                    endTime = startTime + CHUNKSIZE*len(chunks[startTime])
                    studentPref[student][startTime] = [30 for i in xrange(len(chunks[startTime]))]
                    
                    
                    for times in studentSched[student]:
                        if (times[1] < endTime and times[1] > startTime):
                            if (times[0]<startTime):
                                for i in xrange(0, int((times[1]-startTime)/CHUNKSIZE+1)):
                                    studentPref[student][startTime][i] = 0                            
                                studentPref[student][startTime][i+1] = 30 - ((times[1]-startTime)%CHUNKSIZE)/60
                                
                            else:
                                studentPref[student][startTime][int((times[0]-startTime)/CHUNKSIZE)] -=  30-(times[0]-startTime)%CHUNKSIZE/60
                                for i in xrange(int(ceil((times[0]-startTime)/CHUNKSIZE)), int((times[1]-startTime)/CHUNKSIZE)):
                                    studentPref[student][startTime][i] = 0
                                studentPref[student][startTime][i+1] = 30 - ((times[1]-startTime)%CHUNKSIZE)/60

                        elif (times[0] < endTime and times[0] > startTime):
                            if (times[1] > endTime):
                                studentPref[student][startTime][int((times[0]-startTime)/CHUNKSIZE)] -= 30-(times[0]-startTime)%CHUNKSIZE/60
                                for i in xrange(int(ceil((times[0]-startTime)/CHUNKSIZE)), int((endTime-startTime)/CHUNKSIZE)):
                                    studentPref[student][startTime][i] = 0

                        elif (times[0]<startTime and times[1] > endTime):                
                            for i in xrange(0, int((endTime-startTime)/CHUNKSIZE)):
                                studentPref[student][startTime][i] = 0                        
                    
                    studentPref[student]["total"] =  studentPref[student]["total"] + sum(studentPref[student][startTime])
                    
            #print studentPref
            
            
            for startTime in chunks:
                for i in xrange(len(chunks[startTime])):
                    maxStudID = -123
                    maxPref = 0
                    for student in studentPref:
                        if (not studentsAssigned[student]):
                            if studentPref[student][startTime][i] > maxPref:
                                maxPref = studentPref[student][startTime][i]
                                maxStudID = student

                            elif studentPref[student][startTime][i] == maxPref and maxStudID != -123:
                                if (studentPref[student]["total"] < studentPref[maxStudID]["total"]):
                                    maxStudID = student

                    if (maxStudID != -123):                
                        studentsAssigned[maxStudID] = True
                        studentSched[maxStudID].append( (startTime + i*CHUNKSIZE, startTime + (i+1)*CHUNKSIZE ) )

                        scheduleEntry = {}
                        scheduleEntry["student"] = maxStudID
                        scheduleEntry["employer"] = compID
                        scheduleEntry["posting"] = studentPosting[maxStudID][compID][-1]; studentPosting[maxStudID][compID].pop()
                        scheduleEntry["interview_start"] = datetime.fromtimestamp(startTime + i*CHUNKSIZE-3600).isoformat()
                        scheduleEntry["interview_end"] = datetime.fromtimestamp(startTime + (i+1)*CHUNKSIZE-3600).isoformat()

                        schedule.append(scheduleEntry)

            
            
                    

        with open('output.json', 'w') as fp:
            json.dump(schedule, fp)            
                            
            
                    
            
            

    
                        
                    
            
        
        
    
        
               
            



        

