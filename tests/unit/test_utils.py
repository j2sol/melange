# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import unittest
from melange.common import utils


class ParseIntTest(unittest.TestCase):

    def test_converts_invalid_int_to_none(self):
        self.assertEqual(utils.parse_int("a2z"), None)

    def test_converts_none_to_none(self):
        self.assertEqual(utils.parse_int(None), None)

    def test_converts_valid_integer_string_to_int(self):
        self.assertEqual(utils.parse_int("123"), 123)


class Exclude(unittest.TestCase):

    def test_excludes_given_keys(self):
        dictionary = {'key1': "value1", 'key2': "value2", 'key3': "value3"}
        self.assertEqual(utils.exclude(dictionary, 'key2', 'key3'),
                         {'key1': "value1"})

    def test_excludes_ignore_non_exsistant_keys(self):
        dictionary = {'key1': "value1", 'key2': "value2", 'key3': "value3"}
        self.assertEqual(utils.exclude(dictionary, 'key2', 'nonexistant'),
                         {'key1': "value1", 'key3': "value3"})


class Foo(object):
    method_execution_count = 0

    @utils.cached_property
    def bar(self):
        self.method_execution_count += 1
        return 42


class TestCachedProperty(unittest.TestCase):
    def test_retrives_the_value_returned_by_method(self):
        foo = Foo()

        self.assertEqual(foo.bar, 42)

    def test_retrives_the_same_value_all_the_time(self):
        foo = Foo()

        for i in range(1, 5):
            self.assertEqual(foo.bar, 42)

    def test_value_is_cached_after_first_method_call(self):
        foo = Foo()

        for i in range(1, 5):
            foo.bar

        self.assertEqual(foo.method_execution_count, 1)

    def test_returns_instance_of_cached_proprty_when_called_on_class(self):
        self.assertTrue(isinstance(Foo.bar, utils.cached_property))


class TestFind(unittest.TestCase):

    def test_find_returns_first_item_matching_predicate(self):
        items = [1, 2, 3, 4]

        item = utils.find((lambda item: item == 2), items)

        self.assertEqual(item, 2)

    def test_find_returns_none_when_no_matching_item_found(self):
        items = [1, 2, 3, 4]

        item = utils.find((lambda item: item == 8), items)

        self.assertEqual(item, None)