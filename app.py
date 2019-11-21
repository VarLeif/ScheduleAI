# Classes required for exporting the data and depicting each entity (lesson, teacher, etc.)
from entities import *
# Parser used to load and save data
import dataParser


lessons_filepath = './data/lessons.json'
teachers_filepath = './data/teachers.json'
teachers = dataParser.readTeacherJSON(teachers_filepath)
lessons = dataParser.readLessonJSON(lessons_filepath)
running = False #show instructions? :D

def printInstructions():
    print("**************************************")
    print("Τι θέλετε να κάνετε; ")
    print("\t 1. Προσθήκη νέου μαθήματος")
    print("\t 2. Προσθήκη νέου καθηγητή")
    print("\t 3. Δημιουργία ωρολογιακού προγράμματος")
    print("\t 4. Αποθήκευση κατάστασης προγράμματος")
    print("\t 5. Εκτύπωση μαθημάτων")
    print("\t 6. Εκτύπωση καθηγητών")
    print("\t 7. Έξοδος με αποθήκευση")
    print("\t 8. Έξοδος χωρίς αποθήκευση")
    print("**************************************")


def createLesson():
    nextCode = lessons[len(lessons)].code + 1  # increment last id!
    print('Παρακαλώ εισάγετε το όνομα του μαθήματος: ')
    lessonName = input()
    print('Παρακαλώ εισάγετε το έτος του μαθήματος (A, B, C)')
    lessonYear = input()
    while lessonYear not in ['A', 'B', 'C']:
        print('Παρακαλώ εισάγετε το έτος του μαθήματος (A, B, C)')
        lessonYear = input()
    print('Παρακαλώ εισάγετε τις εβδομαδιαίες ώρες του μαθήματος')
    lessonHours = int(input())
    while lessonHours < 1 or lessonHours > 10:
        print('Παρακαλώ εισάγετε τις εβδομαδιαίες ώρες του μαθήματος')
        lessonHours = int(input())
    newLesson =  Lesson(nextCode, lessonName, lessonYear, lessonHours)

    return newLesson


while running:
    printInstructions()
    s = int(input())
    if s == 1:
        newLesson = createLesson()
        lessons[newLesson.code] = newLesson
    elif s == 4:
        dataParser.saveLessonJSON(lessons, lessons_filepath)
        dataParser.saveTeacherJSON(teachers, teachers_filepath)
    elif s == 5:
        for x in lessons:
            lessons[x].out()
    elif s == 6:
        for teacher in teachers:
            print(teacher)
    elif s == 7:
        dataParser.saveLessonJSON(lessons, lessons_filepath)
        dataParser.saveTeacherJSON(teachers, teachers_filepath)
        running = False
        break
    elif s == 8:
        running = False
        break

