
# TODO: Work out how to handle deaths.
# TODO: Create a function that shows a message to all players.
# TODO: Start timer and spawn positions.
# TODO: Game ending conditions.
# TODO: Player blink.
# TODO: Thread main loop to avoid waiting for server data.

import os
from client.client import GameClient


if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    client = GameClient()
    client.main()
