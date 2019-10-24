from entities import Lesson

def getYear(ly):
    if ly == "A":
        return 0
    elif ly == "B":
        return 1
    elif ly == "C":
        return 2

"""
    klassHours [
        [list of lessons of klass] [sum of klass' hours] [sum of lessons] # for class A
        [list of lessons of klass] [sum of klass' hours] [sum of lessons] # for class B
        [list of lessons of klass] [sum of klass' hours] [sum of lessons] # for class C
    ]
"""
def getKlassHours(lessons):
    klassHours = [[[], 0, 0], [[], 0, 0], [[], 0, 0]]
    for key in lessons:
        year = getYear(lessons[key].classYear)
        klassHours[year][0].append(lessons[key])
        klassHours[year][1] = klassHours[year][1] + lessons[key].hours
        klassHours[year][2] = klassHours[year][2] + 1
    


