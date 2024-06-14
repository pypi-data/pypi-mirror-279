from asyncio import Future
from dataclasses import dataclass
from typing import Callable

import techgram

from .identifier import Identifier
from .listenerTypes import ListenerTypes


@dataclass
class Listener:
    listener_type: ListenerTypes
    filters: "techgram.filters.Filter"
    unallowed_click_alert: bool
    identifier: Identifier
    future: Future = None
    callback: Callable = None