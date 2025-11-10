from parameterized import parameterized

from david8 import get_qb
from david8.core.dialects import (
    ClickhouseDialect,
)
from david8.core.expressions import as_
from david8.core.predicates import eq_val
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
        query = (
            qb
            .select(
                'name',
                as_('creator', 'painter'),
                as_(eq_val('painter', 'Giger'), 'is_giger'),
            )
            .from_table('pictures')
         )

        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual({'p1': 'Giger'}, query.get_parameters())
