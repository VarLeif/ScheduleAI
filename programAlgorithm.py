import random

import numpy as np

from app import *
import util


def setLessonsTeachers():
    for key in teachers:
        for jey in lessons:
            if lessons[jey].code in teachers[key].lessons:
                lessons[jey].teachers.append(teachers[key].code)


setLessonsTeachers()


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


def programAlgorithm():
    usedLessonKeys = set()
    array = np.zeros((3, 5, 7), dtype=object)
    sumLessons = len(lessons)
    days = [0, 1, 2, 3, 4]

    for i in range(0, sumLessons):
        randomer = random.choice(list(lessons.keys()))
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

    print(array)


programAlgorithm()
