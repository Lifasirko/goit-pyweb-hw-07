from environs import Env
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

env = Env()
env.read_env()


PGUSER = env.str("DB_USER")
PGPASS = env.str("DB_PASS")
PGNAME = env.str("DB_NAME")
PGHOST = env.str("DB_HOST")
PGPORT = env.str("DB_PORT")
DATABASE = env.str("DATABASE")


engine = create_async_engine(
    f"postgresql://{PGUSER}:{PGPASS}@{PGHOST}:{PGPORT}/{PGNAME}",
    connect_args={'client_encoding': 'utf8'}
)
async_session = async_sessionmaker(engine, expire_on_commit=False)

conn = await engine.connect()

POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASS}@{PGHOST}:{PGPORT}/{PGNAME}"
