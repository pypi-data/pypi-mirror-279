# Copyright 2020 Andrzej Cichocki

# This file is part of Leytonium.
#
# Leytonium is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Leytonium is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Leytonium.  If not, see <http://www.gnu.org/licenses/>.

'Show tree with hidden descendants but not their descendants.'
from lagoon import tree
from lagoon.program import partial
from lagoon.util import stripansi
import re, sys

denymatch = re.compile('── [.]').search

def main():
    allow = True
    allowmatch = None
    with tree._aC[partial](*sys.argv[1:]) as f:
        for line in f:
            bwline = stripansi(line)
            if not allow and allowmatch(bwline) is not None:
                allow = True
            if allow:
                sys.stdout.write(line)
                m = denymatch(bwline)
                if m is not None:
                    allow = False
                    allowmatch = re.compile(f".{{{m.start()}}}── ").match

if '__main__' == __name__:
    main()
