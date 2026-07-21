A `Source` is a `Python class` that represents a database table (or view). Each field maps to a column, and 
`_david8_source` sets the name (with an optional `_david8_db` for the database name). Define a source once, then 
reuse it across queries - with optional aliasing via `.as_('alias')` for joins and multi-table queries.

```python
from dataclasses import dataclass

from david8.functions import concat
from david8.expressions import Source, field_ as f, val as v
from david8.predicates import eq
from david8.joins import inner
from david8.protocols.sql import AliasedProtocol as Aliased


@dataclass(slots=True)
class UsersTable(Source):
    _david8_source   = 'users'      # table name or view name
    # _david8_db     = 'analytics'  # database name

    # property_name  = f(DATABASE_COLUMN_NAME)
    id: Aliased      = f('id')
    name: Aliased    = f('name')
    country: Aliased = f('country')


@dataclass(slots=True)
class OrdersTable(Source):
    _david8_source            = 'orders'
    
    id: Aliased               = f('id')
    user_id: Aliased          = f('user_id')
    product_id: Aliased       = f('product_id')
    billing_address: Aliased  = f('billing_address')
    shipping_address: Aliased = f('shipping_address')


@dataclass(slots=True)
class ProductsTable(Source):
    _david8_source = 'products'

    id: Aliased    = f('id')
    title: Aliased = f('title')


u = UsersTable()
query = (
    qb
    .select(u.name, u.country)
    .from_source(u)
    .where(eq(u.country, 'PL'))
)

query.get_sql()
# SELECT name, country FROM users WHERE country = %(p1)s
# {'p1': 'PL'}


u = UsersTable().as_('u')
o = OrdersTable().as_('o')
p = ProductsTable().as_('p')

query = (
    qb
    .select(
        u.name.as_('username'),
        o.id.as_('order_id'),
        p.title.as_('product_name'),
        concat(o.billing_address, v('|'), o.shipping_address).as_('addresses'),
    )
    .from_source(u)
    .join(
        inner().source(o).on(eq(o.user_id, u.id)),
        inner().source(p).on(eq(p.id, o.product_id)),
    )
    .where(eq(u.country, 'PL'))
)

query.get_sql()
# SELECT u.name AS username,
#        o.id AS order_id,
#        p.title AS product_name,
#        concat(o.billing_address, '|', o.shipping_address) AS addresses
#   FROM users AS u
#  INNER JOIN orders AS o ON (o.user_id = u.id)
#  INNER JOIN products AS p ON (p.id = o.product_id)
#  WHERE u.country = %(p1)s
# {'p1': 'PL'}
```