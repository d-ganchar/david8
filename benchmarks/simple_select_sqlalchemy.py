from sqlalchemy import column, desc, func, select, table
from sqlalchemy.dialects import postgresql


def generate_sql():
    for _ in range(100):
        orders = table(
            "orders",
            column("order_type"),
            column("seller_type"),
            column("total"),
            column("created_at")
        )


        query = (
            select(
                orders.c.order_type,
                orders.c.seller_type,
                func.count(orders.c.order_type).label("order_type_count"),
                func.sum(orders.c.total).label("total_spent"),
                func.max(orders.c.created_at).label("last_order"),
                func.min(orders.c.created_at).label("first_order"),
            )
            .where(orders.c.order_type != "canceled")
            .where(orders.c.seller_type != "unknown")
            .group_by(orders.c.order_type)
            .group_by(orders.c.seller_type)
            .having(func.sum(orders.c.total) > 1000)
            .order_by(desc("total_spent"), desc("order_type_count"))
            .limit(100)
        )

        result = query.compile(dialect=postgresql.dialect())
