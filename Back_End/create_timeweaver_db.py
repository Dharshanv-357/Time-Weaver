import asyncpg, asyncio
async def main():
    conn = await asyncpg.connect('postgresql://postgres:sotta357@localhost:5432/postgres')
    try:
        await conn.execute('CREATE DATABASE timeweaver_db')
        print('Created DB timeweaver_db')
    except Exception as e:
        print(e)
    finally:
        await conn.close()
asyncio.run(main())
