from david8.predicates import (
    between,
    between_val,
    col_is_null,
    col_like,
    eq,
    eq_val,
    ge,
    ge_val,
    gt,
    gt_val,
    le,
    le_val,
    lt,
    lt_val,
    ne,
    ne_val,
)
from tests.base_test import BaseTest


class TestWherePredicates(BaseTest):
    def test_where_val(self):
        query = (
            self.qb
            .select('*')
            .from_table('cats')
            .where(
                eq_val('color', 'ginger'),
                ge_val('age', 2),
                le_val('age', 3),
                gt_val('weight', 3.1),
                lt_val('weight', 3.9),
                ne_val('gender', 'f'),
                between_val('last_visit', '2023', '2024'),
            )
        )

        for predicate in [
            col_is_null('owner'),
            col_is_null('illness', False),
            col_like('description', '%hugs%')
        ]:
            query.where(predicate)

        self.assertEqual(
            query.get_sql(),
            "SELECT * FROM cats WHERE color = %(p1)s AND age >= %(p2)s AND age <= %(p3)s AND weight > %(p4)s AND "
            "weight < %(p5)s AND gender != %(p6)s AND last_visit BETWEEN %(p7)s AND %(p8)s AND owner IS NULL AND "
            "illness IS NOT NULL AND description LIKE '%hugs%'"
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

    def test_where_static(self):
        query = self.qb.select('*').from_table('cats')

        for predicate in [
            eq('color', 'ginger'),
            ge('age', 2),
            le('age', 3),
            gt('weight', 3.1),
            lt('weight', 3.9),
            ne('gender', 'f'),
            between('last_visit', '2023-01-01', '2024-01-01'),
            between('sociality', 69, 96),
        ]:
            query.where(predicate)

        self.assertEqual(
            query.get_sql(),
            "SELECT * FROM cats WHERE color = 'ginger' AND age >= 2 AND age <= 3 AND weight > 3.1 AND weight < 3.9 "
            "AND gender != 'f' AND last_visit BETWEEN '2023-01-01' AND '2024-01-01' AND sociality BETWEEN 69 AND 96"
        )

        self.assertEqual({}, query.get_parameters())
