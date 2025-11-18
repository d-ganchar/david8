from pypika import Query, Table, functions as fn, Field, Order


def generate_sql():
    p = Table('products').as_('p')
    o = Table('orders').as_('o')
    c = Table('customers').as_('c')
    s = Table('shippers').as_('s')

    query = (
        Query.from_(p)
        .join(o).on(p.product_id == o.product_id)
        .left_join(c).on(o.customer_id == c.customer_id)
        .right_join(s).on(o.shipper_id == s.shipper_id)
        .select(
            p.product_name.as_('pn'),
            c.country.as_('cy'),
            s.shipper_name.as_('sn'),
            fn.Sum(o.order_quantity).as_('tqs'),
            fn.Min(o.order_date).as_('eod'),
            fn.Max(o.order_date).as_('lod')
        )
        .where(p.category == 'Beverages')
        .groupby(p.product_name, c.country, s.shipper_name)
        .orderby(Field('tqs'), order=Order.desc)
        .orderby(Field('pn'))
    )

    return str(query)
