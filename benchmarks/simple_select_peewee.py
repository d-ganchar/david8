from peewee import Table, fn


def generate_sql():
    orders = Table('orders')

    order_type_count = fn.COUNT(orders.c.order_type).alias('order_type_count')
    total_spent = fn.SUM(orders.c.total).alias('total_spent')
    last_order = fn.MAX(orders.c.created_at).alias('last_order')
    first_order = fn.MIN(orders.c.created_at).alias('first_order')

    query, _ = (
        orders
        .select(
            orders.c.order_type,
            orders.c.seller_type,
            order_type_count,
            total_spent,
            last_order,
            first_order,
        )
        .where(orders.c.order_type != 'canceled')
        .where(orders.c.seller_type != 'unknown')
        .group_by(orders.c.order_type)
        .group_by(orders.c.seller_type)
        .having(total_spent > 1000)
        .order_by(total_spent.desc(), order_type_count.desc())
        .limit(100)
    ).sql()

    return query
