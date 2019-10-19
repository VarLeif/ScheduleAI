from entities import *

import json

# Parses files to read data

def readLessonJSON(filepath):
    dict = {}
    with open(filepath) as json_file:
        data = json.load(json_file)
        for p in data['lessons']:
            obj = lesson(p['code'],p['name'],p['class_year'],p['hours'])
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
