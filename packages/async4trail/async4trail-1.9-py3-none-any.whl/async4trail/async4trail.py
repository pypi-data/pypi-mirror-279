import asyncio


async def main():
    print('🌽 hello')
    await asyncio.sleep(1)
    print('world 🍎')


def run():
    print('😈 Start')
    asyncio.run(main())
