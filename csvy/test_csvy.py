#!/usr/bin/env python
"""
2016-11-18 22:46:27
@author: Paul Reiter
"""
import os
import pytest
import pandas as pd
from .csvy import yaml_reader, yaml_writer

test_csv = os.path.join(os.path.dirname(__file__), 'test.csv')

read_csvy = yaml_reader(pd.read_csv)
write_csvy = yaml_writer('to_csv')


def test_read_csvy():
    header, content = read_csvy(test_csv)
    assert 'test' in header and 'for_yaml' in header
    assert header['test'] == 'data'
    assert header['for_yaml'][0] == 'item1'
    assert header['for_yaml'][1] == 'item2'


def test_write_csvy():
    header = {'test': 'data', 'for_yaml': ['item1', 'item2']}
    content = pd.DataFrame({'a': [1, 4, 7], 'b': [2, 5, 8], 'c': [3, 6, 9]})
    write_csvy(header, content, 'temp.csv')

    header, content = read_csvy('temp.csv')

    assert 'test' in header and 'for_yaml' in header
    assert header['test'] == 'data'
    assert header['for_yaml'][0] == 'item1'
    assert header['for_yaml'][1] == 'item2'


if __name__ == '__main__':
    pytest.main()
