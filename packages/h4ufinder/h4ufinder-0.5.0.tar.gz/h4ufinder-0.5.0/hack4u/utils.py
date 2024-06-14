from .courses import courses 

def total_duration():
    duration = 0
    for course in courses:
        duration += course.duration
    return duration

# def total_duration():
#   return sum(course.duration for course in courses)
