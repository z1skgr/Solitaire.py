__tags__ = []

import sys
if 'pygame.mixer' not in sys.modules:
    __tags__.extend(('ignore', 'subprocess_ignore'))

