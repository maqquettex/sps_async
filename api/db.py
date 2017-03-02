import re
import sqlalchemy as sa
from sqlalchemy import select, insert
from sqlalchemy.schema import CreateTable

from asyncpgsa import pg


meta = sa.MetaData()

artist = sa.Table(
    'artist', meta,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('name', sa.String(200), nullable=False),

)

song = sa.Table(
    'song', meta,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('artist_id', sa.ForeignKey('artist.id'), nullable=False),
    sa.Column('title', sa.String(200), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),

)


async def create_tables_sql(pool, tables):
    async with pg.transaction() as conn:
        for name, table in tables.items():
            create_sql = re.sub(
                r"CREATE TABLE",
                'CREATE TABLE IF NOT EXISTS',
                str(CreateTable(table))
            ) + ';'
            create_sql = re.sub(
                r'id INTEGER',
                'id SERIAL',
                create_sql
            )
            await conn.execute(create_sql)


async def get_all_songs():
    query = select([song.c.title.label('song_name'), artist.c.name.label('artist')]).select_from(
        song.outerjoin(artist)
    )

    return query

async def get_all_artists():
    query = select([artist.c.id, artist.c.name]).select_from(artist)
    return query
