from tests.base_test import BaseTest


class TestGroupBy(BaseTest):

    def test_group_by_without_quote(self) -> None:
        query = self.qb.select('col1', 'col2').from_table('table1').group_by('col1')
        query.group_by('col2')

        self.assertEqual(query.get_sql(), 'SELECT col1, col2 FROM table1 GROUP BY col1, col2')

        query = self.qb.select('col1', 'col2').from_table('table1').group_by(1)
        query.group_by(2)

        self.assertEqual(query.get_sql(), 'SELECT col1, col2 FROM table1 GROUP BY 1, 2')

    def test_group_by_with_quote(self) -> None:
        query = self.qb_w.select('col1', 'col2').from_table('table1').group_by('col1')
        query.group_by('col2')

        self.assertEqual(query.get_sql(), 'SELECT "col1", "col2" FROM "table1" GROUP BY "col1", "col2"')

        query = self.qb_w.select('col1', 'col2').from_table('table1').group_by(1)
        query.group_by(2)

        self.assertEqual(query.get_sql(), 'SELECT "col1", "col2" FROM "table1" GROUP BY 1, 2')
