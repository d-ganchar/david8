from david8 import get_qb
from david8.agg_functions import count, max_, min_, sum_
from david8.dialects import PostgresDialect
from david8.predicates import gt, ne


def generate_sql():
    return (
        get_qb(PostgresDialect())
        .select(
            'order_type',
            'seller_type',
            count('order_type').as_('order_type_count'),
            sum_('total').as_('total_spent'),
            max_('created_at').as_('last_order'),
            min_('created_at').as_('last_order'),
        )
        .from_table('orders')
        .where(ne('order_type', 'canceled'), ne('seller_type', 'unknown'))
        .group_by('order_type', 'seller_type')
        .having(gt(sum_('total_spent'), 1000))
        .order_by_desc('total_spent', 'order_type_countC')
        .limit(100)
    ).get_sql()


generate_sql()
