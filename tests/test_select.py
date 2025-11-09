from parameterized import parameterized

from tests.base_test import BaseTest, qb


class TestBaseSelect(BaseTest):

    @parameterized.expand([
        (
            (
                qb
                .select('name', 'age')
                .from_table('users')
                .group_by('name', 'age')
            ),
            'SELECT name, age FROM users GROUP BY name, age'
        ),
        (
            (qb.select('*').from_table('users')),
            'SELECT * FROM users'
        ),
        (
            (qb.select('74 AS age', "'Giger' AS painter")),
            "SELECT 74 AS age, 'Giger' AS painter"
        )
    ])
    def test_select(self, query, exp_sql):
        sql, params = query.to_sql()
        self.assertEqual(sql, exp_sql)
        self.assertEqual(params, [])
