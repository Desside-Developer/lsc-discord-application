import multiprocessing
import os


def run_bot(token):
    os.system(f"python {token}.py")


if __name__ == "__main__":
    bot_tokens = ['app\\bots\\bot_tickets', 'app\\bots\\bot_music', 'app\\bots\\bot_moderator']
    processes = []
    for token in bot_tokens:
        p = multiprocessing.Process(target=run_bot, args=(token,))
        processes.append(p)
        p.start()
    for process in processes:
        process.join()
