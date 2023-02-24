from log2d import Log

from button_bot import bot
log = Log("main").logger

def main():
    """
    main entry point of rotten Reversi bot
    """
    
    
    log.info("starting main() entry point")
    bot.run_echo_bot()
    log.info("leaving main()")

  


if __name__ == "__main__":
    main()
    

    
    