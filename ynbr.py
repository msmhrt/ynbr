#!/usr/bin/env python3
# vim:fileencoding=utf-8

# Copyright (c) 2014 Masami HIRATA <msmhrt@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright notice,
#        this list of conditions and the following disclaimer.
#
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys

if sys.version_info < (3, 3):  # pragma: no cover
    raise ImportError("Python >= 3.3 is required")

from functools import partial, wraps
from inspect import isgeneratorfunction

DEFAULT = object()

__all__ = ['yield_none_becomes_return']


def yield_none_becomes_return(function=DEFAULT, *, value=DEFAULT):
    """This decorator changes the yield statement to None checker for
       avoiding "if xxx is None: return" statements

    For example:
    # without this decorator:
    def get_version(self, config_path=None):
        if config_path is None:
            config_path = self.get_default_config_path()
        if config_path is None:
            return ""
        config = self.parse_config(config_path)
        if config is None:
            return ""
        program_name = config.get("program_name")
        if program_name is None:
            return ""
        match = RE_PROGRAM_VERSION.match(program_name)
        if match is None:
            return ""
        return match.group("version")

    # with this decorator:
    @yield_none_becomes_return("")
    def get_version(self, config_path=None):
        if config_path is None:
            config_path = yield self.get_default_config_path()
        config = yield self.parse_config(config_path)
        program_name = yield config.get("program_name")
        match = yield RE_VERSION.match(program_name)
        return match.group("version")
    """

    if not isgeneratorfunction(function):
        if function is DEFAULT:
            if value is DEFAULT:
                # @yield_none_becomes_return()  # CORRECT
                value = None
        else:
            if callable(function):
                raise TypeError("@yield_none_becomes_return is used only " +
                                "for generator functions")

            if value is not DEFAULT:
                # @yield_none_becomes_return("B", value="C")  # WRONG
                raise TypeError("yield_none_becomes_return() takes " +
                                "1 argument but 2 were given.")

            # @yield_none_becomes_return("A")  # CORRECT
            value = function
        return partial(yield_none_becomes_return, value=value)
    else:
        if value is DEFAULT:
            value = None

    @wraps(function)
    def _yield_none_becomes_return(*args, **kwargs):
        generator = function(*args, **kwargs)
        try:
            return_value = next(generator)
            while True:
                if return_value is not None:
                    return_value = generator.send(return_value)
                else:
                    return value
        except StopIteration as exception:
            return exception.value

    return _yield_none_becomes_return
