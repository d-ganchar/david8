from parameterized import parameterized

from david8.expressions import col, val
from david8.predicates import (
    between,
    eq,
    ge,
    gt,
    le,
    lt,
    ne,
)
from david8.protocols.sql import PredicateProtocol
from tests.base_test import BaseTest


class TestWherePredicates(BaseTest):
    def test_where_val(self):
        query = (
            self.qb
            .select('*')
            .from_table('cats')
            .where(
                eq('color', 'ginger'),
                ge('age', 2),
                le('age', 3),
                gt('weight', 3.1),
                lt('weight', 3.9),
                ne('gender', 'f'),
            )
        )

        self.assertEqual(
            query.get_sql(),
            "SELECT * FROM cats WHERE color = %(p1)s AND age >= %(p2)s AND age <= %(p3)s AND weight > %(p4)s AND "
            "weight < %(p5)s AND gender != %(p6)s"
        )

        self.assertEqual(
            {
                'p1': 'ginger',
                'p2': 2,
                'p3': 3,
                'p4': 3.1,
                'p5': 3.9,
                'p6': 'f',
             },
            query.get_parameters()
        )

    def test_where_left_col_right_param_predicates(self):
        query = self.qb.select('*').from_table('cats')

        for predicate in [
            eq('color', 'ginger'),
            ge('age', 2),
            le('age', 3),
            gt('weight', 3.1),
            lt('weight', 3.9),
            ne('gender', 'f'),
        ]:
            query.where(predicate)

        self.assertEqual(
            query.get_sql(),
            'SELECT * FROM cats WHERE color = %(p1)s AND age >= %(p2)s AND age <= %(p3)s AND weight > %(p4)s AND '
            'weight < %(p5)s AND gender != %(p6)s'
        )

        self.assertEqual(
            {
                'p1': 'ginger',
                'p2': 2,
                'p3': 3,
                'p4': 3.1,
                'p5': 3.9,
                'p6': 'f',
            },
            query.get_parameters(),
        )

    @parameterized.expand([
        (
            between('last_visit', '2023-01-01', '2024-01-01'),
            'SELECT last_visit BETWEEN %(p1)s AND %(p2)s',
            {'p1': '2023-01-01', 'p2': '2024-01-01'},
        ),
        (
            between('sociality', 69, 96).as_('soc_level'),
            'SELECT sociality BETWEEN %(p1)s AND %(p2)s AS soc_level',
            {'p1': 69, 'p2': 96},
        ),
        (
            between('price', col('account_balance_free'), col('account_balance_total')),
            'SELECT price BETWEEN account_balance_free AND account_balance_total',
            {},
        ),
        (
            between('price', val(0.1), val(0.9)),
            'SELECT price BETWEEN 0.1 AND 0.9',
            {},
        )
    ])
    def test_between(self, b_expr: PredicateProtocol, exp_sql: str, exp_params: dict):
        query = self.qb.select(b_expr)
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)
