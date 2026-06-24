from sqlalchemy import (
    Table,
    Column,
    MetaData,
    Integer,
    String,
    Date,
    Numeric,
    select,
    func,
    bindparam,
    literal_column,
)


def generate_sql():
    metadata = MetaData()
    events = Table(
        "events", metadata,
        Column("user_id", Integer),
        Column("event_type", String),
        Column("event_day", Date),
        Column("amount", Numeric),
    )

    events_v2 = Table(
        "events_v2", metadata,
        Column("user_id", Integer),
        Column("event_type", String),
        Column("event_day", Date),
        Column("amount", Numeric),
    )

    event_metadata = Table(
        "event_metadata", metadata,
        Column("user_id", Integer),
        Column("event_type", String),
        Column("category", String),
    )

    base_data = (
        select(
            events.c.user_id,
            events.c.event_type,
            events.c.event_day,
            events.c.amount,
        )
        .where(
            events.c.event_day.between(
                literal_column("DATE '2023-01-01'"),
                literal_column("DATE '2025-01-01'")
            )
        ).union_all(
            select(
                events_v2.c.user_id,
                events_v2.c.event_type,
                events_v2.c.event_day,
                events_v2.c.amount,
            )
            .where(
                events_v2.c.event_day.between(
                    bindparam("p1"),
                    bindparam("p2")
                )
            )
        )
    ).cte("base_data")

    bd = base_data.alias("bd")
    stmt = (
        select(
            bd.c.user_id,
            bd.c.event_type,
            func.count().label("cnt_events"),
            func.sum(bd.c.amount).label("sum_amount"),
            func.min(bd.c.amount).label("min_amount"),
            func.max(bd.c.amount).label("max_amount"),
            func.min(bd.c.event_day).label("first_event_day"),
            func.max(bd.c.event_day).label("last_event_day"),
            event_metadata.c.category,
        )
        .select_from(
            bd.outerjoin(
                event_metadata,
                (bd.c.user_id == event_metadata.c.user_id)
                & (bd.c.event_type == event_metadata.c.event_type)
            )
        )
        .group_by(
            bd.c.user_id,
            bd.c.event_type,
            event_metadata.c.category,
        )
        .order_by(
            bd.c.event_type.desc(),
            bd.c.user_id,
        )
    )

    return str(stmt.compile())
