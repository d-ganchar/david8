from david8 import get_qb
from david8.dialects import (
    ClickhouseDialect,
)
from tests.base_test import BaseTest


class TestUnion(BaseTest):
    def test_union(self) -> None:
        qb = get_qb(ClickhouseDialect())
        query = (
            qb
            .select('col1').from_table('table1')
            .union(qb.select('col2').from_table('table2'))
            .union(qb.select('col3').from_table('table3'), all_flag=False)
        )

        self.assertEqual(
            query.get_sql(),
            'SELECT col1 FROM table1 UNION ALL SELECT col2 FROM table2 UNION SELECT col3 FROM table3'
        )
