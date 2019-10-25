from entities import Lesson

def getYear(ly):
    if ly == "A":
        return 0
    elif ly == "B":
        return 1
    elif ly == "C":
        return 2

"""
    klassHours [
        [list of lessons of klass] [sum of klass' hours] [sum of lessons] # for class A
        [list of lessons of klass] [sum of klass' hours] [sum of lessons] # for class B
        [list of lessons of klass] [sum of klass' hours] [sum of lessons] # for class C
    ]
"""
def getKlassHours(lessons):
    klassHours = [[[], 0, 0], [[], 0, 0], [[], 0, 0]]
    for key in lessons:
        year = getYear(lessons[key].classYear)
        klassHours[year][0].append(lessons[key])
        klassHours[year][1] = klassHours[year][1] + lessons[key].hours
        klassHours[year][2] = klassHours[year][2] + 1
    
# Check if two Lesson elements are duplicates    
def eqDuplicateLesson(ele1, ele2):
    return ele1.name == ele2.name and ele1.classYear == ele2.classYear

# Creates a list of possible duplicate Lesson elements in the teacher dictionary/json_file
def checkDuplicateLesson(data):
    duplicates = []
    confirmedIndexes = set()
    for ikey in data:
        for jkey in data:
            if ikey == jkey:
                continue
            if ((ikey, jkey) in confirmedIndexes) or ((jkey, ikey) in confirmedIndexes):
                continue
            if eqDuplicateLesson(data[ikey], data[jkey]):
                confirmedIndexes.add((ikey, jkey))
                confirmedIndexes.add((jkey, ikey))
                duplicates.append([data[ikey], data[jkey]])
    return duplicates

# Check if two Teacher elements have identical data
def eqDuplicateTeacher(ele1, ele2):
    sameLessons = ele1.lessons == ele2.lessons
    sameHours = ele1.maxHourDay == ele2.maxHourDay and ele1.maxHourWeek == ele2.maxHourWeek
    sameName = ele1.name == ele2.name
    return sameLessons and sameHours and sameName

# Creates a list of possible duplicate Teacher elements in the teacher dictionary/json_file
def checkDuplicateTeacher(data):
    duplicates = []
    confirmedIndexes = set()
    for ikey in data:
        for jkey in data:
            if ikey == jkey:
                continue
            if ((ikey, jkey) in confirmedIndexes) or ((jkey, ikey) in confirmedIndexes):
                continue
            if eqDuplicateTeacher(data[ikey], data[jkey]):
                confirmedIndexes.add((ikey, jkey))
                confirmedIndexes.add((jkey, ikey))
                duplicates.append([data[ikey], data[jkey]])
    return duplicates
