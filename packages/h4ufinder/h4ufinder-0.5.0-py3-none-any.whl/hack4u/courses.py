class Course:
    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link

    def __repr__(self): # se hace ya en la instancia asi, no como __str__ que tambien funciona pero no en la instancia
        # si probas el print(lista de objetos) funciona de una, con el str a cada objeto con un for
        return f"{self.name} [duracion: {self.duration} horas] link: {self.link}"


courses = [
    Course("Introducción a Linux", 15,"https://hack4u.io/cursos/introduccion-a-linux/"),
    Course("Personalización de Linux",3,"https://hack4u.io/personalizacion-de-entorno-en-linux/"),
    Course("Python Ofensivo", 35,"https://hack4u.io/cursos/python-ofensivo/"),
    Course("Introducción al Hacking", 53,"https://hack4u.io/cursos/introduccion-al-hacking/")
]

# print(courses[1]) ahora si queda como un iterable posicionado

def list_courses():
    for course in courses:
        print(course)

def search_course_by_name(name):
    for course in courses:
        if course.name == name:
            return course
    return None

