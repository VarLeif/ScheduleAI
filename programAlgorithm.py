import random
from app import *


def setLessonsTeachers():
    for key in teachers:
        for jey in lessons:
            if lessons[jey].code in teachers[key].lessons:
                lessons[jey].teachers.append(teachers[key].code)


setLessonsTeachers()


def programAlgorithm():
    randPos = random.randint(0, 1000)
    StateTmimatwn = State(3)

    for key in lessons:
        lessons[key].out()


programAlgorithm()

for key in lessons:
    print(lessons[key].teachers)
