import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.future import select

from db.models import User, Event, Note, Setting, Screenshot

old_db_engine = create_async_engine("sqlite+aiosqlite:///database.db")
new_db_engine = create_async_engine("sqlite+aiosqlite:///database_new.db")

old_db_sessionmaker = async_sessionmaker(bind=old_db_engine, autoflush=False)
new_db_sessionmaker = async_sessionmaker(bind=new_db_engine, autoflush=False)

models = [User, Event, Note, Setting, Screenshot]


async def migrate_data(old_session, new_session, model):
    async with old_session() as old_db_session, new_session() as new_db_session:
        # Fetch all records from the old database for the current model
        old_records = await old_db_session.execute(select(model))

        # Iterate over old records and insert them into the new database
        for record in old_records.scalars():
            new_db_session.add(record)

        # Commit the changes to the new database
        await new_db_session.commit()


async def main():  # Loop through each model and migrate the data
    for model in models:
        await migrate_data(old_db_sessionmaker, new_db_sessionmaker, model)


if __name__ == '__main__':
    asyncio.run(main())
