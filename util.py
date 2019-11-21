import dataParser as parser
import random
import pandas as pd
import numpy as np
import os

def getYear(ly):
    if ly == "A" or ly == "Α":
        return 0
    elif ly == "B" or ly=="Β":
        return 1
    elif ly == "C" or ly =="Γ":
        return 2

def generateAvailDays(days, randomDay):
    availDayRange = days.copy()
    availDayRange.remove(randomDay)
    randomDay = random.choice(availDayRange)
    return randomDay
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

    return klassHours
    
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

# global for grouped teachers
grouped_teachers = []

def initGroups(teachers, lessons, lesson_dictionary_filepath):
    # get lesson categories/sets/groups and their subjects
    lesson_sets = parser.readLessonDict(lesson_dictionary_filepath)

    for i in lesson_sets:
        grouped_teachers.append([i[0], []])

    # Join Lesson names with teachers
    Teachers = []
    for i in teachers:
        # teacher code, teacher name, lessons, how much it fits
        element = [teachers[i].code, teachers[i].name, [], 0]
        for j in lessons:
            if j in teachers[i].lessons:
                element[2].append(lessons[j].name)

        Teachers.append(element)

    # find matching teachers and add them with their data
    for teacher in Teachers:
        for x in lesson_sets:
            LessonsInGroup = []
            #LessonsInGroup = x[1].intersection(teacher[2])

            for l in range(0, len(teacher[2])):
                if teacher[2][l] in x[1]:
                    LessonsInGroup.append(teacher[2][l])

            if len(LessonsInGroup) == 0:
                continue

            for index in range(0, len(grouped_teachers)):
                if grouped_teachers[index][0] == x[0]:
                    grouped_teachers[index][1].append([teacher[1], teacher[0], LessonsInGroup, len(LessonsInGroup)/len(teacher[2])])
                    break

    return [lesson_sets, grouped_teachers]

def exportHTML(array, lessons, teachers, tmimataArray):

    locale = "gr"
    style = None

    if not os.path.exists('./output'):
        print("\nOutput folder doesn\' exist. Trying to create folder")
        try:
            os.mkdir('./output')
        except OSError:
            print("Creation of the output directory failed")
        else:
            print("Folder created")

    if not os.path.exists('./data/htmlData.json'):
        hour_axis = ['8:00-9:00', '9:00-10:00', '10:00-11:00',
                     '11:00-12:00', '12:00-1:00', '1:00-2:00', '2:00-3:00']

        day_axis = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        header = "Classroom"
        classrooms = ['A','B','C']
    else:
        data = parser.readHtmlData(locale)
        day_axis = data[0]
        hour_axis = data[1]
        header = data[2]
        classrooms = data[3]

    if os.path.exists('./style/style.css'):
        style = parser.readFile('./style/style.css')

    tmimata = array.shape[0]  # tmima
    days = array.shape[1]  # days
    hours = array.shape[2]  # hours

    htmlList = []

    newArray = np.zeros((len(array), len(array[0]), len(array[0][0])), dtype=object)

    for z in range(0, len(array)):
        for y in range(0 , len(array[0])):
            for x in range(0, len(array[0][0])):
                if array[z][y][x].lessonCode != 0:
                    newArray[z][y][x] = lessons[array[z][y][x].lessonCode].name + " (" + teachers[array[z][y][x].teacherCode].name + ")"

    # export each schedule
    for tmima in range(0, tmimata):

        array2d = newArray[tmima]

        dfarray = np.zeros( (hours, days), dtype=object)
        for day in range(0, days):
            dfarray[:, day] = array2d[day]

        dfarray[ dfarray == 0] = ' '
        df = pd.DataFrame(dfarray, index=hour_axis, columns=day_axis)
        htmlList.append(df.to_html())

    # Creating the html file
    # START
    breakLines = """\n\n<br>\n\n"""

    html_file = ""
    if not style == None:
        html_file = """<html>
<head>
    <link rel="stylesheet" type="text/css" href="./style.css"> 
    <title>Schedule</title>
</head>"""
        parser.writeFile('output/style.css', style)
    else:
        html_file = """<html>
<head>
    <title>Schedule</title>
</head>"""

    bodyElements = "\t"+breakLines.join(htmlList)
    bodyElements = bodyElements.replace("\n", "\n\t")

    substr = "<thead>\n"
    theadlen = len("<thead>\n")
    start = 0

    # Append A class
    for i in range(1, tmimataArray[0]+1):
        index = bodyElements.find(substr, start) + theadlen
        newInput = """\t\t<tr><th colspan = "6" id="Tmima">""" + header+' '+ classrooms[0] + str(i) + """</th></tr>\n"""
        bodyElements = bodyElements[:index] + newInput + bodyElements[index:]
        start = index + len(newInput)

    # Append B class
    for i in range(1, tmimataArray[1]+1):
        index = bodyElements.find(substr, start) + theadlen
        newInput = """\t\t<tr><th colspan = "6" id="Tmima">""" + header+' '+ classrooms[1] + str(i) + """</th></tr>\n"""
        bodyElements = bodyElements[:index] + newInput + bodyElements[index:]
        start = index + len(newInput)

    # Append C class
    for i in range(1, tmimataArray[2]+1):
        index = bodyElements.find(substr, start) + theadlen
        newInput = """\t\t<tr><th colspan = "6" id="Tmima">""" + header+' '+ classrooms[2] + str(i) + """</th></tr>\n"""
        bodyElements = bodyElements[:index] + newInput + bodyElements[index:]
        start = index + len(newInput)

    html_file2 = html_file

    html_file = html_file + \
                """\n<body>\n"""+bodyElements + \
                """\n\n</body>\n</html>"""

    parser.writeFile('output/schedule.html', html_file)