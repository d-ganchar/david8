from pypika import Table, Query, functions as fn, Parameter, Order

def generate_sql():
    events = Table("events")
    events_v2 = Table("events_v2")
    event_metadata = Table("event_metadata")
    bd = Table("base_data")

    query = (
        Query
        .with_(
            (
                Query
                .from_(events)
                .select(
                    events.user_id,
                    events.event_type,
                    events.event_day,
                    events.amount,
                )
                .where(
                    events.event_day.between("2023-01-01", "2025-01-01")
                )
            ).union_all(
                Query
                .from_(events_v2)
                .select(
                    events_v2.user_id,
                    events_v2.event_type,
                    events_v2.event_day,
                    events_v2.amount,
                )
                .where(
                    events_v2.event_day.between(Parameter("%(p1)s"), Parameter("%(p2)s"))
                )
            ),
            "base_data"
        )
        .from_(bd)
        .left_join(event_metadata)
        .using(bd.user_id, bd.event_type)
        .select(
            bd.user_id,
            bd.event_type,
            fn.Count("*").as_("cnt_events"),
            fn.Sum(bd.amount).as_("sum_amount"),
            fn.Min(bd.amount).as_("min_amount"),
            fn.Max(bd.amount).as_("max_amount"),
            fn.Min(bd.event_day).as_("first_event_day"),
            fn.Max(bd.event_day).as_("last_event_day"),
            event_metadata.category,
        )
        .groupby(
            bd.user_id,
            bd.event_type,
            event_metadata.category,
        )
        .orderby(
            bd.event_type,
            order=Order.desc,
        )
        .orderby(
            bd.user_id
        )
    )

    return query.get_sql()
