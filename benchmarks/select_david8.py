from david8 import get_default_qb
from david8.expressions import val
from david8.functions import max_, min_, sum_, count
from david8.joins import left
from david8.predicates import between

def generate_sql():
    qb = get_default_qb()

    return (
        qb
        .with_(
            (
                'base_data',
                (
                    qb
                    .select('user_id', 'event_type', 'event_day', 'amount')
                    .from_table('events')
                    .where(
                        between('event_day', val('2023-01-01'), val('2025-01-01'))
                    )
                    .union(
                        qb
                        .select('user_id', 'event_type', 'event_day', 'amount')
                        .from_table('events_v2')
                        .where(
                            between('event_day', '2025-02-02', '2025-09-09')
                        )
                    )
                )
            )
        )
        .select(
            'bd.user_id',
            'bd.event_type',
            'm.category',
            count('*').as_('cnt_events'),
            sum_('bd.amount').as_('sum_amount'),
            min_('bd.amount').as_('min_amount'),
            max_('bd.amount').as_('max_amount'),
            min_('bd.event_day').as_('first_event_day'),
            max_('bd.event_day').as_('last_event_day'),
        )
        .from_table('base_data', alias='bd')
        .join(
            left()
            .table('event_metadata')
            .as_('m')
            .using('user_id', 'event_type')
        )
        .group_by('bd.user_id', 'bd.event_type', 'm.category')
        .order_by_desc('bd.event_type')
        .order_by('bd.user_id')
    ).get_sql()
