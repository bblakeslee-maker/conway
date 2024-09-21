import argparse
import pathlib
import signal
import types

import conway

halt_flag = False


def interrupt_handler(signum: int, frame: types.FrameType):
    global halt_flag
    halt_flag = not halt_flag


def main(config_path: pathlib.Path):
    try:
        game = conway.Conway(config_path)
        while True:
            print(game)
            game.update_grid()
            if halt_flag:
                return
    except ValueError as ve:
        print(ve)


if __name__ == '__main__':
    g_parser = argparse.ArgumentParser()
    g_parser.add_argument('--config', type=pathlib.Path, required=True,
                          help='Path to game config file.')
    g_args = g_parser.parse_args()
    signal.signal(signal.SIGINT, interrupt_handler)
    main(g_args.config)
