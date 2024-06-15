#
# Copyright (C) 2024 RomanLabs, Rafael Roman Otero
# This file is part of RLabs MiniBox.
#
# RLabs MiniBox is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RLabs MiniBox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RLabs MiniBox. If not, see <http://www.gnu.org/licenses/>.
#
'''
    Run Manual Test
    (entry point)

    For help type:
      poetry run manual-test-run --help

'''
import logging
from rlabs_mini_box import logger
from pathlib import Path

LOG_DIR = Path('../logs')

def main():
    '''
        main
    '''

    ##
    ##  There's no main in a package, this is just a sample
    ##  for when building the classes
    ##
    ##  Replace this with a test
    ##
    logger.enable_pretty_tracebacks()

    from rlabs_mini_box.data import Box

    json_str_data = \
'''
{
  "key": [
    {
      "a1": "vala1",
      "a2": "vala2"
    },
    {
      "b1": "valb1",
      "b2": "valb2"
    },
    {
      "c1": "valc1",
      "c2": "valc2"
    }
  ],
  "key2": {
    "field1": 1,
    "field2": 2,
    "field3": [
      1,
      2,
      3
    ]
  }
}
'''

    Box.config(
        log_level=logging.DEBUG,
        operations_log_dir=LOG_DIR,
    )

    box = (
        Box(json_str_data)
        .from_json()
        .key('key')
        .range(
            (1,2),
            inclusive=True
        )
        .map(
            lambda x: {k: v.upper() for k, v in x.items()}
        )
        .filter(
            lambda x: 'c1' in x
        )
        .select(
            ['c1']
        )
        .index(0)
        .to_json()
    )
    print(
        box.data()
    )

