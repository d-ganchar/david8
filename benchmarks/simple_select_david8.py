from david8 import get_qb
from david8.agg_functions import count, max_, min_, sum_
from david8.dialects import PostgresDialect
from david8.expressions import as_
from david8.predicates import gt, ne


def generate_sql():
    return (
        get_qb(PostgresDialect())
        .select(
            'order_type',
            'seller_type',
            as_(count('order_type'), 'order_type_count'),
            as_(sum_('total'), 'total_spent'),
            as_(max_('created_at'), 'last_order'),
            as_(min_('created_at'), 'first_order'),
        )
        .from_table('orders')
        .where(ne('order_type', 'canceled'), ne('seller_type', 'unknown'))
        .group_by('order_type', 'seller_type')
        .having(gt(sum_('total_spent'), 1000))
        .order_by_desc('total_spent', 'order_type_countC')
        .limit(100)
    ).get_sql()


generate_sql()
