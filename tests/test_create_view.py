from parameterized import parameterized

from david8.protocols.sql import CreateTableProtocol
from tests.base_test import BaseTest


class TestCreateView(BaseTest):
    @parameterized.expand([
        (
            BaseTest.qb
            .create_view(
                BaseTest.qb.select('*').from_table('users'),
                'active_users',
            ),
            'CREATE VIEW active_users AS SELECT * FROM users',
        ),
        (
            BaseTest.qb
            .create_view(
                BaseTest.qb.select('*').from_table('users'),
                'active_users',
                'analytics'
            ),
            'CREATE VIEW analytics.active_users AS SELECT * FROM users',
        ),
        (
            BaseTest.qb
            .create_view(
                BaseTest.qb.select('*').from_table('users'),
                'active_users',
                if_not_exists=True,
            ),
            'CREATE VIEW IF NOT EXISTS active_users AS SELECT * FROM users',
        ),
        (
            BaseTest.qb
            .create_view(
                BaseTest.qb.select('*').from_table('users'),
                'active_users',
                or_replace=True,
            ),
            'CREATE OR REPLACE VIEW active_users AS SELECT * FROM users',
        ),
        (
            BaseTest.qb
            .create_view(
                BaseTest.qb.select('*').from_table('users'),
                'active_users',
                'analytics',
                or_replace=True,
            ),
            'CREATE OR REPLACE VIEW analytics.active_users AS SELECT * FROM users',
        ),
        (
            BaseTest.qb
            .create_view(
                BaseTest.qb.select('*').from_table('users'),
                'active_users',
                'analytics',
                or_replace=True,
                if_not_exists=True,
            ),
            'CREATE OR REPLACE VIEW analytics.active_users AS SELECT * FROM users',
        ),
        (
            BaseTest.qb
            .create_view(
                BaseTest.qb.select('*').from_table('users'),
                'active_users',
                or_replace=True,
                if_not_exists=True,
            ),
            'CREATE OR REPLACE VIEW active_users AS SELECT * FROM users',
        ),
        (
            BaseTest.qb_w
            .create_view(
                BaseTest.qb.select('*').from_table('users'),
                'active_users',
            ),
            'CREATE VIEW "active_users" AS SELECT "*" FROM "users"',
        ),
    ])
    def test_create_table_as(self, query: CreateTableProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)
