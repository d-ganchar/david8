from parameterized import parameterized

from david8.expressions import false, null, param, true, val
from david8.logical_operators import not_
from david8.predicates import (
    between,
    eq,
    eq_c,
    eq_e,
    ge,
    ge_c,
    ge_e,
    gt,
    gt_c,
    gt_e,
    is_,
    le,
    le_c,
    le_e,
    lt,
    lt_c,
    lt_e,
    ne,
    ne_c,
    ne_e,
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
            eq_e(val(1), param(1)),
            'SELECT 1 = %(p1)s',
            {'p1': 1}
        ),
        # ge_e
        (
            ge_e(val(1), param(1)),
            'SELECT 1 >= %(p1)s',
            {'p1': 1}
        ),
        # gt_e
        (
            gt_e(val(1), param(1)),
            'SELECT 1 > %(p1)s',
            {'p1': 1}
        ),
        # le_e
        (
            le_e(val(1), param(1)),
            'SELECT 1 <= %(p1)s',
            {'p1': 1}
        ),
        # lt_e
        (
            lt_e(val(1), param(1)),
            'SELECT 1 < %(p1)s',
            {'p1': 1}
        ),
        # le_e
        (
            le_e(val(1), param(1)),
            'SELECT 1 <= %(p1)s',
            {'p1': 1}
        ),
        # lt_e
        (
            lt_e(val(1), param(1)),
            'SELECT 1 < %(p1)s',
            {'p1': 1}
        ),
        # ne_e
        (
            ne_e(val(1), param(1)),
            'SELECT 1 != %(p1)s',
            {'p1': 1}
        ),
        # is
        (
            is_('is_active', true()),
            'SELECT is_active IS TRUE',
            {},
        ),
        (
            is_('is_active', not_(true())),
            'SELECT is_active IS NOT TRUE',
            {},
        ),
        (
            is_('is_active', false()),
            'SELECT is_active IS FALSE',
            {},
        ),
        (
            is_('is_active', not_(false())),
            'SELECT is_active IS NOT FALSE',
            {},
        ),
        (
            is_('is_active', null()),
            'SELECT is_active IS NULL',
            {},
        ),
        (
            is_('is_active', not_(null())),
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
    ])
    def test_predicate(self, predicate: PredicateProtocol, exp_sql: str, exp_params: dict) -> None:
        query = BaseTest.qb.select(predicate)
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)
