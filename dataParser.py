from entities import *
import os
import json
import re


# Parses files to read data

def readLessonDict(filepath):
    list = []

    f = open(filepath)

    for x in f:
        if ":" in x:
            str = re.sub('[\s* | : | \n]', "", x)
            list.append([str, set()])
        elif ("\t" in x) or ("    " in x):
            endI = len(list) - 1
            str = re.sub('[\n]', '', x)
            str = str.lstrip()
            list[endI][1].add(str)

    f.close()

    return list

def readLessonJSON(filepath):
    dict = {}
    with open(filepath, encoding="utf-8") as json_file:
        data = json.load(json_file)
        for p in data['lessons']:
            obj = Lesson(p['code'], p['name'], p['classYear'], p['hours'])
            dict[p['code']] = obj
    return dict


def readTeacherJSON(filepath):
    dict = {}
    with open(filepath, encoding="utf-8") as json_file:
        data = json.load(json_file)
        for p in data['teachers']:
            obj = Teacher(p['code'], p['name'], p['maxHourDay'], p['maxHourWeek'])
            for lesson_code in p['lessons']:
                obj.addLesson(lesson_code['code'])
            dict[p['code']] = obj

    return dict


def saveLessonJSON(lessons, filepath):
    data = {}
    data['lessons'] = []
    for x in lessons:
        data['lessons'].append(lessons[x].toObject())

    with open(filepath, "w", encoding="utf-8", buffering=512) as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.flush()
        os.fsync(f.fileno())

    return True


def saveTeacherJSON(lessons, filepath):
    data = {}
    data['teachers'] = []
    for x in lessons:
        data['teachers'].append(lessons[x].toObject())

    with open(filepath, "w", encoding="utf-8", buffering=512) as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.flush()
        os.fsync(f.fileno())

    return True


import re


# Parses files to read data

def readLessonDict(filepath):
    list = []

    f = open(filepath, encoding="utf8")

    for x in f:
        if ":" in x:
            str = re.sub('[\s* | : | \n]', "", x)
            list.append([str, set()])
        elif ("\t" in x) or ("    " in x):
            endI = len(list) - 1
            str = re.sub('[\n]', '', x)
            str = str.lstrip()
            list[endI][1].add(str)

    f.close()

    return list

def readHtmlData(locale = None):

    if locale == None:
        locale = "en"

    days = []
    hours = []

    with open("./data/htmlData.json", encoding="utf8") as json_file:
        data = json.load(json_file)

        days = data[locale]['days']
        hours = data[locale]['hours']

    return [days, hours]

def readFile(pathname):

    f = open(pathname)
    text = ""
    line = f.readline()

    while line:
        text += line
        line = f.readline()
    f.close()

    return text

def writeFile(pathname, text):

    f = open(pathname, "w+")
    f.write(text)
    f.close()