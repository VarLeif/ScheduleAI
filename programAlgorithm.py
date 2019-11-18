import copy
import random
import datetime

import numpy as np

from app import *
import util

amountOfTmimata = [3, 3, 3]
klassHours = util.getKlassHours(lessons)
sumLessonsSessions = klassHours[0][2] * amountOfTmimata[0] + klassHours[1][2] * amountOfTmimata[1] + klassHours[2][2] * amountOfTmimata[2]
lessonsAssigned = np.zeros(sumLessonsSessions, dtype=object)


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


"""
Epilogi tou :
    
    25 wres tin evdomada swsta? nai!
    
    Kathigitis: hoursAssigned: 22 wres tin evdomada / 25. E PREPEI NA TON VALOYME KAPOY GIATI EXEI LIGES EPILOGES.
    Baros gia ton pinaka assignedLessons -> Epireazetai apo: hoursAssigned, sum(oraMathimathimatos*tmimataKathigiti), sum(oraMathimatos*tmimata)
    prepei na kratame: WresPouExounOristeiGiaTonKathigiti, WresPoyApomenoynGiaAssignmentGiaToTmima
    
    
    exoume N tmimata:
        Briskoume tis desmeumenes wres.
        
Topothetisi tou : (kodikosMathimatos, kathigitis, tmima)
    wX: baros se tmimata
    wY: baros se imera
    wZ: baros se ora
    [tmimata][x1, x2, x3 ,x4 ,x5][1,2,3,4,5,6,7]
    [(({tmima, xn, ora_imeras), wxyz)1, (({tmima, xn, ora_imeras), wxyz)1, ... ,(({tmima, xn, ora_imeras), wxyz)k]

 [komvos]
 171 nodes
 [171 komvoi] -> o kathenas exei [171 paidia] -> -> -> -> -> 
 
 [my_brain].exe [has_stopped.working]
 segmetation fault; core dumped
State:
    parentState/parentNode
    children[]
    array[][][]
    
    
    
    [0][0][4] -> 3 wres sinolika. 
"""


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

    #CHECK if teacher's limit isn't exceeded on that particular day.
    if teacherDayHour + 1 > teachers[chosenLessonAssigned.teacherCode].maxHourWeek:
        return 0

    # an to tmima exei allo mathima ekein tin wra
    if timetable[chosenLessonAssigned.tmimaCode][day][hour] != 0:
        return 0

    # an kanei kapoy allou mathima to sigkekrimeno (day,hour), to varos gurnaei 0
    for i in range(0, sum(amountOfTmimata)):
        if timetable[i][day][hour].teachercode == chosenLessonAssigned.teacherCode:
            return 0
    # an exei sunexomenes wres [(day, hour-1),(day, hour-2), (day, hour-1), (day, hour+1), (day, hour+1), (day, hour+2)]
    # einai gemata, to varos gurnaei 0

    #check forward
    if hour <= 4:
        times = 0
        for tmima in range(0, sum(amountOfTmimata)):
            tmimaDay = timetable[tmima][day]

            if tmimaDay[hour + 1].teacherCode == chosenLessonAssigned.teacherCode and tmimaDay[
                hour + 2].teacherCode == chosenLessonAssigned.teacherCode:
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


    # oso megalutero einai to assignedHours, toso megalutero varos prepei na exoun ta mikra (hour), diladi na mpainei o kathigitis
    #stis prwtes wres, kai na kaluptei 2wra kai oxi 1, keno, 1 keno k.lp.
    #n(logn) sunartisi
    teacherHoursAssigned = teachers[chosenLessonAssigned.teacherCode].hoursAssigned
    heavySchedule = teacherHoursAssigned * (math.log(teacherHoursAssigned) +1)

    #[0,1,2,3,4,5,6]
    # heavySchedule megalo, tote to 0 exei > varos apo to 1,2,3,4,5,6
    # heavySchedule mikro, tote theloyme to varos na douleuei antistrofa. [6,5,4,3,2,1]


    #kalipsi kenou? kalipsi 2oro?

    #25 wres

    #2, keno, 2, keno , 1

    #keno, 2, keno, 2, keno




def programAlgorithm():
    localLessonsAssigned = copy.deepcopy(lessonsAssigned)
    for element in localLessonsAssigned:
        element.out()
    usedLessonKeys = set()
    array = np.zeros((sum(amountOfTmimata), 5, 7), dtype=object)
    #[9][5][7] -> [...][5][7]

    #CALCULATE WEIGHTS FOR EACH ELEMENT IN localLessonsAssigned

    weightAssignedLessons = np.zeros(len(localLessonsAssigned))
    totalWeight = 0
    for x in range(0, len(localLessonsAssigned)):
        weightAssignedLessons[x] = localLessonsAssigned[x].getWeight(lessons, teachers)
        totalWeight = totalWeight + weightAssignedLessons[x]

    weightAssignedLessons = weightAssignedLessons / totalWeight
    chosenTeacher = np.random.choice(localLessonsAssigned, p=weightAssignedLessons)
    teachers[chosenTeacher.teacherCode].out()

    #END CALCULATE WEIGHTS

    # CALCULATE WEIGHT FOR DAY N HOUR....
    weightDayHours = np.zeros((5,7))

    # END CALCULATE WEIGHT FOR DAY N HOUR

    sumLessons = len(lessons)
    # ./. var1: hoursAssignedKathigiti   #var2: sum(oraMathimathimatos*tmimataKathigiti)  #var3: sum(oraMathimatos*tmimata)

    days = [0, 1, 2, 3, 4]

    for i in range(0, sumLessons):
        randomer = random.choice(list(lessons.keys()))
        # change the while loop to get from a set that pops them (randomly)
        while randomer in usedLessonKeys:
            randomer = random.choice(list(lessons.keys()))

        usedLessonKeys.add(randomer)

        year = util.getYear(lessons[randomer].classYear)
        availHours = lessons[randomer].hours

        while availHours != 0:

            randomDay = random.randint(0, 4)
            randomHour = random.randint(0, 6)
            # count unique appearances of a single lesson in a particular day!
            countDayInstances = np.count_nonzero(array[year][randomDay] == lessons[randomer].name)

            # FREQUENCY CHECK:
            # If: a single lesson has only 2 hours per week, do not allow assignment on the same weekday
            # Else: (a lesson has more than 2 hours), allow a maximum of 2 hours for each weekday.
            if lessons[randomer].hours == 2:
                if countDayInstances == 1:
                    randomDay = util.generateAvailDays(days, randomDay)
            else:
                if countDayInstances == 2:
                    randomDay = util.generateAvailDays(days, randomDay)

            # END FREQUENCY CHECK

            while array[year][randomDay][randomHour] != 0:
                randomDay = random.randint(0, 4)
                randomHour = random.randint(0, 6)

            randomHour = getHour(array, year, randomDay, randomHour)

            array[year][randomDay][randomHour] = lessons[randomer].name
            availHours = availHours - 1

    # print(array)
    return array


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

    # for key in teachers:
    #     print('ID: ', teachers[key].code, ' ', teachers[key].name, ' maxHoursPerWeek: ', teachers[key].maxHourWeek,
    #           ' AssignedHours: ', teachers[key].hoursAssigned)
        #results(teachers[key].name)

    return programAlgorithm()


def runProgramMany(times):
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
        lessonsAssigned = np.zeros(sumLessonsSessions, dtype=object)
        for key in teachers:
            teachers[key].clear()


util.exportPDF(runProgramOnce())


# lessonsAss = list(lessonsAssigned)
# # lessonsAss.sort(key=lambda x: x.lessonCode, reverse=False)
# lessonsAssigned = np.array(lessonsAss)

# for x in range(0, len(lessonsAssigned)):
#     lessonsAssigned[x].out()

# testWeights()
# programAlgorithm()
