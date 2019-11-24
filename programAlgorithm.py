import copy
import time
from entities import *

import numpy as np

import util


class SchoolSchedule:

    def __init__(self, amountOfTmimata, klassHours, lessons, teachers, groups, lessonSets, hx, prelude, interlude):
        self.amountOfTmimata = amountOfTmimata
        self.klassHours = klassHours
        self.lessons = lessons
        self.teachers = teachers
        self.sumLessonsSessions = klassHours[0][2] * amountOfTmimata[0] + klassHours[1][2] * amountOfTmimata[1] + \
                                  klassHours[2][2] * amountOfTmimata[2]
        self.lessonsAssigned = np.zeros(self.sumLessonsSessions, dtype=object)
        self.groups = groups
        self.lessonSets = lessonSets
        self.hx = hx  # weight variable which affects how much to choose an hour
        self.prelude = prelude  # hour used before assigning to the last remaining hours
        self.interlude = interlude
        self.totalHoursAssigned = 0
        self.totalHours = klassHours[0][1] * amountOfTmimata[0] + klassHours[1][1] * amountOfTmimata[1] + klassHours[2][
            1] * amountOfTmimata[2]
        self.ScheduleArray = None
        print("Process spawned")

    # initialize array that holds lesson/teacher assignments! :)
    def populateLessonsAsigned(self):
        index = 0
        for key in self.lessons:

            lessonYear = util.getYear(self.lessons[key].classYear)
            endFor = sum(self.amountOfTmimata[:lessonYear + 1])
            startFor = endFor - self.amountOfTmimata[lessonYear]
            for x in range(startFor, endFor):
                self.lessonsAssigned[index] = AssignedLesson(self.lessons[key].code, -1, x)
                index = index + 1

    # create a list of each lesson's available teachers
    def setLessonsTeachers(self):
        for key in self.teachers:
            for jey in self.lessons:
                if self.lessons[jey].code in self.teachers[key].lessons:
                    self.lessons[jey].teachers.append(self.teachers[key].code)

    # calculate how many hours are needed for each lesson for all tmimata
    def countLessonsTotalHours(self):
        for key in self.lessons:
            self.lessons[key].totalTmimaHours = self.amountOfTmimata[util.getYear(self.lessons[key].classYear)] * \
                                                self.lessons[key].hours

    def assignSingleLessonTeachers(self):
        for key in self.lessons:
            if len(self.lessons[key].teachers) == 1:
                teacherCode = self.lessons[key].teachers[0]

                self.teachers[teacherCode].hoursAssigned = self.teachers[teacherCode].hoursAssigned + self.lessons[
                    key].totalTmimaHours
                self.teachers[teacherCode].lessonsAssigned = self.teachers[teacherCode].lessonsAssigned

                if self.teachers[teacherCode].maxHourWeek < self.teachers[teacherCode].hoursAssigned:
                    print('Η εισαγωγή των δεδομένων που έχετε κάνει είναι λανθασμένη. better use ΕΣΠΑ')
                    print('ERROR => ', self.teachers[teacherCode].name, 'Ώρες: ',
                          self.teachers[teacherCode].hoursAssigned)
                    exit()

                for x in range(0, len(self.lessonsAssigned)):

                    if self.lessonsAssigned[x].lessonCode == self.lessons[key].code:
                        self.lessonsAssigned[x].teacherCode = teacherCode
                        # performance improvement, avoid some repetitions :)
                        if x + 1 != len(self.lessonsAssigned) and self.lessonsAssigned[x + 1].lessonCode != \
                                self.lessons[key].code:
                            break

    def assignLessonTeachers(self):
        np.random.shuffle(self.lessonsAssigned)
        totalRuns = 0
        for i in range(0, len(self.lessonsAssigned)):

            lesSetIn = 0
            for ls in range(0, len(self.lessonSets)):
                if self.lessons[self.lessonsAssigned[i].lessonCode].name in self.lessonSets[ls][1]:
                    lesSetIn = ls
                    break

            if self.lessonsAssigned[i].teacherCode == -1:
                lessonCode = self.lessonsAssigned[i].lessonCode
                weightList = np.zeros(len(self.lessons[lessonCode].teachers))
                index = 0
                totalWeight = 0
                for key in self.lessons[lessonCode].teachers:
                    weight = 0
                    fitProb = 0
                    if self.teachers[key].getRemainingHour() >= self.lessons[key].hours:
                        fitsIn = self.groups[lesSetIn][1]
                        for te in fitsIn:
                            if te[1] == self.teachers[key].code:
                                fitProb = te[3]
                        weight = self.teachers[key].getCurrWeigh(fitProb)

                    weightList[index] = weight
                    totalWeight = totalWeight + weight
                    index = index + 1
                    # print(teachers[key].name, ' hours: ', teachers[key].getRemainingHour())
                    # print(lessons[lessonCode].hours)

                if totalWeight == 0:
                    return False
                weightList = weightList / totalWeight

                chosenTeacher = np.random.choice(self.lessons[lessonCode].teachers, p=weightList)
                self.lessonsAssigned[i].teacherCode = chosenTeacher
                self.teachers[chosenTeacher].hoursAssigned = self.teachers[chosenTeacher].hoursAssigned + self.lessons[
                    lessonCode].hours
                self.teachers[chosenTeacher].lessonsAssigned = self.teachers[chosenTeacher].lessonsAssigned + 1

        for key in self.teachers:
            if self.teachers[key].hoursAssigned == 0:
                # tWLM = teachers with lessons match
                tWLM = set()
                for t in self.teachers:
                    if self.teachers[t] == self.teachers[key]:
                        continue
                    if len(self.teachers[t].lessons.intersection(self.teachers[key].lessons)) > 0:
                        tWLM.add(self.teachers[t].code)

                # print('Teacher: ', teachers[key].name, 'Matches: ', tWLM, '\tWeight: ', teachers[key].getCurrWeigh())
                maxHours = 0
                WHOIS = -1
                for k in tWLM:
                    if maxHours < self.teachers[k].hoursAssigned:
                        maxHours = self.teachers[k].hoursAssigned
                        WHOIS = k
                #                print('Teacher: ', teachers[k].name, ' HoursAssigned: ', teachers[k].hoursAssigned, '\tWeight: ', teachers[k].getCurrWeigh())
                for k in tWLM:
                    if maxHours == self.teachers[k].hoursAssigned:
                        if WHOIS != k and self.teachers[WHOIS].lessonsAssigned < self.teachers[k].lessonsAssigned:
                            WHOIS = k

        return True

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

    def testWeights(self):
        wghtDt = np.dtype([('lesson-code', int), ('tmima-code', int), ('weight', float)])

        weightElements = np.zeros(len(self.lessonsAssigned), dtype=wghtDt)
        for x in range(0, len(self.lessonsAssigned)):
            weightElements[x] = (self.lessonsAssigned[x].lessonCode), (self.lessonsAssigned[x].tmimaCode), (
                self.lessonsAssigned[x].getWeight(self.lessons, self.teachers))

        weightElements = np.sort(weightElements, order='weight')
        weightElements = np.flip(weightElements)

        print(weightElements)

    def getDayHourWeight(self, timetable, day, hour, chosenLessonAssigned, teachers):

        # count how many hours the teacher has on that particular day
        teacherDayHour = 0
        tmimaTotalAssignedHours = 0

        if (self.totalHoursAssigned / self.totalHours) < self.interlude:
            if hour > self.prelude:  # and (self.totalHoursAssigned / self.totalHours >= self.interlude):
                return 0

        # #calculate how many hours each tmima has already settled on the timetable
        for i in range(0, 5):
            for j in range(0, 7):
                if timetable[chosenLessonAssigned.tmimaCode][i][j].lessonCode != 0:
                    tmimaTotalAssignedHours += 1

        # get how many hours teacher has on that day
        for tmima in range(0, sum(self.amountOfTmimata)):
            for k in range(0, 7):
                if timetable[tmima][day][k].teacherCode == chosenLessonAssigned.teacherCode:
                    teacherDayHour = teacherDayHour + 1

        # if a lesson has 2 hours per week, do not allow more than one hour per day
        if self.lessons[chosenLessonAssigned.lessonCode].hours == 2:
            for k in range(0, 7):
                if timetable[chosenLessonAssigned.tmimaCode][day][k].lessonCode == chosenLessonAssigned.lessonCode:
                    return 0

        # if a lesson has 3 or 4 hours, do not allow more than 2 of these per day
        countHours = 0
        if self.lessons[chosenLessonAssigned.lessonCode].hours == 3 or self.lessons[
            chosenLessonAssigned.lessonCode].hours == 4:
            for k in range(0, 7):
                if timetable[chosenLessonAssigned.tmimaCode][day][k].lessonCode == chosenLessonAssigned.lessonCode:
                    countHours += 1
            if countHours == 2:
                return 0

        # CHECK if teacher's limit isn't exceeded on that particular day.
        if teacherDayHour + 1 > teachers[chosenLessonAssigned.teacherCode].maxHourDay:
            return 0

        # an to tmima exei allo mathima ekein tin wra
        if timetable[chosenLessonAssigned.tmimaCode][day][hour].teacherCode != 0:
            return 0

        # an kanei kapoy allou mathima to sigkekrimeno (day,hour), to varos gurnaei 0
        for i in range(0, sum(self.amountOfTmimata)):
            if timetable[i][day][hour].teacherCode == chosenLessonAssigned.teacherCode:
                return 0
        # an exei sunexomenes wres [(day, hour-1),(day, hour-2), (day, hour-1), (day, hour+1), (day, hour+1), (day, hour+2)]
        # einai gemata, to varos gurnaei 0

        # check forward
        if hour <= 4:
            times = 0
            for tmima in range(0, sum(self.amountOfTmimata)):
                tmimaDay = timetable[tmima][day]

                if tmimaDay[hour + 1].teacherCode == chosenLessonAssigned.teacherCode and tmimaDay[
                    hour + 2].teacherCode == chosenLessonAssigned.teacherCode:
                    return 0

                if tmimaDay[hour + 1].teacherCode == chosenLessonAssigned.teacherCode:
                    times = times + 1

                if tmimaDay[hour + 2].teacherCode == chosenLessonAssigned.teacherCode:
                    times = times + 1

            if times >= 2:
                return 0

        # check backwards
        if hour >= 2:
            times = 0
            for tmima in range(0, sum(self.amountOfTmimata)):
                tmimaDay = timetable[tmima][day]
                if tmimaDay[hour - 1].teacherCode == chosenLessonAssigned.teacherCode and tmimaDay[
                    hour - 2].teacherCode == chosenLessonAssigned.teacherCode:
                    return 0

                if tmimaDay[hour - 1].teacherCode == chosenLessonAssigned.teacherCode:
                    times = times + 1

                if tmimaDay[hour - 2].teacherCode == chosenLessonAssigned.teacherCode:
                    times = times + 1

            if times >= 2:
                return 0

        # check back and forth
        if 1 <= hour <= 5:
            times = 0
            for tmima in range(0, sum(self.amountOfTmimata)):
                tmimaDay = timetable[tmima][day]
                if tmimaDay[hour - 1].teacherCode == chosenLessonAssigned.teacherCode and tmimaDay[
                    hour + 1].teacherCode == chosenLessonAssigned.teacherCode:
                    return 0

                if tmimaDay[hour - 1].teacherCode == chosenLessonAssigned.teacherCode:
                    times = times + 1

                if tmimaDay[hour + 1].teacherCode == chosenLessonAssigned.teacherCode:
                    times = times + 1

            if times >= 2:
                return 0

        # n(logn) sunartisi
        teacherHoursAssigned = teachers[chosenLessonAssigned.teacherCode].hoursAssigned
        heavySchedule = teacherHoursAssigned * (math.log(teacherHoursAssigned) + 1) / (teacherDayHour + 1)

        return heavySchedule / (hour + 1) ** self.hx

    def isFinishedState(self, localLessonsAssigned):

        for element in localLessonsAssigned:
            if not element.isCompleted(self.lessons):
                return False

        return True

    def hasSpaces(self, NumArray):

        f_empty = lambda t, d, h, numpyArray: numpyArray[t][d][h].lessonCode == 0 and numpyArray[t][d][
            h].teacherCode == 0

        dimensions = NumArray.shape
        emptyInBetween = 0
        for tmima in range(0, dimensions[0]):
            for day in range(0, dimensions[1]):
                for hour in range(0, dimensions[2]):
                    if f_empty(tmima, day, hour, NumArray) and hour + 1 < dimensions[2]:
                        if not f_empty(tmima, day, hour + 1, NumArray):
                            emptyInBetween += 1

        return emptyInBetween

    def puzzleTimetable(self):
        f_empty = lambda t, d, h, numpyArray: numpyArray[t][d][h].lessonCode == 0 and numpyArray[t][d][
            h].teacherCode == 0

        dimensions = self.ScheduleArray.shape

        emptyTmima = -1
        emptyDay = -1
        emptyHour = -1
        emptyInBetween = 0
        for tmima in range(0, dimensions[0]):
            for day in range(0, dimensions[1]):
                for hour in range(0, dimensions[2]):
                    if f_empty(tmima, day, hour, self.ScheduleArray) and hour + 1 < dimensions[2]:
                        if not f_empty(tmima, day, hour + 1, self.ScheduleArray):
                            emptyTmima = tmima
                            emptyDay = day
                            emptyHour = hour

        # if zero gaps
        if emptyTmima == -1:
            return

        for day in range(0, dimensions[1]):
            if self.ScheduleArray[emptyTmima][day][6].teacherCode != 0:

                assignedLesson = copy.deepcopy(self.ScheduleArray[emptyTmima][day][6])
                teachersCopy = copy.deepcopy(self.teachers)
                if day == emptyDay:
                    teachersCopy[self.ScheduleArray[emptyTmima][day][6].teacherCode].maxHourDay -= 1

                teachersCopy[self.ScheduleArray[emptyTmima][day][6].teacherCode].settledHours -= 1

                assignedLesson.assignedHours -= 1
                weight = self.getDayHourWeight(self.ScheduleArray, emptyDay, emptyHour, assignedLesson, teachersCopy)

                if weight > 0:
                    assignedLesson.assignedHours += 1
                    self.ScheduleArray[emptyTmima][day][6] = AssignedLesson(0, 0, 0)
                    self.ScheduleArray[emptyTmima][emptyDay][emptyHour] = assignedLesson
                    # break
                    return True

        return False

    def programAlgorithm(self):
        # position array
        posArray = np.zeros(35, dtype=object)
        for i in range(0, 5):
            for j in range(0, 7):
                posArray[7 * i + j] = [i, j]

        localLessonsAssigned = copy.deepcopy(self.lessonsAssigned)
        # for element in localLessonsAssigned:
        #     element.out()
        usedLessonKeys = set()
        emptyLesson = AssignedLesson(0, 0, 0)
        array = np.zeros((sum(self.amountOfTmimata), 5, 7), dtype=object)
        array.fill(emptyLesson)

        while not self.isFinishedState(localLessonsAssigned):

            # CALCULATE WEIGHTS FOR EACH ELEMENT IN localLessonsAssigned
            weightAssignedLessons = np.zeros(len(localLessonsAssigned))
            totalWeight = 0
            for x in range(0, len(localLessonsAssigned)):
                weightAssignedLessons[x] = localLessonsAssigned[x].getWeight(self.lessons, self.teachers)
                totalWeight = totalWeight + weightAssignedLessons[x]

            weightAssignedLessons = weightAssignedLessons / totalWeight
            chosenTeacher = np.random.choice(localLessonsAssigned, p=weightAssignedLessons)
            # teachers[chosenTeacher.teacherCode].out()

            # END CALCULATE WEIGHTS

            # CALCULATE WEIGHT FOR DAY N HOUR....
            weightDayHours = np.zeros((35), dtype=float)

            for i in range(0, 5):
                for j in range(0, 7):
                    weightDayHours[7 * i + j] = self.getDayHourWeight(array, i, j, chosenTeacher, self.teachers)

            totalWeight = np.sum(weightDayHours)

            # adieksodo: restart algorithm
            if totalWeight == 0:
                self.prelude += 1
                if self.prelude >= 7:
                    return False
                else:
                    continue

            weightDayHours = np.divide(weightDayHours, totalWeight)

            chosenDayHour = np.random.choice(posArray, p=weightDayHours)

            chosenDay = chosenDayHour[0]
            chosenHour = chosenDayHour[1]

            # Fill all the appropriate variables after picking day n' hour
            array[chosenTeacher.tmimaCode][chosenDay][chosenHour] = chosenTeacher
            chosenTeacher.assignedHours += 1
            self.teachers[chosenTeacher.teacherCode].settledHours += 1
            self.totalHoursAssigned += 1

            #     break

        self.ScheduleArray = array

        return True

    # from here :)
    def runProgramOnce(self):
        startingPrelude = self.prelude
        start_time = time.time()
        self.setLessonsTeachers()
        self.countLessonsTotalHours()

        self.populateLessonsAsigned()
        self.assignSingleLessonTeachers()

        while not self.assignLessonTeachers():
            lessonsAssigned = np.zeros(self.sumLessonsSessions, dtype=object)
            for key in self.teachers:
                self.teachers[key].clear()

            self.populateLessonsAsigned()
            self.assignSingleLessonTeachers()

        counter = 0
        # run algorithm! :
        maxGaps = 1
        gaps = 0
        while True:
            for key in self.teachers:
                self.teachers[key].clearSettledHours()

            self.totalHoursAssigned = 0
            shouldRun = self.programAlgorithm()
            if shouldRun:
                gaps = self.hasSpaces(self.ScheduleArray)
                if gaps <= maxGaps:
                    if self.puzzleTimetable():
                        break
            else:
                # print("failed try: ", counter)
                self.prelude = startingPrelude
                counter += 1

        print("--- %s seconds ---" % (time.time() - start_time))
        return self.ScheduleArray