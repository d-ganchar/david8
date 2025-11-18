from david8.predicates import (
    between_c,
    eq,
    ge,
    gt,
    le,
    lt,
    ne,
)
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
                between_c('last_visit', '2023', '2024'),
            )
        )

        self.assertEqual(
            query.get_sql(),
            "SELECT * FROM cats WHERE color = %(p1)s AND age >= %(p2)s AND age <= %(p3)s AND weight > %(p4)s AND "
            "weight < %(p5)s AND gender != %(p6)s AND last_visit BETWEEN %(p7)s AND %(p8)s"
        )

        self.assertEqual(
            {
                'p1': 'ginger',
                'p2': 2,
                'p3': 3,
                'p4': 3.1,
                'p5': 3.9,
                'p6': 'f',
                'p7': '2023',
                'p8': '2024',
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
            between_c('last_visit', '2023-01-01', '2024-01-01'),
            between_c('sociality', 69, 96),
        ]:
            query.where(predicate)

        self.assertEqual(
            query.get_sql(),
            'SELECT * FROM cats WHERE color = %(p1)s AND age >= %(p2)s AND age <= %(p3)s AND weight > %(p4)s AND '
            'weight < %(p5)s AND gender != %(p6)s AND last_visit BETWEEN %(p7)s AND %(p8)s AND sociality '
            'BETWEEN %(p9)s AND %(p10)s'
        )

        self.assertEqual(
            {
                'p1': 'ginger',
                'p10': 96,
                'p2': 2,
                'p3': 3,
                'p4': 3.1,
                'p5': 3.9,
                'p6': 'f',
                'p7': '2023-01-01',
                'p8': '2024-01-01',
                'p9': 69,
            },
            query.get_parameters(),
        )
