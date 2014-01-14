#!/usr/bin/env python3
# vim:fileencoding=utf-8

# Copyright (c) 2014 Masami HIRATA <msmhrt@gmail.com>

import re
import unittest


class TestYnbr(unittest.TestCase):
    def test_ynbr(self):
        from ynbr import yield_none_becomes_return

        restr_type_error_1 = (r"\A" +
                              re.escape("yield_none_becomes_return() takes" +
                                        " from 0 to 1 positional arguments" +
                                        " but 2 were given"))
        restr_type_error_2 = (r"\A" +
                              re.escape("yield_none_becomes_return() takes" +
                                        " 1 argument but 2 were given."))
        restr_type_error_3 = (r"\A" +
                              re.escape("@yield_none_becomes_return is used" +
                                        " only for generator functions"))

        @yield_none_becomes_return
        def a_ham():
            yield None

        self.assertEqual(a_ham(), None)
        del a_ham

        @yield_none_becomes_return
        def a_ham():
            num = yield 1
            return num

        self.assertEqual(a_ham(), 1)
        del a_ham

        @yield_none_becomes_return()
        def a_ham():
            yield None

        self.assertEqual(a_ham(), None)
        del a_ham

        @yield_none_becomes_return()
        def a_ham():
            num = yield 2
            return num

        self.assertEqual(a_ham(), 2)
        del a_ham

        @yield_none_becomes_return(None)
        def a_ham():
            yield None

        self.assertEqual(a_ham(), None)
        del a_ham

        @yield_none_becomes_return(None)
        def a_ham():
            num = yield 3
            return num

        self.assertEqual(a_ham(), 3)
        del a_ham

        @yield_none_becomes_return(4)
        def a_ham():
            yield None

        self.assertEqual(a_ham(), 4)
        del a_ham

        @yield_none_becomes_return(5)
        def a_ham():
            num = yield 6
            return num

        self.assertEqual(a_ham(), 6)
        del a_ham

        @yield_none_becomes_return(value=None)
        def a_ham():
            yield None

        self.assertEqual(a_ham(), None)
        del a_ham

        @yield_none_becomes_return(value=None)
        def a_ham():
            num = yield 7
            return num

        self.assertEqual(a_ham(), 7)
        del a_ham

        def a_generator():
            yield None

        @yield_none_becomes_return(value=a_generator)
        def a_ham():
            yield None

        self.assertEqual(a_ham(), a_generator)
        del a_ham, a_generator

        def a_generator():
            yield None

        @yield_none_becomes_return(value=a_generator)
        def a_ham():
            num = yield 8
            return num

        self.assertEqual(a_ham(), 8)
        del a_ham, a_generator

        @yield_none_becomes_return(value=9)
        def a_ham():
            yield None

        self.assertEqual(a_ham(), 9)
        del a_ham

        @yield_none_becomes_return(value=10)
        def a_ham():
            num = yield 11
            return num

        self.assertEqual(a_ham(), 11)
        del a_ham

        with self.assertRaisesRegex(TypeError, restr_type_error_1):
            @yield_none_becomes_return(12, 13)
            def a_ham():
                yield None

            del a_ham  # for pyflakes

        with self.assertRaisesRegex(TypeError, restr_type_error_2):
            @yield_none_becomes_return(14, value=15)
            def a_ham():
                yield None

            del a_ham  # for pyflakes

        with self.assertRaisesRegex(TypeError, restr_type_error_2):
            @yield_none_becomes_return(16, value=17)
            def a_ham():
                num = yield 18
                return num

            del a_ham  # for pyflakes

        with self.assertRaisesRegex(TypeError, restr_type_error_2):
            @yield_none_becomes_return(None, value=None)
            def a_ham():
                yield

            del a_ham  # for pyflakes

        with self.assertRaisesRegex(TypeError, restr_type_error_3):
            @yield_none_becomes_return
            def a_ham():
                pass

            del a_ham

        with self.assertRaisesRegex(TypeError, restr_type_error_3):
            @yield_none_becomes_return
            def a_ham():
                return

            del a_ham

        with self.assertRaisesRegex(TypeError, restr_type_error_3):
            @yield_none_becomes_return
            def a_ham():
                return 19

            del a_ham

        @yield_none_becomes_return(20)
        def a_ham():
            yield

        self.assertEqual(a_ham(), 20)
        del a_ham

        @yield_none_becomes_return(21)
        def a_ham():
            yield 22

        self.assertEqual(a_ham(), None)
        del a_ham

        @yield_none_becomes_return(23)
        def a_ham():
            yield
            return

        self.assertEqual(a_ham(), 23)
        del a_ham

        @yield_none_becomes_return(24)
        def a_ham():
            yield 25
            return

        self.assertEqual(a_ham(), None)
        del a_ham

        @yield_none_becomes_return
        def a_ham():
            first = yield 26
            second = yield (27, 28)
            third = yield (29,)
            return first, second, third

        self.assertEqual(a_ham(), (26, (27, 28), (29,)))
        del a_ham
