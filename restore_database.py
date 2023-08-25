from sqlalchemy import create_engine, text

from config import DATABASE_NAME

sqlite_engine = create_engine(f'sqlite:///{DATABASE_NAME}.db')

with open('database_dump.sql', 'r', encoding='utf-8') as file:
    sql_script = file.read()

sql_commands = sql_script.split(';')

sql_commands = [cmd.strip() for cmd in sql_commands if cmd.strip()]

with sqlite_engine.connect() as conn:
    for sql_command in sql_commands:
        conn.execute(text(sql_command))
