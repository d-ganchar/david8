from parameterized import parameterized

from david8 import QueryBuilderProtocol, get_qb
from david8.dialects import ClickhouseDialect
from david8.expressions import Column, Parameter, as_
from david8.functions import concat
from tests.base_test import BaseTest


class TestFunctions(BaseTest):

    @parameterized.expand([
        (
            get_qb(ClickhouseDialect()),
            "SELECT concat('static-value', col1, %(p1)s, '1', '0.5'), concat(col2, %(p2)s, 'static-value2') AS "
            "alias FROM test",
        ),
        (
            get_qb(ClickhouseDialect(True)),
            'SELECT concat(\'static-value\', "col1", %(p1)s, \'1\', \'0.5\'), '
            'concat("col2", %(p2)s, \'static-value2\') AS "alias" FROM "test"',
        )
    ])
    def test_concat(self, qb: QueryBuilderProtocol, exp_sql: str):
        query = (
            qb
            .select(
                concat(
                    'static-value',
                    Column('col1'),
                    Parameter('value'),
                    1,
                    0.5,
                ),
                as_(
                    concat(Column('col2'), Parameter('value2'), 'static-value2'),
                    'alias'
                ),
            )
            .from_table('test')
        )

        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual({'p1': 'value', 'p2': 'value2'}, query.get_parameters())
