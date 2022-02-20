from typing import Any

import pygame.bufferproxy
import pygame.color

Color = pygame.color.Color
BufferProxy = pygame.bufferproxy.BufferProxy

def __getattr__(name) -> Any: ...  # don't error on missing stubs
