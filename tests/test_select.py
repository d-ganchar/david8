from parameterized import parameterized

from tests.base_test import BaseTest, qb


class TestSelect(BaseTest):
    @parameterized.expand([
        (
            (
                qb
                .select('name', 'age')
                .from_table('users')
                .group_by('name', 'age')
            ),
            'SELECT name, age FROM users GROUP BY name, age',
            []
        ),
        (
            (
                qb
                .select('name', 'age')
                .from_table('users')
                .group_by('name', 'age')
                .limit(10)
            ),
            'SELECT name, age FROM users GROUP BY name, age LIMIT 10',
            []
        ),
        (
            (qb.select('*').from_table('artists').where(qb.cond().eq('name', 'Hammock'))),
            'SELECT * FROM artists WHERE name = ?',
            ['Hammock']
        ),
        (
            (qb.select('*').from_table('users').limit(3)),
            'SELECT * FROM users LIMIT 3',
            []
        ),
        (
            (qb.select('74 AS age', "'Giger' AS painter")),
            "SELECT 74 AS age, 'Giger' AS painter",
            []
        )
    ])
    def test_simple_select(self, query, exp_sql, exp_params):
        sql, params = query.to_sql()
        self.assertEqual(sql, exp_sql)
        self.assertEqual(params, exp_params)
