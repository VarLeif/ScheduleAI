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