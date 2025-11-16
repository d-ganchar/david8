from parameterized import parameterized

from david8 import QueryBuilderProtocol
from david8.expressions import Column, as_
from david8.predicates import eq_val
from tests.base_test import BaseTest


class TestSelect(BaseTest):
    @parameterized.expand([
        (
            BaseTest.qb,
            'SELECT name, creator AS painter, painter = %(p1)s AS is_giger FROM pictures',
        ),
        (
            BaseTest.qb_w,
            'SELECT "name", "creator" AS "painter", "painter" = %(p1)s AS "is_giger" FROM "pictures"',
        )
    ])
    def test_as_expression(self, qb, exp_sql):
        query = qb.select('name').from_table('pictures')
        for col in [
            as_(Column('creator'), 'painter'),
            as_(eq_val('painter', 'Giger'), 'is_giger'),
        ]:
            query.select(col)

        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual({'p1': 'Giger'}, query.get_parameters())

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
            .from_query(
                BaseTest.qb
                .select('*')
                .from_table('music')
                .where(eq_val('band', 'Port-Royal')),
            )
            .where(eq_val('EPs', 'Anya: Sehnsucht EP'))
        )

        self.assertEqual(
            query.get_sql(),
            'SELECT * FROM (SELECT * FROM music WHERE band = %(p1)s) WHERE EPs = %(p2)s'
        )

        self.assertEqual(query.get_parameters(), {'p1': 'Port-Royal', 'p2': 'Anya: Sehnsucht EP'})
