# Entities used for the production of the schedule

class Lesson:

    def __init__(self, code, name, classYear, hours):
        self.code = code
        self.name = name
        self.classYear = classYear
        self.hours = hours
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
        self.hoursAssigned = 0

    def addLesson(self, lesson_code):
        self.lessons.add(lesson_code)

    def out(self):
        print("Teacher: ", self.name, "Code: ", self.code)

    def lessonCodes(self):
        for code in self.lessons:
            print("Code: ", code)

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
