from ..protocols.sql import (
    AliasedProtocol as _AliasedProtocol,
)
from ..protocols.sql import (
    DeleteProtocol as _DeleteProtocol,
)
from ..protocols.sql import (
    ExprProtocol as _ExprProtocol,
)
from ..protocols.sql import (
    InsertProtocol as _InsertProtocol,
)
from ..protocols.sql import (
    JoinProtocol as _JoinProtocol,
)
from ..protocols.sql import (
    SelectProtocol as _SelectProtocol,
)
from ..protocols.sql import (
    Sql92JoinProtocol as _Sql92JoinProtocol,
)
from ..protocols.sql import (
    UpdateProtocol as _UpdateProtocol,
)

# TODO: breaking changes. remove when major release
JoinProtocol = _JoinProtocol
SelectProtocol = _SelectProtocol
Sql92JoinProtocol = _Sql92JoinProtocol
UpdateProtocol = _UpdateProtocol
InsertProtocol = _InsertProtocol
DeleteProtocol = _DeleteProtocol
AliasedProtocol = _AliasedProtocol
ExprProtocol = _ExprProtocol
