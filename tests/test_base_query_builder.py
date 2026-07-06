import dataclasses

from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import ExprProtocol
from tests.base_test import BaseTest


class TestBaseQueryBuilder(BaseTest):
    def test_query(self):

        @dataclasses.dataclass(slots=True)
        class MyExpr(ExprProtocol):
            static_param: int
            dynamic_param: str

            def get_sql(self, dialect: DialectProtocol) -> str:
                _, alias = dialect.get_paramstyle().add_param(self.dynamic_param)
                col_name = dialect.quote_ident('col_name')
                return f'CUSTOM SQL ... SELECT {self.static_param}, {alias}, {col_name}'

        query = self.qb.query(MyExpr(static_param=1, dynamic_param='test'))
        self.assertEqual(query.get_sql(), 'CUSTOM SQL ... SELECT 1, %(p1)s, col_name')
        self.assertEqual(query.get_parameters(), {'p1': 'test'})
