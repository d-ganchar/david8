from david8 import get_qb
from david8.core.base_dialect import BaseDialect
from david8.expressions import col
from david8.functions import max_, min_, sum_
from david8.joins import left, inner, right
from david8.param_styles import PyFormatParamStyle
from david8.predicates import eq_c, eq


class _TestDialect(BaseDialect):
    def __init__(self):
        super().__init__(PyFormatParamStyle(), False)


def generate_sql():
    return (
        get_qb(_TestDialect())
        .select(
            col('p.product_name').as_('pn'),
            col('c.country').as_('cy'),
            col('s.shipper_name').as_('sn'),
            sum_('o.order_quantity').as_('tqs'),
            min_('o.order_date').as_('eod'),
            max_('o.order_date').as_('lod'),
        )
        .join(inner().table('orders').as_('o').on(eq_c('o.customer_id', 'o.product_id')))
        .join(left().table('customers').as_('c').on(eq_c('o.customer_id', 'c.customer_id')))
        .join(right().table('shippers').as_('s').on(eq_c('o.shipper_id', 's.shipper_id')))
        .where(eq('p.category', 'Beverages'))
        .group_by('p.product_name', 'c.country', 's.shipper_name')
        .order_by_desc('tqs')
        .order_by('pn')
    ).get_sql()
