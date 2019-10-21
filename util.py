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
        [sum of klass' hours] [sum of lessons] # for class A
        [sum of klass' hours] [sum of lessons] # for class B
        [sum of klass' hours] [sum of lessons] # for class C
    ]
"""
def getKlassHours(lessons):
    klassHours = [[0, 0], [0, 0], [0, 0]]
    for key in lessons:
        year = getYear(lessons[key].classYear)
        klassHours[year][0] = klassHours[year][0] + lessons[key].hours
        klassHours[year][1] = klassHours[year][1] + 1
    

    print("Klass A: ", klassHours[0])
    print("Klass B: ",klassHours[1])
    print("Klass C: ",klassHours[2])


