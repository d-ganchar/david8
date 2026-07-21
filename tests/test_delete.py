from dataclasses import dataclass

from parameterized import parameterized

from david8.expressions import Source
from david8.expressions import field_ as f
from david8.predicates import eq, le
from david8.protocols.sql import AliasedProtocol as Aliased
from david8.protocols.sql import DeleteProtocol
from tests.base_test import BaseTest


@dataclass(slots=True)
class _MetricsTable(Source):
    _david8_source = 'metrics'

    name: Aliased = f('name')
    year: Aliased = f('year')


@dataclass(slots=True)
class _LegacyMetricsTable(Source):
    _david8_source = 'Metric'
    _david8_db = 'analytics'

    name: Aliased = f('m_name')
    year: Aliased = f('m_year')


_metrics = _MetricsTable()
_old_metric = _LegacyMetricsTable()


class TestDelete(BaseTest):
    @parameterized.expand([
        (
            BaseTest.qb
            .delete()
            .from_table('movie')
            .where(eq('name', ''), le('year', 1888)),
            'DELETE FROM movie WHERE name = %(p1)s AND year <= %(p2)s',
            {'p1': '', 'p2': 1888},
        ),
        (
            BaseTest.qb
            .delete()
            .from_table('movie', 'art')
            .where(eq('name', ''), le('year', 1888)),
            'DELETE FROM art.movie WHERE name = %(p1)s AND year <= %(p2)s',
            {'p1': '', 'p2': 1888},
        ),
        (
            BaseTest.qb_w
            .delete()
            .from_table('movie')
            .where(eq('name', ''), le('year', 1888)),
            'DELETE FROM "movie" WHERE "name" = %(p1)s AND "year" <= %(p2)s',
            {'p1': '', 'p2': 1888},
        ),
        (
            BaseTest.qb_w
            .delete()
            .from_table('movie', 'art')
            .where(eq('name', ''), le('year', 1888)),
            'DELETE FROM "art"."movie" WHERE "name" = %(p1)s AND "year" <= %(p2)s',
            {'p1': '', 'p2': 1888},
        ),
    ])
    def test_delete(self, query: DeleteProtocol, exp_sql: str, exp_params: dict):
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)

    @parameterized.expand([
        (
            BaseTest.qb
            .delete()
            .from_source(_metrics)
            .where(eq(_metrics.name, ''), le(_metrics.year, 1888)),
            'DELETE FROM metrics WHERE name = %(p1)s AND year <= %(p2)s',
            {'p1': '', 'p2': 1888},
        ),
        (
            BaseTest.qb
            .delete()
            .from_source(_old_metric)
            .where(eq(_old_metric.name, ''), le(_old_metric.year, 1888)),
            'DELETE FROM analytics.Metric WHERE m_name = %(p1)s AND m_year <= %(p2)s',
            {'p1': '', 'p2': 1888},
        ),
        (
            BaseTest.qb_w
            .delete()
            .from_source(_metrics)
            .where(eq(_metrics.name, ''), le(_metrics.year, 1888)),
            'DELETE FROM "metrics" WHERE "name" = %(p1)s AND "year" <= %(p2)s',
            {'p1': '', 'p2': 1888},
        ),
        (
            BaseTest.qb_w
            .delete()
            .from_source(_old_metric)
            .where(eq(_old_metric.name, ''), le(_old_metric.year, 1888)),
            'DELETE FROM "analytics"."Metric" WHERE "m_name" = %(p1)s AND "m_year" <= %(p2)s',
            {'p1': '', 'p2': 1888},
        ),
    ])
    def test_delete_from_source(self, query: DeleteProtocol, exp_sql: str, exp_params: dict):
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)
