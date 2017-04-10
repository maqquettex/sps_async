"""
Here connections to databases (SQL and NoSQL) are created
Functions defined here should take care of:
 * configuring connection 
 * creating connection 
 * gracefully closing connections
"""
import os
import aioredis
import asyncpgsa



async def init_redis(app):
    # Configuring
    conf = (
        'redis',  # Host
        6379      # Port
    )

    # Creating pool
    redis = await aioredis.create_connection(conf)

    # Grateful shutdown
    async def close_redis():
        redis.close()
    app.on_cleanup.append(close_redis)


async def init_postgres(app):
    # Configuring
    conf = {
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'port': os.getenv('POSTGRES_PORT'),
        'database': os.getenv('POSTGRES_DB'),
        'host': os.getenv('postgres'),
    }

    # Creating pool
    app['pool'] = await asyncpgsa.create_pool(**conf)

    # Grateful shutdown
    app.on_cleanup.append(app['pool'].close)
