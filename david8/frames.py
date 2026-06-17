from .core.base_frames import CurrentRowBound as _CurrentRowBound
from .core.base_frames import FollowingBound as _FollowingBound
from .core.base_frames import PrecedingBound as _PrecedingBound
from .core.base_frames import RangeMode as _RangeMode
from .core.base_frames import RowsMode as _RowsMode
from .core.base_frames import UnboundedFollowingBound as _UnboundedFollowingBound
from .core.base_frames import UnboundedPrecedingBound as _UnboundedPrecedingBound
from .protocols.sql import FrameBoundProtocol, FrameModeProtocol


def rows(start: FrameBoundProtocol, end: FrameBoundProtocol = None) -> FrameModeProtocol:
    return _RowsMode(_start=start, _end=end, _name='ROWS')

def range_(start: FrameBoundProtocol, end: FrameBoundProtocol = None) -> FrameModeProtocol:
    return _RangeMode(_start=start, _end=end, _name='RANGE')

def current_row() -> FrameBoundProtocol:
    return _CurrentRowBound()

def following() -> FrameBoundProtocol:
    return _FollowingBound()

def preceding() -> FrameBoundProtocol:
    return _PrecedingBound()

def unbounded_preceding() -> FrameBoundProtocol:
    return _UnboundedPrecedingBound()

def unbounded_following() -> FrameBoundProtocol:
    return _UnboundedFollowingBound()
