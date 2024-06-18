#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: nu:ai:ts=4:sw=4

#
#  Copyright (C) 2024 Joseph Areeda <joseph.areeda@ligo.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

""""""

import time

from ja_webutils.Page import Page
from ja_webutils.PageForm import PageFormText, PageForm, PageFormCheckBox, PageFormSelect
from ja_webutils.PageItem import PageItemHeader, PageItemList, PageItemArray, PageItemBlanks, PageItemString
from ja_webutils.PageTable import PageTable, PageTableRow, PageTableCell

start_time = time.time()

import argparse
import logging
from pathlib import Path
import re
import subprocess
import sys
import traceback

try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = Path(__file__).name

logger = None


def parser_add_args(parser):
    """
    Set up command parser
    :param argparse.ArgumentParser parser:
    :return: None but parser object is updated
    """
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')


def add_row(tbl, label, value, knowns, add_delete=True):
    """
    Add a row of editable information to the table
    :param add_delete:
    :param value:
    :param PageTable tbl: where to add the new row
    :param str label: 1st columns
    :param list[str] knowns: what we alread know
    :return: None
    """
    row = PageTableRow()
    label_cell = PageTableCell(label)
    value_cell = PageTableCell(value)
    known_cell = PageItemArray()
    n = 0

    for known in knowns:
        n += 1
        edit_box = PageFormText(f'{n}', known, size=40)
        known_cell.add(edit_box)
        if add_delete:
            known_cell.add(PageFormCheckBox('Delete'))
            known_cell.add(PageItemString('Delete'))

        known_cell.add(PageItemBlanks())

    known_cell.add(PageFormText(f'{n+1}', '', size=40, place_holder='add new'))

    row.add(label_cell)
    row.add(value_cell)
    row.add(known_cell)
    tbl.add_row(row)


def add_dropdown_row(tbl, label, options):
    """

    :param PageTable tbl:
    :param str label:
    :param list[str] options:
    :return:
    """
    drop_down = PageFormSelect(label, options)
    row = PageTableRow([label, drop_down])
    tbl.add_row(row)


def add_txt_row(srch_tbl, label, help_txt=''):
    """

    :param PageTable srch_tbl:
    :param str label:
    :param str help_txt:
    :return:
    """
    edit_box = PageFormText("srch", "", size=40)

    row = PageTableRow([label,edit_box, help_txt])
    srch_tbl.add_row(row)


def main():
    global logger

    logging.basicConfig()
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(description=__doc__, prog=__process_name__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_add_args(parser)
    args = parser.parse_args()
    verbosity = 0 if args.quiet else args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    # debugging?
    logger.debug(f'{__process_name__} version: {__version__} called with arguments:')
    for k, v in args.__dict__.items():
        logger.debug('    {} = {}'.format(k, v))

    edit_page = Page()
    edit_page.add_style('#chantbl tr:nth-child(even){background-color: #d2d2d2;}'
                   '#chantbl tr:nth-child(odd){background-color: #9292d2;}'
                   '#chantbl tr:hover {background-color: #ddd;}')
    edit_page.add(PageItemHeader('H1:GDS-CALIB_STRAIN', 2))
    edit_page.add_blanks(2)
    tbl = PageTable(id='chantbl')
    ifo_info = ['LHO_4k (prefix:H1)', 'localTime=0', 'longitude =-2.08407688', 'latitude =0.81079525',
                'Arm Azimuth: X=5.6549 Y=4.0841', 'Altitude: X=-0.0006 Y=0.0000', 'midPoint: X=1997.5 Y=1997.5']
    add_row(tbl, 'IFO', 'H1', ifo_info)
    add_row(tbl, 'Subsystem', 'GDS', ['Global Diagnostic System'])
    add_row(tbl, 'Fragment', 'CALIB', ['Calibrate', 'Calibration'])
    add_row(tbl, 'Fragment', 'STRAIN', [])
    add_row(tbl, 'Sample rate(s)', 'Hz', ['16384'], False)
    add_row(tbl, 'Channel types', '', ['RDS, Online, Minute trend'], False)

    edit_form = PageForm(action='/update_info')
    edit_form.add(tbl)
    edit_page.add(edit_form)

    html = edit_page.get_html()
    fname = '/tmp/cis-edit.html'
    with open(fname, 'w') as out:
        print(html, file=out)
    logger.info(f'Wrote {fname}')

    srch_page = Page()
    srch_tbl = PageTable()
    srch_page.add(PageItemHeader('CIS search', 2))

    add_dropdown_row(srch_tbl, 'IFO', ['H1', 'L1', 'V1'])
    
    add_txt_row(srch_tbl, 'Channel name', 'Wild cards * and ? may be used')
    add_txt_row(srch_tbl, 'Subsystem/Fragment', '')
    add_txt_row(srch_tbl, 'Description contains', 'list of substrings separated by spaces')

    srch_form = PageForm(action='/search')
    srch_form.add(srch_tbl)
    srch_page.add(srch_form)

    html = srch_page.get_html()
    fname = '/tmp/cis-search.html'
    with open(fname, 'w') as out:
        print(html, file=out)
    logger.info(f'Wrote {fname}')

if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, OSError, NameError, ArithmeticError, RuntimeError) as ex:
        print(ex, file=sys.stderr)
        traceback.print_exc(file=sys.stderr)

    if logger is None:
        logging.basicConfig()
        logger = logging.getLogger(__process_name__)
        logger.setLevel(logging.DEBUG)
    # report our run time
    logger.info(f'Elapsed time: {time.time() - start_time:.1f}s')
