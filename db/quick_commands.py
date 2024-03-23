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


async def get_all_students():
    async with async_session() as session:
        async with async_session.begin():
            students = select(Student.name)
            result = await session.execute(students)
            names = [name[0] for name in result.fetchall()]
            return names


async def add_teacher(name):
    async with async_session() as session:
        teacher = Teacher(name=name)
        session.add(teacher)
        await session.commit()


async def get_all_teachers():
    async with async_session() as session:
        teachers = select(Teacher.name)
        result = await session.execute(teachers)
        names = [name[0] for name in result.fetchall()]
        return names


async def add_group(name, student):
    async with async_session() as session:
        group = Group(name=name, student=student)
        session.add(group)
        await session.commit()


async def get_all_groups():
    async with async_session() as session:
        groups = select(Group.name)
        result = await session.execute(groups)
        names = [name[0] for name in result.fetchall()]
        return names


async def add_discipline(name, teacher_id):
    async with async_session() as session:
        discipline = Discipline(name=name, teacher_id=teacher_id)
        session.add(discipline)
        await session.commit()


async def get_all_disciplines():
    async with async_session() as session:
        disciplines = select(Discipline.name)
        result = await session.execute(disciplines)
        names = [name[0] for name in result.fetchall()]
        return names


async def add_mark(name, discipline, student):
    async with async_session() as session:
        mark = Mark(name=name, discipline=discipline, student=student)
        session.add(mark)
        await session.commit()


async def get_all_marks():
    async with async_session() as session:
        marks = select(Mark.value)
        result = await session.execute(marks)
        values = [value[0] for value in result.fetchall()]
        return values


async def top_students_by_average_mark(number_of_students: int):
    async with async_session() as session:
        async with session.begin():
            avg_marks = select(Student.name, func.avg(Mark.value).label('average_mark')) \
                .join(Mark, Mark.student_id == Student.id) \
                .group_by(Student.id) \
                .order_by(func.avg(Mark.value).desc()) \
                .limit(number_of_students)
            result = await session.execute(avg_marks)
            return result.fetchall()


async def top_student_in_discipline(discipline_id):
    async with async_session() as session:
        async with session.begin():
            avg_marks = select(Student.name, func.avg(Mark.value).label('average_mark')) \
                .join(Mark, Mark.student_id == Student.id) \
                .where(Mark.discipline_id == discipline_id) \
                .group_by(Student.id) \
                .order_by(func.avg(Mark.value).desc()) \
                .limit(1)
            result = await session.execute(avg_marks)
            return result.fetchone()


async def average_mark_in_groups_for_discipline(discipline_id):
    async with async_session() as session:
        async with session.begin():
            avg_marks = select(Group.name, func.avg(Mark.value).label('average_mark')) \
                .join(Student, Student.id == Group.student_id) \
                .join(Mark, Mark.student_id == Student.id) \
                .where(Mark.discipline_id == discipline_id) \
                .group_by(Group.id)
            result = await session.execute(avg_marks)
            return result.fetchall()


async def average_mark_across_all():
    async with async_session() as session:
        async with session.begin():
            avg_mark = select(func.avg(Mark.value).label('average_mark'))
            result = await session.execute(avg_mark)
            return result.fetchone()


async def courses_taught_by_teacher(teacher_id):
    async with async_session() as session:
        async with session.begin():
            courses = select(Discipline.name) \
                .where(Discipline.teacher_id == teacher_id)
            result = await session.execute(courses)
            return result.fetchall()


async def students_in_group(group_id):
    async with async_session() as session:
        async with session.begin():
            students = select(Student.name) \
                .join(Group, Group.student_id == Student.id) \
                .where(Group.id == group_id)
            result = await session.execute(students)
            return result.fetchall()


async def marks_in_group_for_discipline(group_id, discipline_id):
    async with async_session() as session:
        async with session.begin():
            marks = select(Student.name, Mark.value) \
                .join(Student, Student.id == Mark.student_id) \
                .join(Group, Group.student_id == Student.id) \
                .where(Mark.discipline_id == discipline_id, Group.id == group_id)
            result = await session.execute(marks)
            return result.fetchall()


async def average_mark_by_teacher(teacher_id):
    async with async_session() as session:
        async with session.begin():
            avg_mark = select(func.avg(Mark.value).label('average_mark')) \
                .join(Discipline, Discipline.id == Mark.discipline_id) \
                .where(Discipline.teacher_id == teacher_id)
            result = await session.execute(avg_mark)
            return result.scalar()


async def courses_attended_by_student(student_id):
    async with async_session() as session:
        async with session.begin():
            courses = select(Discipline.name) \
                .join(Mark, Mark.discipline_id == Discipline.id) \
                .where(Mark.student_id == student_id)
            result = await session.execute(courses)
            return result.fetchall()


async def courses_taught_to_student_by_teacher(student_id, teacher_id):
    async with async_session() as session:
        async with session.begin():
            courses = select(Discipline.name) \
                .join(Mark, Mark.discipline_id == Discipline.id) \
                .where(Mark.student_id == student_id, Discipline.teacher_id == teacher_id)
            result = await session.execute(courses)
            return result.fetchall()


async def average_mark_given_by_teacher_to_student(teacher_id, student_id):
    async with async_session() as session:
        async with session.begin():
            statement = select(func.avg(Mark.value).label('average_mark')) \
                .join(Discipline, Discipline.id == Mark.discipline_id) \
                .where(Discipline.teacher_id == teacher_id, Mark.student_id == student_id)
            result = await session.execute(statement)
            average_mark = result.scalar()
            return average_mark


async def last_marks_in_group_for_discipline(group_id, discipline_id):
    async with async_session() as session:
        async with session.begin():
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
