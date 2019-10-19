# Entities used for the production of the schedule

class lesson:

    def __init__(self, code, name, class_year, hours):
        self.code = code
        self.name = name
        self.class_year = class_year
        self.hours = hours

    def out(self):
        print("Lesson: ", self.name, "\tCode: ", self.code)

class teacher:

    def __init__(self, code, name, maxHourDay, maxHourWeek):
        self.code = code
        self.name = name
        self.maxHourDay = maxHourDay
        self.maxHourWeek = maxHourWeek
        self.lessons = set()

    def addLesson(self, lesson_code):
        self.lessons.add(lesson_code)

    def out(self):
        print("Teacher: ", self.name, "Code: ", self.code)

    def lessonCodes(self):
        for code in self.lessons:
            print("Code: ", code)

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

    def __init__(self, id, year):
        self.id = id
        self.year = year
        self.Days = []


    def addDay(self, day):
        self.Days.append(day)
        