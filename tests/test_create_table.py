from parameterized import parameterized

from david8.predicates import eq
from david8.protocols.sql import CreateTableProtocol
from tests.base_test import BaseTest


class TestCreateTable(BaseTest):
    @parameterized.expand([
        (
            BaseTest.qb
            .create_table_as(
                BaseTest.qb.select('*').from_table('users').where(eq('status', 'active')),
                'active_users',
            ),
            'CREATE TABLE active_users AS SELECT * FROM users WHERE status = %(p1)s',
            {'p1': 'active'},
        ),
        (
            BaseTest.qb_w
            .create_table_as(
                BaseTest.qb.select('*').from_table('users').where(eq('status', 'active')),
                'active_users',
            ),
            'CREATE TABLE "active_users" AS SELECT "*" FROM "users" WHERE "status" = %(p1)s',
            {'p1': 'active'},
        ),
    ])
    def test_create_table_as(self, query: CreateTableProtocol, exp_sql: str, exp_params: dict):
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)
