import unittest

from david8 import get_default_qb


class BaseTest(unittest.TestCase):
    maxDiff = 1500

    qb = get_default_qb()                      # without quotes
    qb_w = get_default_qb(is_quote_mode=True)  # with quotes
