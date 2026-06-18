from parameterized import parameterized

from david8 import QueryBuilderProtocol
from david8.expressions import window_spec
from david8.functions import sum_
from david8.predicates import eq
from david8.protocols.sql import SelectProtocol
from tests.base_test import BaseTest


class TestSelect(BaseTest):
    @parameterized.expand([
        (
            BaseTest.qb,
            'SELECT * FROM art.pictures',
        ),
        (
            BaseTest.qb_w,
            'SELECT "*" FROM "art"."pictures"',
        )
    ])
    def test_from_db(self, qb, exp_sql):
        query = (
            qb
            .select('*')
            .from_table('pictures', db_name='art')
        )

        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            BaseTest.qb,
            'SELECT * FROM pictures AS virtual_table',
            'SELECT * FROM legacy_db.pictures AS virtual_db_table',
        ),
        (
            BaseTest.qb_w,
            'SELECT "*" FROM "pictures" AS "virtual_table"',
            'SELECT "*" FROM "legacy_db"."pictures" AS "virtual_db_table"'
        )
    ])
    def test_from_alias(self, qb: QueryBuilderProtocol, table_sql: str, db_tabl_sql: str):
        query = (
            qb
            .select('*')
            .from_table('pictures', alias='virtual_table')
        )

        self.assertEqual(query.get_sql(), table_sql)
        query = (
            qb
            .select('*')
            .from_table('pictures', 'virtual_db_table', 'legacy_db')
        )

        self.assertEqual(query.get_sql(), db_tabl_sql)

    def test_select_from_query(self):
        query = (
            BaseTest.qb
            .select('*')
            .from_expr(
                BaseTest.qb
                .select('*')
                .from_table('music')
                .where(eq('band', 'Port-Royal')),
            )
            .where(eq('EPs', 'Anya: Sehnsucht EP'))
        )

        self.assertEqual(
            query.get_sql(),
            'SELECT * FROM (SELECT * FROM music WHERE band = %(p1)s) WHERE EPs = %(p2)s'
        )

        self.assertEqual(query.get_parameters(), {'p1': 'Port-Royal', 'p2': 'Anya: Sehnsucht EP'})

    @parameterized.expand([
        (
            BaseTest.qb.select(
                sum_('salary').over(order_by=['salary'], window='w').as_('by_dept')
            )
            .from_table('events')
            .window('w', window_spec(partition_by=['debt'])),
            'SELECT sum(salary) OVER (w ORDER BY salary) AS by_dept FROM events WINDOW w AS (PARTITION BY debt)',
        ),
        (
            BaseTest.qb.select('*').from_table('events')
            .window('base', window_spec(partition_by=['debt']))
            .window('new_window', window_spec(window='base', order_by=['salary'])),
            'SELECT * FROM events WINDOW base AS (PARTITION BY debt), new_window AS (base ORDER BY salary)',
        ),
        (
            BaseTest.qb_w.select('*').from_table('events')
            .window('base', window_spec(partition_by=['debt']))
            .window('new_window', window_spec(window='base', order_by=['salary'])),
            'SELECT "*" FROM "events" WINDOW base AS (PARTITION BY "debt"), new_window AS (base ORDER BY "salary")'
        )
    ])
    def test_window(self, query: SelectProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)
