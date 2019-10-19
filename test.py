from entities import *
import parser

dict2 = parser.readTeacherJSON('./data/teachers.json')

print("\n\nTest:",dict2)

print("\n\n\n")

dict2[1].lessonCodes()
