from environs import Env
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

env = Env()
env.read_env()

PGUSER = env.str("DB_USER")
PGPASS = env.str("DB_PASS")
PGNAME = env.str("DB_NAME")
PGHOST = env.str("DB_HOST")
PGPORT = env.str("DB_PORT")
DATABASE = env.str("DATABASE")

POSTGRES_URI = f"postgresql+asyncpg://{PGUSER}:{PGPASS}@{PGHOST}:{PGPORT}/{PGNAME}"

engine = create_async_engine(
    POSTGRES_URI
)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
