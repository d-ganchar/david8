from parameterized import parameterized

from tests.base_test import BaseTest, qb


class TestWhere(BaseTest):
    @parameterized.expand([
        (
            (
                qb
                .select('*')
                .from_table('cats')
                .where(
                    qb.cond().eq('name', 'Baksya'),
                    qb.cond().lt('age', 3),
                    qb.cond().gt('age', 1),
                    qb.cond().is_null('sadness'),
                    qb.cond().is_not_null('positive'),
                )
            ),
            'SELECT * FROM cats WHERE name = ? AND age < ? AND age > ? AND sadness IS NULL AND positive IS NOT NULL',
            ['Baksya', 3, 1],
        ),
    ])
    def test_where_conditions(self, query, exp_sql, exp_params):
        sql, params = query.to_sql()
        self.assertEqual(sql, exp_sql)
        self.assertEqual(params, exp_params)
