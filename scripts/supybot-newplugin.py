#!/usr/bin/env python

import supybot

import os
import sys
import os.path
import optparse

if sys.version_info < (2, 3, 0):
    sys.stderr.write('This script requires Python 2.3 or newer.\n')
    sys.exit(-1)

import conf
from questions import *

template = '''
#!%s

###
# Copyright (c) 2002, Jeremiah Fincher
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
###

"""
Add the module docstring here.  This will be used by the setup.py script.
"""

from baseplugin import *

import utils
import privmsgs
import callbacks


def configure(onStart, afterConnect, advanced):
    # This will be called by setup.py to configure this module.  onStart and
    # afterConnect are both lists.  Append to onStart the commands you would
    # like to be run when the bot is started; append to afterConnect the
    # commands you would like to be run when the bot has finished connecting.
    from questions import expect, anything, something, yn
    onStart.append('load %s')

example = utils.wrapLines("""
Add an example IRC session using this module here.
""")

class %s(%s):
    %s


Class = %s

# vim:set shiftwidth=4 tabstop=8 expandtab textwidth=78:
'''.strip() # This removes the newlines that precede and follow the text.

def main():
    parser = optparse.OptionParser(usage='Usage: %prog [options]',
                                   version='Supybot %s' % conf.version)
    parser.add_option('-r', '--regexp', action='store_true', dest='regexp',
                      help='uses a regexp-based callback.')
    parser.add_option('-n', '--name', action='store', dest='name',
                      help='sets the name for the plugin.')
    parser.add_option('-t', '--thread', action='store_true', dest='threaded',
                      help='makes the plugin threaded.')
    (options, args) = parser.parse_args()
    if options.name:
        name = options.name
        if options.regexp:
            kind = 'regexp'
        else:
            kind = 'command'
        if options.threaded:
            threaded = True
        else:
            threaded = False
    else:
        name = something('What should the name of the plugin be?')
        if name.endswith('.py'):
            name = name[:-3]
        while name[0].islower():
            print 'Plugin names must begin with a capital.'
            name = something('What should the name of the plugin be?')
            if name.endswith('.py'):
                name = name[:-3]
        print textwrap.fill(textwrap.dedent("""
        Supybot offers two major types of plugins: command-based and
        regexp-based.  Command-based plugins are the kind of plugins
        you've seen most when you've used supybot.  They're also the
        most featureful and easiest to write.  Commands can be nested, 
        for instance, whereas regexp-based callbacks can't do nesting.

        That doesn't mean that you'll never want regexp-based callbacks.
        They offer a flexibility that command-based callbacks don't offer;
        however, they don't tie into the whole system as well.

        If you need to combine a command-based callback with some
        regexp-based methods, you can do so by subclassing
        callbacks.PrivmsgCommandAndRegexp and then adding a class-level
        attribute "regexps" that is a sets.Set of methods that are
        regexp-based.  But you'll have to do that yourself after this
        wizard is finished :)
        """).strip())
        kind = expect('Do you want a command-based plugin' \
                      ' or a regexp-based plugin?', ['command', 'regexp'])

        print textwrap.fill("""Sometimes you'll want a callback to be
        threaded.  If its methods (command or regexp-based, either one) will
        take a signficant amount of time to run, you'll want to thread them so
        they don't block the entire bot.""")
        print
        threaded = (yn('Does your plugin need to be threaded?') == 'y')

    if threaded:
        threaded = 'threaded = True'
    else:
        threaded = 'pass'
    if kind == 'command':
        className = 'callbacks.Privmsg'
    else:
        className = 'callbacks.PrivmsgRegexp'
    if name.endswith('.py'):
        name = name[:-3]
    while name[0].islower():
        print 'Plugin names must begin with a capital.'
        name = something('What should the name of the plugin be?')
        if name.endswith('.py'):
            name = name[:-3]

    python = os.path.normpath(sys.executable)
    fd = file(name + '.py', 'w')
    fd.write(template % (python, name, name, className, threaded, name))
    fd.close()
    print 'Your new plugin template is %s.py.' % name


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

# vim:set shiftwidth=4 tabstop=8 expandtab textwidth=78:
