__tags__ = []

import sys
if 'pygame.mixer_music' not in sys.modules:
    __tags__.extend(('ignore', 'subprocess_ignore'))

