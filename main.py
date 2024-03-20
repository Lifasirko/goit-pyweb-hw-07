import asyncio
from faker import Faker
from faker.generator import random
# from sqlalchemy.ext.asyncio import AsyncSession
# from myapp.models import Student, Group, Teacher, Discipline, Mark  # Імпортуйте ваші моделі

from data.config import async_session, engine
from db.tables import Group, Teacher, Discipline, Student, Mark, Base

faker = Faker()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def create_groups():
    async with async_session() as session:
        async with session.begin():
            # Створіть та додайте групи
            groups = [Group(name=faker.word()) for _ in range(3)]
            session.add_all(groups)
        await session.commit()


async def create_teacher():
    async with async_session() as session:
        async with session.begin():
            teachers = [Teacher(name=faker.name()) for _ in range(3)]
            session.add_all(teachers)
        await session.commit()


async def create_disciplines():
    async with async_session() as session:
        async with session.begin():
            disciplines = [Discipline(name=faker.word(), teacher_id=random.randint(1, 3)) for _ in range(8)]
            session.add_all(disciplines)
        await session.commit()


async def create_students():
    async with async_session() as session:
        async with session.begin():
            students = [Student(name=faker.name(), group_id=random.randint(1, 3)) for _ in
                        range(50)]
            session.add_all(students)
        await session.commit()


async def create_marks():
    async with async_session() as session:
        async with session.begin():
            for student_id in range(1, 51):
                for _ in range(20):
                    marks = [Mark(value=faker.random_int(min=1, max=10), student_id=student_id,
                                  discipline_id=random.randint(1, 8))]
                    session.add_all(marks)
        await session.commit()


async def seed_db():
    await create_tables()
    await create_groups()
    await create_teacher()
    await create_disciplines()
    await create_students()
    await create_marks()
    # async with async_session() as session:
    # async with session.begin():
    #     # Створіть та додайте групи
    #     groups = [Group(name=faker.word()) for _ in range(3)]
    #     session.add_all(groups)
    #
    #
    #     # Створіть та додайте викладачів
    #     teachers = [Teacher(name=faker.name()) for _ in range(4)]
    #     session.add_all(teachers)
    #
    #     # Створіть та додайте предмети
    #     disciplines = [Discipline(name=faker.word(), teacher_id=random.randint(1, 3)) for teacher in teachers for _ in
    #                    range(8)]
    #     session.add_all(disciplines)
    #
    #     # Створіть та додайте студентів
    #     students = [Student(name=faker.name(), group_id=random.randint(0, 3)) for group in groups for _ in
    #                 range(50)]
    #     session.add_all(students)
    #
    #     # Додайте оцінки студентам
    #     marks = [Mark(value=faker.random_int(min=1, max=10), student_id=random.randint(0, 50), discipline_id=random.randint(0, 8)) for
    #              student in students for discipline in disciplines for _ in range(random.randint(1, 20))]
    #     session.add_all(marks)

    # await session.commit()


if __name__ == "__main__":
    asyncio.run(seed_db())
