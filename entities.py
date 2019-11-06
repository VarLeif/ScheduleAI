import math
from math import factorial
# Entities used for the production of the schedule

class Lesson:

    def __init__(self, code, name, classYear, hours):
        self.code = code
        self.name = name
        self.classYear = classYear
        self.hours = hours
        self.totalTmimaHours = 0
        self.teachers = []

    def out(self):
        print("Μάθημα:", self.name, "\n\tΚωδικός μαθήματος:", self.code, "\n\tΈτος:", self.classYear, "\n\tΏρες:",
              self.hours)

    def toObject(self):
        lessonObj = {
            "code": self.code,
            "name": self.name,
            "classYear": self.classYear,
            "hours": self.hours
        }
        return lessonObj

class Teacher:

    def __init__(self, code, name, maxHourDay, maxHourWeek):
        self.code = code
        self.name = name
        self.maxHourDay = maxHourDay
        self.maxHourWeek = maxHourWeek
        self.lessons = set()
        self.hoursAssigned = 0 #Amount of hours assigned to the teacher
        self.lessonsAssigned = 0 #Amount of lessons assigned to the teacher
        self.settledHours = 0 #Hours that are commited to the timetable

    def addLesson(self, lesson_code):
        self.lessons.add(lesson_code)

    def out(self):
        print("Teacher: ", self.name, "Code: ", self.code, "totalLessons: ", self.getLessonsSum())

    def lessonCodes(self):
        for code in self.lessons:
            print("Code: ", code)

    def getLessonsSum(self):
        return len(self.lessons)

    #returns the number of available hours for "LESSON ASSIGNMENT"
    def getRemainingHour(self):
        return self.maxHourWeek - self.hoursAssigned

    #returns the number of available hours for "TIMETABLE ALGORITHM"
    def getUnsettledHours(self):
        return self.hoursAssigned - self.settledHours

    # WEIGHT: THE BIGGER, THE BETTER (16 better than 15)
    # Positive:
    # - More remaining hours (flexibility)
    # Negative:
    # - Amount of subjects (He's more flexible for later)
    # - hoursOfLesson -> gives some randomness
    def getCurrWeigh(self):
        return math.exp(self.getRemainingHour())  / ((len(self.lessons)) * math.log(math.exp(self.lessonsAssigned +1)))

    # 18 /
    # 20-22 /

    def toObject(self):
        data = {}
        data['code'] = self.code
        data['name'] = self.name
        data['maxHourDay'] = self.maxHourDay
        data['maxHourWeek'] = self.maxHourWeek
        data["lessons"] = []
        for code in self.lessons:
            data["lessons"].append({"code": code})

        return data

    def clear(self):
        self.hoursAssigned=0
        self.lessonsAssigned=0


class Session:

    def __init__(self, hour, lesson_id, teacher_id):
        self.hour = hour
        self.lesson_id = lesson_id
        self.teacher_id = teacher_id


class Day:

    def __init__(self, noDay):
        self.noDay = noDay
        self.Sessions = []
        self.total_hours = 0

    def addSession(self, session):
        self.Sessions.append(session)
        self.total_hours = self.total_hours + 1


class Tmima:

    def __init__(self, id):
        self.id = id
        self.Days = []

    def addDay(self, day):
        self.Days.append(day)


class Klass:

    def __init__(self, year, noTmima):
        self.year = year
        self.hoursWeek = 0
        self.lessonsCount = 0
        self.tmimata = []

        for i in range(0, noTmima):
            self.tmimata.append(Tmima(i + 1))

class AssignedLesson:

    def __init__(self,lessonCode, teacherCode, tmimaCode):
        self.lessonCode = lessonCode
        self.teacherCode = teacherCode
        self.tmimaCode = tmimaCode
        self.assignedHours = 0

    def out(self):
        print('Κωδικός: ', self.lessonCode, ' Καθηγητής: ', self.teacherCode, ' Τμήμα: ', self.tmimaCode)

    def getWeight(self, lessons, teachers):
        return (math.exp(lessons[self.lessonCode].hours - self.assignedHours)) * (teachers[self.teacherCode].getUnsettledHours()**2)
