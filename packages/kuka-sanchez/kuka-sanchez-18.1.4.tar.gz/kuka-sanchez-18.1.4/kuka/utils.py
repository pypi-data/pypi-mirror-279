from .curso import cursos

def total_duration():
    return sum(curso.duration for curso in cursos)

    