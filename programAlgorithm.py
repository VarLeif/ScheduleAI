import copy
import random
import time

import numpy as np

from app import *
import util

amountOfTmimata = [3, 3, 3]
klassHours = util.getKlassHours(lessons)
sumLessonsSessions = klassHours[0][2] * amountOfTmimata[0] + klassHours[1][2] * amountOfTmimata[1] + klassHours[2][2] * amountOfTmimata[2]
lessonsAssigned = np.zeros(sumLessonsSessions, dtype=object)

start_time = time.time()
# initialize array that holds lesson/teacher assignments! :)
def populateLessonsAsigned():
    index = 0
    for key in lessons:

        lessonYear = util.getYear(lessons[key].classYear)
        endFor = sum(amountOfTmimata[:lessonYear + 1])
        startFor = endFor - amountOfTmimata[lessonYear]
        for x in range(startFor, endFor):
            lessonsAssigned[index] = AssignedLesson(lessons[key].code, -1, x)
            index = index + 1


# create a list of each lesson's available teachers
def setLessonsTeachers():
    for key in teachers:
        for jey in lessons:
            if lessons[jey].code in teachers[key].lessons:
                lessons[jey].teachers.append(teachers[key].code)


# calculate how many hours are needed for each lesson for all tmimata
def countLessonsTotalHours():
    for key in lessons:
        lessons[key].totalTmimaHours = amountOfTmimata[util.getYear(lessons[key].classYear)] * lessons[key].hours


def assignSingleLessonTeachers():
    for key in lessons:
        if len(lessons[key].teachers) == 1:
            teacherCode = lessons[key].teachers[0]

            teachers[teacherCode].hoursAssigned = teachers[teacherCode].hoursAssigned + lessons[key].totalTmimaHours
            teachers[teacherCode].lessonsAssigned = teachers[teacherCode].lessonsAssigned

            if teachers[teacherCode].maxHourWeek < teachers[teacherCode].hoursAssigned:
                print('Η εισαγωγή των δεδομένων που έχετε κάνει είναι λανθασμένη. better use ΕΣΠΑ')
                print('ERROR => ', teachers[teacherCode].name, 'Ώρες: ', teachers[teacherCode].hoursAssigned)
                exit()

            for x in range(0, len(lessonsAssigned)):

                if lessonsAssigned[x].lessonCode == lessons[key].code:
                    lessonsAssigned[x].teacherCode = teacherCode
                    # performance improvement, avoid some repetitions :)
                    if x + 1 != len(lessonsAssigned) and lessonsAssigned[x + 1].lessonCode != lessons[key].code:
                        break


def assignLessonTeachers():
    np.random.shuffle(lessonsAssigned)
    totalRuns = 0
    for i in range(0, len(lessonsAssigned)):

        lesSetIn = 0
        for ls in range(0, len(lessonSets)):
            if lessons[lessonsAssigned[i].lessonCode].name in lessonSets[ls][1]:
                lesSetIn = ls
                break

        if lessonsAssigned[i].teacherCode == -1:
            lessonCode = lessonsAssigned[i].lessonCode
            weightList = np.zeros(len(lessons[lessonCode].teachers))
            index = 0
            totalWeight = 0
            for key in lessons[lessonCode].teachers:
                weight = 0
                fitProb = 0
                if teachers[key].getRemainingHour() >= lessons[key].hours:
                    fitsIn = groups[lesSetIn][1]
                    for te in fitsIn:
                        if te[1] == teachers[key].code:
                            fitProb = te[3]
                    weight = teachers[key].getCurrWeigh(fitProb)

                weightList[index] = weight
                totalWeight = totalWeight + weight
                index = index + 1
                # print(teachers[key].name, ' hours: ', teachers[key].getRemainingHour())
                # print(lessons[lessonCode].hours)

            if totalWeight == 0:
                return False
            weightList = weightList / totalWeight

            chosenTeacher = np.random.choice(lessons[lessonCode].teachers, p=weightList)
            lessonsAssigned[i].teacherCode = chosenTeacher
            teachers[chosenTeacher].hoursAssigned = teachers[chosenTeacher].hoursAssigned + lessons[lessonCode].hours
            teachers[chosenTeacher].lessonsAssigned = teachers[chosenTeacher].lessonsAssigned + 1

    for key in teachers:
        if teachers[key].hoursAssigned == 0:
            # tWLM = teachers with lessons match
            tWLM = set()
            for t in teachers:
                if teachers[t] == teachers[key]:
                    continue
                if len(teachers[t].lessons.intersection(teachers[key].lessons)) > 0:
                    tWLM.add(teachers[t].code)

            # print('Teacher: ', teachers[key].name, 'Matches: ', tWLM, '\tWeight: ', teachers[key].getCurrWeigh())
            maxHours = 0
            WHOIS = -1
            for k in tWLM:
                if maxHours < teachers[k].hoursAssigned:
                    maxHours = teachers[k].hoursAssigned
                    WHOIS = k
            #                print('Teacher: ', teachers[k].name, ' HoursAssigned: ', teachers[k].hoursAssigned, '\tWeight: ', teachers[k].getCurrWeigh())
            for k in tWLM:
                if maxHours == teachers[k].hoursAssigned:
                    if WHOIS != k and teachers[WHOIS].lessonsAssigned < teachers[k].lessonsAssigned:
                        WHOIS = k

            # print(teachers[WHOIS].name)

    return True
    # TODO: kanonikopoiisi


# Check if random hour is in last 2 hours of each day.
# IF it's true, try to find an earlier hour available on the same day
def getHour(array, year, randomDay, randomHour):
    if randomHour in (5, 6):
        for k in range(0, 5):

            # if there's an empty space in the first 5 hours, assign it to the lesson

            if array[year][randomDay][k] == 0:
                randomHour = k

            # If last hour is selected, check if lasthour-1 is available, then assign it

            if randomHour == 6:
                if array[year][randomDay][randomHour - 1] == 0:
                    randomHour = 5

    return randomHour


def testWeights():
    wghtDt = np.dtype([('lesson-code', int), ('tmima-code', int), ('weight', float)])

    weightElements = np.zeros(len(lessonsAssigned), dtype=wghtDt)
    for x in range(0, len(lessonsAssigned)):
        weightElements[x] = (lessonsAssigned[x].lessonCode), (lessonsAssigned[x].tmimaCode), (
            lessonsAssigned[x].getWeight(lessons, teachers))

    weightElements = np.sort(weightElements, order='weight')
    weightElements = np.flip(weightElements)

    print(weightElements)

def getDayHourWeight(timetable, day, hour, chosenLessonAssigned):

    #count how many hours the teacher has on that particular day
    teacherDayHour = 0
    for tmima in range(0, sum(amountOfTmimata)):
        for k in range(0, 6):
            if timetable[tmima][day][k].teacherCode == chosenLessonAssigned.teacherCode:
                teacherDayHour = teacherDayHour +1

    # if a lesson has 2 hours per week, do not allow more than one hour per day
    if lessons[chosenLessonAssigned.lessonCode].hours == 2:
        for k in range(0,6):
            if timetable[chosenLessonAssigned.tmimaCode][day][k].lessonCode == chosenLessonAssigned.lessonCode:
                return 0

    # if a lesson has 3 or 4 hours, do not allow more than 2 of these per day
    countHours = 0
    if lessons[chosenLessonAssigned.lessonCode].hours == 3 or lessons[chosenLessonAssigned.lessonCode].hours == 4:
        for k in range(0,6):
            if timetable[chosenLessonAssigned.tmimaCode][day][k].lessonCode == chosenLessonAssigned.lessonCode:
                countHours += 1
        if countHours == 2:
            return 0

    #CHECK if teacher's limit isn't exceeded on that particular day.
    if teacherDayHour + 1 > teachers[chosenLessonAssigned.teacherCode].maxHourWeek:
        return 0

    # an to tmima exei allo mathima ekein tin wra
    if timetable[chosenLessonAssigned.tmimaCode][day][hour].teacherCode != 0:
        return 0

    # an kanei kapoy allou mathima to sigkekrimeno (day,hour), to varos gurnaei 0
    for i in range(0, sum(amountOfTmimata)):
        if timetable[i][day][hour].teacherCode == chosenLessonAssigned.teacherCode:
            return 0
    # an exei sunexomenes wres [(day, hour-1),(day, hour-2), (day, hour-1), (day, hour+1), (day, hour+1), (day, hour+2)]
    # einai gemata, to varos gurnaei 0

    #check forward
    if hour <= 4:
        times = 0
        for tmima in range(0, sum(amountOfTmimata)):
            tmimaDay = timetable[tmima][day]

            if tmimaDay[hour + 1].teacherCode == chosenLessonAssigned.teacherCode and tmimaDay[hour + 2].teacherCode == chosenLessonAssigned.teacherCode:
                return 0

            if tmimaDay[hour+1].teacherCode == chosenLessonAssigned.teacherCode:
                times = times + 1

            if tmimaDay[hour+2].teacherCode == chosenLessonAssigned.teacherCode:
                times = times + 1

        if times >= 2:
            return 0

    #check backwards
    if hour >= 2:
        times = 0
        for tmima in range(0, sum(amountOfTmimata)):
            tmimaDay = timetable[tmima][day]
            if tmimaDay[hour-1].teacherCode == chosenLessonAssigned.teacherCode and tmimaDay[hour-2].teacherCode == chosenLessonAssigned.teacherCode:
                return 0

            if tmimaDay[hour-1].teacherCode == chosenLessonAssigned.teacherCode:
                times = times + 1

            if tmimaDay[hour-2].teacherCode == chosenLessonAssigned.teacherCode:
                times = times + 1

        if times >= 2:
            return 0

    #check back and forth
    if 1 <= hour <= 5:
        times = 0
        for tmima in range(0, sum(amountOfTmimata)):
            tmimaDay = timetable[tmima][day]
            if tmimaDay[hour-1].teacherCode == chosenLessonAssigned.teacherCode and tmimaDay[hour+1].teacherCode == chosenLessonAssigned.teacherCode:
                return 0

            if tmimaDay[hour-1].teacherCode == chosenLessonAssigned.teacherCode:
                times = times + 1

            if tmimaDay[hour+1].teacherCode == chosenLessonAssigned.teacherCode:
                times = times + 1

        if times >= 2:
            return 0

    #n(logn) sunartisi
    teacherHoursAssigned = teachers[chosenLessonAssigned.teacherCode].hoursAssigned
    heavySchedule = teacherHoursAssigned * (math.log(teacherHoursAssigned) +1) / (teacherDayHour+1)

    # 1/hour => 1/1 > 1/2 > 1/3  (1/hour * tmimaAssignedHours) 1/hour * tmimaAssignedHours = 30/32 -> 1 wra = (*30), pithanotita 2h wra (*15), (3h wra *10) 1/7*30
    return heavySchedule/((hour+1)**2)

    #kalipsi kenou? kalipsi 2oro?

    #25 wres

    #2, keno, 2, keno , 1

    #keno, 2, keno, 2, keno


def isFinishedState(localLessonsAssigned):

    for element in localLessonsAssigned:
        if not element.isCompleted(lessons):
            return False

    return True

def getTeachersFinalState(finalTimeTable):

    perdikakiHours = [0,0,0,0,0]

    for i in range(0, len(finalTimeTable)):
        for j in range(0, len(finalTimeTable[0])):
            for b in range(0, len(finalTimeTable[0][0])):
                if finalTimeTable[i][j][b].teacherCode == teachers[1].code:
                    perdikakiHours[j] += 1

    print(teachers[1].hoursAssigned)
    print(perdikakiHours)


def programAlgorithm():
    #position array
    posArray = np.zeros(35, dtype=object)
    for i in range(0, 5):
        for j in range(0, 7):
            posArray[7*i+j] = [i, j]

    localLessonsAssigned = copy.deepcopy(lessonsAssigned)
    # for element in localLessonsAssigned:
    #     element.out()
    usedLessonKeys = set()
    emptyLesson = AssignedLesson(0, 0, 0)
    array = np.zeros((sum(amountOfTmimata), 5, 7), dtype=object)
    array.fill(emptyLesson)


    while not isFinishedState(localLessonsAssigned):

        #CALCULATE WEIGHTS FOR EACH ELEMENT IN localLessonsAssigned
        weightAssignedLessons = np.zeros(len(localLessonsAssigned))
        totalWeight = 0
        for x in range(0, len(localLessonsAssigned)):
            weightAssignedLessons[x] = localLessonsAssigned[x].getWeight(lessons, teachers)
            totalWeight = totalWeight + weightAssignedLessons[x]

        weightAssignedLessons = weightAssignedLessons / totalWeight
        chosenTeacher = np.random.choice(localLessonsAssigned, p=weightAssignedLessons)
        #teachers[chosenTeacher.teacherCode].out()

        #END CALCULATE WEIGHTS

        # CALCULATE WEIGHT FOR DAY N HOUR....
        weightDayHours = np.zeros((35), dtype=float)

        for i in range(0, 5):
            for j in range(0, 7):
                weightDayHours[7*i+j] = getDayHourWeight(array, i, j, chosenTeacher)

        totalWeight = np.sum(weightDayHours)

        #adieksodo: restart algorithm
        if totalWeight==0:
            return False

        weightDayHours = np.divide(weightDayHours, totalWeight)

        chosenDayHour = np.random.choice(posArray, p=weightDayHours)

        chosenDay = chosenDayHour[0]
        chosenHour = chosenDayHour[1]

        #Fill all the appropriate variables after picking day n' hour
        array[chosenTeacher.tmimaCode][chosenDay][chosenHour] = chosenTeacher
        chosenTeacher.assignedHours += 1
        teachers[chosenTeacher.teacherCode].settledHours += 1

        #     break
    util.exportPDF(array, lessons, teachers)

    return True


groups = 'global'
lessonSets = 'global'

initGroupLessonSet = util.initGroups(teachers, lessons, './data/dictionary.txt')

groups = initGroupLessonSet[1]
lessonSets = initGroupLessonSet[0]

setLessonsTeachers()
countLessonsTotalHours()


def results(teacherName):
    for x in range(0, len(groups)):
        list = groups[x][1]

        for k in range(0, len(list)):
            if list[k][0] == teacherName:
                print(list[k][2])


# from here :)
def runProgramOnce():

    populateLessonsAsigned()
    assignSingleLessonTeachers()

    while not assignLessonTeachers():
        lessonsAssigned = np.zeros(sumLessonsSessions, dtype=object)
        for key in teachers:
            teachers[key].clear()

        populateLessonsAsigned()
        assignSingleLessonTeachers()


    #run algorithm! :
    while True:
        for key in teachers:
            teachers[key].clearSettledHours()

        shouldRun = programAlgorithm()
        if shouldRun:
            break

    print("--- %s seconds ---" % (time.time() - start_time))


def runProgramMany(times):
    totalCount = 0
    for x in range(0, times):
        populateLessonsAsigned()
        assignSingleLessonTeachers()
        while not assignLessonTeachers():
            lessonsAssigned = np.zeros(sumLessonsSessions, dtype=object)
            for key in teachers:
                teachers[key].clear()

            populateLessonsAsigned()
            assignSingleLessonTeachers()
        # #

        # run algorithm! :
        while True:
            for key in teachers:
                teachers[key].clearSettledHours()

            shouldRun = programAlgorithm()
            totalCount += 1
            if shouldRun:
                break

        #clear for restart!
        lessonsAssigned = np.zeros(sumLessonsSessions, dtype=object)
        for key in teachers:
            teachers[key].clear()


    print("I ran successfully, ", times, " out of ", totalCount, " attempts.")
    print("--- %s seconds ---" % (time.time() - start_time))

#
runProgramOnce()
# runProgramMany(10)
