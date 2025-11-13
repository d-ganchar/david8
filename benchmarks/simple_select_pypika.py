from pypika import Field, Order, Table
from pypika import functions as fn


def generate_sql():
    orders = Table("orders")

    builder = (
        orders
        .select(
            orders.order_type,
            orders.seller_type,
            fn.Count(orders.order_type).as_("order_type_count"),
            fn.Sum(orders.total).as_("total_spent"),
            fn.Max(orders.created_at).as_("last_order"),
            fn.Min(orders.created_at).as_("first_order")
        )
        .where(orders.order_type != "canceled")
        .where(orders.seller_type != "unknown")
        .groupby(orders.order_type)
        .groupby(orders.seller_type)
        .having(fn.Sum(orders.total) > 1000)
        .orderby(orders.total, order=Order.desc)
    )

    builder = builder.orderby(Field("total_spent"), order=Order.desc)
    builder = builder.orderby(Field("order_type_count"), order=Order.desc)
    builder = builder.limit(100)
    return builder.get_sql()
