from parameterized import parameterized

from david8.expressions import param, val
from david8.functions import lower
from david8.predicates import (
    between,
    eq,
    eq_c,
    ge,
    ge_c,
    gt,
    gt_c,
    in_,
    is_,
    is_false,
    is_not_false,
    is_not_null,
    is_not_true,
    is_null,
    is_true,
    le,
    le_c,
    lt,
    lt_c,
    ne,
    ne_c,
)
from david8.protocols.sql import PredicateProtocol
from tests.base_test import BaseTest


class TestPredicates(BaseTest):
    @parameterized.expand([
        # between
        (
            between('age', 14, 18).as_('is_valid'),
            'SELECT age BETWEEN %(p1)s AND %(p2)s AS is_valid',
            {'p1': 14, 'p2': 18}
        ),
        (
            between('created_day', val('2025-01-01'), val('2026-01-01')),
            "SELECT created_day BETWEEN '2025-01-01' AND '2026-01-01'",
            {}
        ),
        # eq
        (
            eq('color', 'orange'),
            'SELECT color = %(p1)s',
            {'p1': 'orange'}
        ),
        (
            eq('beer', 0.5).as_('size'),
            'SELECT beer = %(p1)s AS size',
            {'p1': 0.5}
        ),
        (
            eq('age', 27).as_('is_valid'),
            'SELECT age = %(p1)s AS is_valid',
            {'p1': 27}
        ),
        (
            eq('status', val('active')),
            "SELECT status = 'active'",
            {}
        ),
        # ge
        (
            ge('beer', 0.5).as_('size'),
            'SELECT beer >= %(p1)s AS size',
            {'p1': 0.5}
        ),
        (
            ge('age', 27).as_('is_valid'),
            'SELECT age >= %(p1)s AS is_valid',
            {'p1': 27}
        ),
        # gt
        (
            gt('beer', 0.5).as_('size'),
            'SELECT beer > %(p1)s AS size',
            {'p1': 0.5}
        ),
        (
            gt('age', 27).as_('is_valid'),
            'SELECT age > %(p1)s AS is_valid',
            {'p1': 27}
        ),
        # le
        (
            le('beer', 0.5).as_('size'),
            'SELECT beer <= %(p1)s AS size',
            {'p1': 0.5}
        ),
        (
            le('age', 27).as_('is_valid'),
            'SELECT age <= %(p1)s AS is_valid',
            {'p1': 27}
        ),
        # lt
        (
            lt('beer', 0.5).as_('size'),
            'SELECT beer < %(p1)s AS size',
            {'p1': 0.5}
        ),
        (
            lt('age', 27).as_('is_valid'),
            'SELECT age < %(p1)s AS is_valid',
            {'p1': 27}
        ),
        # ne
        (
            ne('beer', 0.5).as_('size'),
            'SELECT beer != %(p1)s AS size',
            {'p1': 0.5}
        ),
        (
            ne('age', 27).as_('is_valid'),
            'SELECT age != %(p1)s AS is_valid',
            {'p1': 27}
        ),
        # eq_c
        (
            eq_c('billing', 'shipping').as_('is_the_same'),
            'SELECT billing = shipping AS is_the_same',
            {}
        ),
        # ge_c
        (
            ge_c('created', 'last_active'),
            'SELECT created >= last_active',
            {}
        ),
        # gt_c
        (
            gt_c('created', 'last_active'),
            'SELECT created > last_active',
            {}
        ),
        # le_c
        (
            le_c('created', 'last_active'),
            'SELECT created <= last_active',
            {}
        ),
        # lt_c
        (
            lt_c('created', 'last_active'),
            'SELECT created < last_active',
            {}
        ),
        # ne_c
        (
            ne_c('created', 'last_active'),
            'SELECT created != last_active',
            {}
        ),
        # eq_e
        (
            eq(val(1), param(1)),
            'SELECT 1 = %(p1)s',
            {'p1': 1}
        ),
        # ge_e
        (
            ge(val(1), param(1)),
            'SELECT 1 >= %(p1)s',
            {'p1': 1}
        ),
        # gt_e
        (
            gt(val(1), param(1)),
            'SELECT 1 > %(p1)s',
            {'p1': 1}
        ),
        # le_e
        (
            le(val(1), param(1)),
            'SELECT 1 <= %(p1)s',
            {'p1': 1}
        ),
        # lt_e
        (
            lt(val(1), param(1)),
            'SELECT 1 < %(p1)s',
            {'p1': 1}
        ),
        # le_e
        (
            le(val(1), param(1)),
            'SELECT 1 <= %(p1)s',
            {'p1': 1}
        ),
        # lt_e
        (
            lt(val(1), param(1)),
            'SELECT 1 < %(p1)s',
            {'p1': 1}
        ),
        # ne_e
        (
            ne(val(1), param(1)),
            'SELECT 1 != %(p1)s',
            {'p1': 1}
        ),
        # is
        (
            is_true('is_active'),
            'SELECT is_active IS TRUE',
            {},
        ),
        (
            is_not_true('is_active'),
            'SELECT is_active IS NOT TRUE',
            {},
        ),
        (
            is_false('is_active'),
            'SELECT is_active IS FALSE',
            {},
        ),
        (
            is_not_false('is_active'),
            'SELECT is_active IS NOT FALSE',
            {},
        ),
        (
            is_null('is_active'),
            'SELECT is_active IS NULL',
            {},
        ),
        (
            is_not_null('is_active'),
            'SELECT is_active IS NOT NULL',
            {},
        ),
        (
            is_('last_update_dt', 'last_login_dt'),
            'SELECT last_update_dt IS last_login_dt',
            {}
        ),
        (
            is_('last_update_dt', param(1)),
            'SELECT last_update_dt IS %(p1)s',
            {'p1': 1}
        ),
        (
            in_('status', [1, 2, 3]),
            'SELECT status IN (1, 2, 3)',
            {}
        ),
        (
            in_('status', [1, 2, 3], True),
            'SELECT status IN (%(p1)s, %(p2)s, %(p3)s)',
            {'p1': 1, 'p2': 2, 'p3': 3},
        ),
        (
            in_('status', ['closed', 'cancelled']),
            "SELECT status IN ('closed', 'cancelled')",
            {}
        ),
        (
            in_('status', ['closed', 'cancelled'], True),
            'SELECT status IN (%(p1)s, %(p2)s)',
            {'p1': 'closed', 'p2': 'cancelled'},
        ),
        (
            in_('status', [lower('old_status'), lower('new_status'), lower(val('NewValue'))]),
            "SELECT status IN (lower(old_status), lower(new_status), lower('NewValue'))",
            {},
        ),
        (
            in_('status', [lower('old_status'), lower('new_status'), lower(param('NewValue'))]),
            'SELECT status IN (lower(old_status), lower(new_status), lower(%(p1)s))',
            {'p1': 'NewValue'},
        ),
        (
            in_('status', BaseTest.qb.select('name').from_table('statuses')),
            'SELECT status IN (SELECT name FROM statuses)',
            {},
        ),
    ])
    def test_predicate(self, predicate: PredicateProtocol, exp_sql: str, exp_params: dict) -> None:
        query = BaseTest.qb.select(predicate)
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)
