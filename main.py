import asyncio
import logging

from button_bot import bot

async def main():
    
    # logging.basicConfig(
    #     level=logging.ERROR,
    #     format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    #     filename=".log"
    #     )
    
    await bot.run_echo_bot()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    
    