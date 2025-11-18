from david8.logical_operators import and_, or_, xor
from david8.predicates import eq
from tests.base_test import BaseTest


class TestLogicalOperators(BaseTest):
    def test_or(self):
        query = (
            self.qb
            .select('*')
            .from_table('logical_operators')
            .where(
                or_(
                    eq('col1', 1),
                    eq('col1', 2),
                    xor(
                        eq('col2', 3),
                        eq('col2', 4),
                    ),
                ),
                eq('col3', 5),
            )
         )

        self.assertEqual(
            query.get_sql(),
            'SELECT * FROM logical_operators WHERE (col1 = %(p1)s OR col1 = %(p2)s OR (col2 = %(p3)s '
            'XOR col2 = %(p4)s)) AND col3 = %(p5)s'
        )

        self.assertEqual(query.get_parameters(), {'p1': 1, 'p2': 2, 'p3': 3, 'p4': 4, 'p5': 5})

    def test_xor(self):
        query = (
            self.qb
            .select('*')
            .from_table('logical_operators')
            .where(
                xor(
                    eq('col1', 1),
                    eq('col1', 2),
                    or_(
                        eq('col2', 3),
                        eq('col2', 4),
                    ),
                ),
                eq('col3', 5),
            )
         )

        self.assertEqual(
            query.get_sql(),
            'SELECT * FROM logical_operators WHERE (col1 = %(p1)s XOR col1 = %(p2)s XOR '
            '(col2 = %(p3)s OR col2 = %(p4)s)) AND col3 = %(p5)s'
        )

        self.assertEqual(query.get_parameters(), {'p1': 1, 'p2': 2, 'p3': 3, 'p4': 4, 'p5': 5})

    def test_and(self):
        query = (
            self.qb
            .select('*')
            .from_table('logical_operators')
            .where(
                or_(
                    and_(
                        eq('col1', 1),
                        eq('col2', 2),
                        eq('col3', 3),
                    ),
                    eq('col4', 4),
                ),
                eq('col3', 5),
            )
         )

        self.assertEqual(
            query.get_sql(),
            'SELECT * FROM logical_operators WHERE ((col1 = %(p1)s AND col2 = %(p2)s AND '
            'col3 = %(p3)s) OR col4 = %(p4)s) AND col3 = %(p5)s'
        )

        self.assertEqual(query.get_parameters(), {'p1': 1, 'p2': 2, 'p3': 3, 'p4': 4, 'p5': 5})
