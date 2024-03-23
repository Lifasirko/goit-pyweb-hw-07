import argparse
import asyncio
import db.quick_commands as qc


async def handle_create(args):
    print(args.name)
    await qc.add_teacher(args.name)


async def handle_list(args):
    print(await qc.list_teachers())


async def handle_update(args):
    await update_teacher(args.id, args.name)


async def handle_remove(args):
    await remove_teacher(args.id)


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Manage database records.")
#     parser.add_argument("-a", "--action", choices=["create", "list", "update", "remove"], required=True)
#     parser.add_argument("-m", "--model", choices=["Teacher", "Student", "Group", "Discipline", "Mark"], required=True)
#     parser.add_argument("-n", help="Name of the teacher")
#     parser.add_argument("--id", help="ID of the teacher", type=int)
#
#     args = parser.parse_args()
#
#     loop = asyncio.get_event_loop()
#
#     if args.action == "create":
#         loop.run_until_complete(handle_create(args))
#     elif args.action == "list":
#         loop.run_until_complete(handle_list(args))
#     elif args.action == "update":
#         loop.run_until_complete(handle_update(args))
#     elif args.action == "remove":
#         loop.run_until_complete(handle_remove(args))

async def main(args):
    if args.model == "Teacher":
        if args.action == "create":
            await qc.add_teacher(args.name)
        elif args.action == "list":
            print(await qc.get_all_teachers())
        elif args.action == "update":
            await update_teacher(args.id, args.name)
        elif args.action == "remove":
            await remove_teacher(args.id)
    # Add more conditions for other models here

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage database records.")
    parser.add_argument("-a", "--action", choices=["create", "list", "update", "remove"], required=True, help="Action to perform.")
    parser.add_argument("-m", "--model", choices=["Teacher", "Student", "Group", "Discipline", "Mark"], required=True, help="Model on which to perform the action.")
    parser.add_argument("-n", "--name", help="Name of the entity, used with create and update actions.")
    parser.add_argument("--id", type=int, help="ID of the entity, used with update and remove actions.")

    args = parser.parse_args()

    asyncio.run(main(args))


# py cli.py -a create -m Teacher -n 'Boris Jonson'
