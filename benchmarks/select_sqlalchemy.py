from sqlalchemy import Table, Column, Integer, String, Date, MetaData, select, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.elements import literal_column
from sqlalchemy.sql.expression import desc


def generate_sql():
    metadata = MetaData()
    products_t = Table(
        'products',
        metadata,
        Column('product_id', Integer),
        Column('product_name', String),
        Column('category', String)
    )

    orders_t = Table(
        'orders',
        metadata,
        Column('order_id', Integer),
        Column('product_id', Integer),
        Column('customer_id', Integer),
        Column('shipper_id', Integer),
        Column('order_quantity', Integer),
        Column('order_date', Date)
    )

    customers_t = Table('customers', metadata, Column('customer_id', Integer), Column('country', String))
    shippers_t = Table('shippers', metadata, Column('shipper_id', Integer), Column('shipper_name', String))

    p = products_t.alias('p')
    o = orders_t.alias('o')
    c = customers_t.alias('c')
    s = shippers_t.alias('s')

    base_join = s.outerjoin(o, s.c.shipper_id == o.c.shipper_id)
    base_join = base_join.join(p, o.c.product_id == p.c.product_id)
    base_join = base_join.outerjoin(c, o.c.customer_id == c.c.customer_id)
    stmt = (
        select(
            p.c.product_name.label('pn'),
            c.c.country.label('cy'),
            s.c.shipper_name.label('sn'),
            func.sum(o.c.order_quantity).label('tqs'),
            func.min(o.c.order_date).label('eod'),
            func.max(o.c.order_date).label('lod')
        )
        .select_from(base_join)
        .where(p.c.category == 'Beverages')
        .group_by(p.c.product_name, c.c.country, s.c.shipper_name)
        .order_by(
            desc(literal_column('tqs')),
            literal_column('pn')
        )
    )

    return str(stmt.compile(dialect=postgresql.dialect()))
