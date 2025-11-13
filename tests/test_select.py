from parameterized import parameterized

from david8 import get_qb
from david8.dialects import (
    ClickhouseDialect,
)
from david8.expressions import Column, as_
from david8.predicates import eq_val
from tests.base_test import BaseTest


class TestSelect(BaseTest):
    @parameterized.expand([
        (
            get_qb(ClickhouseDialect()),
            'SELECT name, creator AS painter, painter = %(p1)s AS is_giger FROM pictures',
        ),
        (
            get_qb(ClickhouseDialect(True)),
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
            get_qb(ClickhouseDialect()),
            'SELECT * FROM art.pictures',
        ),
        (
            get_qb(ClickhouseDialect(True)),
            'SELECT "*" FROM "art"."pictures"',
        )
    ])
    def test_from_db(self, qb, exp_sql):
        query = (
            qb
            .select('*')
            .from_table('pictures', 'art')
        )

        self.assertEqual(query.get_sql(), exp_sql)
