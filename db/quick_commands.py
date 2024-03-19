from sqlalchemy import func
from sqlalchemy import select

from data.config import async_session
from db.tables import *


async def add_student(name):
    async with async_session() as session:
        async with session.begin():
            student = Student(name=name)
            session.add(student)
        await session.commit()


async def top_students_by_average_mark(session, number_of_students: int):
    avg_marks = select(Student.name, func.avg(Mark.value).label('average_mark')) \
        .join(Mark, Mark.student_id == Student.id) \
        .group_by(Student.id) \
        .order_by(func.avg(Mark.value).desc()) \
        .limit(number_of_students)
    result = await session.execute(avg_marks)
    return result.fetchall()


async def top_student_in_discipline(session, discipline_id):
    avg_marks = select(Student.name, func.avg(Mark.value).label('average_mark')) \
        .join(Mark, Mark.student_id == Student.id) \
        .where(Mark.discipline_id == discipline_id) \
        .group_by(Student.id) \
        .order_by(func.avg(Mark.value).desc()) \
        .limit(1)
    result = await session.execute(avg_marks)
    return result.fetchone()


async def average_mark_in_groups_for_discipline(session, discipline_id):
    avg_marks = select(Group.name, func.avg(Mark.value).label('average_mark')) \
        .join(Student, Student.id == Group.student_id) \
        .join(Mark, Mark.student_id == Student.id) \
        .where(Mark.discipline_id == discipline_id) \
        .group_by(Group.id)
    result = await session.execute(avg_marks)
    return result.fetchall()


async def average_mark_across_all(session):
    avg_mark = select(func.avg(Mark.value).label('average_mark'))
    result = await session.execute(avg_mark)
    return result.fetchone()


async def courses_taught_by_teacher(session, teacher_id):
    courses = select(Discipline.name) \
        .where(Discipline.teacher_id == teacher_id)
    result = await session.execute(courses)
    return result.fetchall()


async def students_in_group(session, group_id):
    students = select(Student.name) \
        .join(Group, Group.student_id == Student.id) \
        .where(Group.id == group_id)
    result = await session.execute(students)
    return result.fetchall()


async def marks_in_group_for_discipline(session, group_id, discipline_id):
    marks = select(Student.name, Mark.value) \
        .join(Student, Student.id == Mark.student_id) \
        .join(Group, Group.student_id == Student.id) \
        .where(Mark.discipline_id == discipline_id, Group.id == group_id)
    result = await session.execute(marks)
    return result.fetchall()


async def average_mark_by_teacher(session, teacher_id):
    avg_mark = select(func.avg(Mark.value).label('average_mark')) \
        .join(Discipline, Discipline.id == Mark.discipline_id) \
        .where(Discipline.teacher_id == teacher_id)
    result = await session.execute(avg_mark)
    return result.scalar()


async def courses_attended_by_student(session, student_id):
    courses = select(Discipline.name) \
        .join(Mark, Mark.discipline_id == Discipline.id) \
        .where(Mark.student_id == student_id)
    result = await session.execute(courses)
    return result.fetchall()


async def courses_taught_to_student_by_teacher(session, student_id, teacher_id):
    courses = select(Discipline.name) \
        .join(Mark, Mark.discipline_id == Discipline.id) \
        .where(Mark.student_id == student_id, Discipline.teacher_id == teacher_id)
    result = await session.execute(courses)
    return result.fetchall()


async def average_mark_given_by_teacher_to_student(session, teacher_id, student_id):
    statement = select(func.avg(Mark.value).label('average_mark')) \
        .join(Discipline, Discipline.id == Mark.discipline_id) \
        .where(Discipline.teacher_id == teacher_id, Mark.student_id == student_id)
    result = await session.execute(statement)
    average_mark = result.scalar()
    return average_mark


async def last_marks_in_group_for_discipline(session, group_id, discipline_id):
    # Для прикладу, візьмемо останню дату оцінювання для конкретного предмета у групі
    subquery = select(func.max(Mark.created_at).label('last_mark_date')) \
        .join(Student, Student.id == Mark.student_id) \
        .where(Mark.discipline_id == discipline_id, Student.group_id == group_id) \
        .subquery()

    # Отримуємо оцінки на цю дату
    statement = select(Mark) \
        .join(subquery, Mark.created_at == subquery.c.last_mark_date) \
        .where(Mark.discipline_id == discipline_id, Student.group_id == group_id)

    result = await session.execute(statement)
    marks = result.scalars().all()
    return marks


async def add_teacher(name):
    async with async_session() as session:
        teacher = Teacher(name=name)
        session.add(teacher)
        await session.commit()


async def add_group(name, student):
    async with async_session() as session:
        group = Group(name=name, student=student)
        session.add(group)
        await session.commit()


async def add_discipline(name, teacher_id):
    async with async_session() as session:
        discipline = Discipline(name=name, teacher_id=teacher_id)
        session.add(discipline)
        await session.commit()


async def add_mark(name, discipline, student):
    async with async_session() as session:
        mark = Mark(name=name, discipline=discipline, student=student)
        session.add(mark)
        await session.commit()
