import asyncio
import random

import db.quick_commands as qc
import seed as seed
from data.config import async_session


# from sqlalchemy.ext.asyncio import AsyncSession
# from myapp.models import Student, Group, Teacher, Discipline, Mark  # Імпортуйте ваші моделі


async def commands():
    session = async_session
    # print("Введіть номер")
    user_input = input("Введіть номер")
    try:
        command, *args = user_input.split()
    except ValueError:
        print("Give me the correct command please.")
        command = None
        pass

    if command is None:
        pass
    elif command.lower() == "1":
        print(await qc.add_student(args))
    elif command.lower() == "2":
        print(int(args[0]))
        print(await qc.top_students_by_average_mark(int(args[0])))
        # res = await top_students_by_average_mark(session, int(args))
    # print(res)
    elif command.lower() == "3":
        print(await qc.top_student_in_discipline(int(args[0])))
    elif command.lower() == "4":
        print(await qc.get_all_students())

    elif command.lower() == "5":
        names = await qc.get_all_marks()
        length = len(names)
        print(length)
        get_rand_student = names[random.randint(0, length)]
        print(get_rand_student)


async def main():
    await seed.seed_db()
    while True:
        await commands()


if __name__ == "__main__":
    asyncio.run(main())
