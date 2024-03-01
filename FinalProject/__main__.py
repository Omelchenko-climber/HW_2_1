from Bot import Bot
from View import ConsoleView


def run_bot():
    console = ConsoleView()
    console.get_greeting()
    bot = Bot()
    bot.book.load("auto_save")
    while True:
        action = console.get_user_input('Type help for list of commands or enter your command\n')
        if action == 'help':
            console.get_menu()
        else:
            bot.handle(action)
            if action in ['add', 'remove', 'edit']:
                bot.book.save("auto_save")
        if action == 'exit':
            console.exit()
            break


if __name__ == "__main__":
    run_bot()