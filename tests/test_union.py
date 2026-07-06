from tests.base_test import BaseTest


class TestUnion(BaseTest):
    def test_union(self) -> None:
        query = (
            self.qb
            .select('col1').from_table('table1')
            .union(
                self.qb.select('col2').from_table('table2'),
                self.qb.select('col3').from_table('table3'),
            )
            .union(
                self.qb.select('col4').from_table('table4'),
                self.qb.select('col5').from_table('table5'),
                all_flag=False,
            )
        )

        self.assertEqual(
            query.get_sql(),
            'SELECT col1 FROM table1 UNION ALL SELECT col2 FROM table2 UNION ALL SELECT col3 FROM table3 '
            'UNION SELECT col4 FROM table4 UNION SELECT col5 FROM table5'
        )
