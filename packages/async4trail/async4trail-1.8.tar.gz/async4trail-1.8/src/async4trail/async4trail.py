import asyncio


async def main():
    print('🌽 hello')
    await asyncio.sleep(1)
    print('world 🍎')

if __name__ == "__main__":
    print('😈 Start')
    asyncio.run(main())
