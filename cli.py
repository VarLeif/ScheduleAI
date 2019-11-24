import multiprocessing
import sys
import os
import dataParser as parser
import util
import psutil
import programAlgorithm as algo
from multiprocessing import Process

lessons = None
teachers = None
lessonFilepath = None
teacherFilepath = None
styleFilepath = None
locale = "gr"
outputFilepath = './output/'
amountOfTmimata = [3, 3, 3]

def helpOut():
    print("\n************************")
    print("This is a program/script which produces a schedule for a junior high school. ")
    print("The program/script requires to pass some arguments in order to run, ")
    print("otherwise it will require from the user to have 1 folder with 2 json files: ")
    print("* the lesson json file(-l and the filepath), which has all the lessons with their data, ")
    print("* the teacher json file(-t and the filepath) which has all the teachers with their data.")
    print("The user might also create add a css file(-s and the filepath), which ")
    print("will manipulate the html file(-o for output folder) the program produces (table elements). ")
    print("The user might choose a language with -lang (\"gr\" or \"en\"")
    print("Finally the user can add how many classrooms each year has with -cl number number number")
    print("\t-- (Default values are {3 3 3}.)")
    print("************************\n")


def exists(filepath, param, arg):
    if not os.path.exists(filepath):
        print('Error. File ', filepath, 'doesn\'t exist.')
        return False

    reversed = filepath[::-1]
    dotIndex = reversed.find('.') + 1

    if filepath[len(filepath) - dotIndex:] != param:
        print('File didn\'t match with the file extension: ', arg, filepath)
        return False
    return True


def rerunMsg():
    print("Run python schedule.py --help for help")
    exit(0)


if len(sys.argv) == 2:
    if sys.argv[1] == "--help":
        helpOut()
        exit(0)

if len(sys.argv) < 5 and len(sys.argv) != 2:
    rerunMsg()

if len(sys.argv) >= 5:
    arglist = sys.argv
    # Checks and takes the filepath values for each parameter
    for i in range(0, len(sys.argv)):
        # Lesson parameter -l
        if sys.argv[i] == '-l':
            lessonFilepath = sys.argv[i + 1]
            if not exists(lessonFilepath, '.json', '-l'):
                exit(1)
        # Teacher parameter -t
        if sys.argv[i] == '-t':
            teacherFilepath = sys.argv[i + 1]
            if not exists(teacherFilepath, '.json', '-t'):
                exit(1)
        # Language parameter -lang
        if sys.argv[i] == '-lang':
            locale = sys.argv[i + 1]
        # Style (css) parameter -s
        if sys.argv[i] == '-s':
            styleFilepath = sys.argv[i + 1]
            if not exists(styleFilepath, '.css', '-s'):
                exit(1)
        # Read classrooms for each year
        if sys.argv[i] == '-cl':
            amountOfTmimata[0] = int(sys.argv[i + 1])
            amountOfTmimata[1] = int(sys.argv[i + 2])
            amountOfTmimata[2] = int(sys.argv[i + 3])

    # Check if dictionary.txt and htmlData.json exists
    if not os.path.exists('./data/'):
        print("Missing data folder.")
        exit(1)

    if not os.path.exists('./data/dictionary.txt'):
        print("Missing dictionary.txt. (Subject-field groups")
        exit(1)

    if not os.path.exists('./data/htmlData.json'):
        print("Missing htmlData.json (Tables' header information, language, and school hours)")
        exit(1)

    lessons = parser.readLessonJSON(lessonFilepath)
    teachers = parser.readTeacherJSON(teacherFilepath)
# Initialization of data

# Read PC and OS physical cores in order to distribute computing if available
PhysCores = psutil.cpu_count(logical=False)
noProc = 1

if PhysCores > 2:
    noProc = PhysCores - 1

# Start

# Grouping by subject-field
initGroupLessonSet = util.initGroups(teachers, lessons, './data/dictionary.txt')
groups = initGroupLessonSet[1]
lessonSets = initGroupLessonSet[0]
weightVars = parser.readHeuristic('./data/heuristic.json')
klassHours = util.getKlassHours(lessons)
sumLessonsSessions = klassHours[0][2] * amountOfTmimata[0] + klassHours[1][2] * amountOfTmimata[1] + klassHours[2][2] * \
                     amountOfTmimata[2]

# End

# Variables used in programAlgorithm
klassHours = util.getKlassHours(lessons)


# scheduleAlgo = algo.SchoolSchedule(amountOfTmimata,klassHours,lessons,teachers, groups, lessonSets, weightVars.hx, weightVars.prelude, weightVars.interlude)
# scheduleAlgo.runProgramOnce()

def f(i, solved):
    scheduleAlgo = algo.SchoolSchedule(amountOfTmimata, klassHours, lessons, teachers, groups, lessonSets,
                                       weightVars.hx, weightVars.prelude, weightVars.interlude)
    varBool = scheduleAlgo.runProgramOnce()

    util.exportHTML(scheduleAlgo.ScheduleArray, scheduleAlgo.lessons, scheduleAlgo.teachers, scheduleAlgo.amountOfTmimata)
    solved.set()
    return varBool

if __name__ == '__main__':

    solved = multiprocessing.Event()
    procLis = []
    for i in range(0, noProc):
        procLis.append(Process(target=f, args=(i, solved)))
    for i in range(0, noProc):
        procLis[i].start()

    solved.wait()
    for i in range(0, noProc):
        procLis[i].terminate()
        procLis[i].join()
    print('I got a result! Your result is in the folder', outputFilepath, 'schedule.html')
    # Run program algorithm
