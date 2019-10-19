from entities import *

import json


# Parses files to read data

def readLessonJSON(filepath):
    dict = {}
    with open(filepath) as json_file:
        data = json.load(json_file)
        for p in data['lessons']:
            obj = lesson(p['code'], p['name'], p['classYear'], p['hours'])
            dict[p['code']] = obj
    return dict


def readTeacherJSON(filepath):
    dict = {}
    with open(filepath) as json_file:
        data = json.load(json_file)
        for p in data['teachers']:
            obj = teacher(p['code'], p['name'], p['maxHourDay'], p['maxHourWeek'])
            for lesson_code in p['lessons']:
                obj.addLesson(lesson_code['code'])
            dict[p['code']] = obj

    return dict


def saveLessonJSON(lessons, filepath):
    JSON_lessons = []
    for x in lessons:
        JSON_lessons.append(lessons[x].toObject())
    dataToWrite = '{"lessons": ' + json.dumps(JSON_lessons) + '}'
    # lessonsAsJSON = json.dumps(JSON_lessons)
    lessonsFile = open(filepath, 'w')
    lessonsFile.write(dataToWrite)
    return True

