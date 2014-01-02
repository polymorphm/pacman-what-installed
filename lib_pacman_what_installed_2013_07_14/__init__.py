# -*- mode: python; coding: utf-8 -*-
#
# Copyright 2013 Andrej A Antonov <polymorphm@gmail.com>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

assert str is not bytes

import argparse, shlex, subprocess

PACMAN_QUERY_EXPLICIT_CMD = tuple(shlex.split('pacman -Qqe'))
PACMAN_QUERY_IMPLICIT_CMD = tuple(shlex.split('pacman -Qq'))
PACMAN_QUERY_GROUP_CMD = tuple(shlex.split('pacman -Qqg'))
PACMAN_SYNC_GROUP_CMD = tuple(shlex.split('pacman -Sqg'))

class Error(Exception):
    pass

class ReadGroupListError(Error):
    pass

class InfoCtx:
    pass

def read_group_list(path):
    group_list = []
    
    with open(path, 'r', encoding='utf-8', errors='replace') as fd:
        for raw_line in fd:
            line = raw_line.strip()
            
            if not line or line.startswith('#'):
                continue
            
            line_split = line.split(sep=':', maxsplit=1)
            if len(line_split) == 2:
                line_left = line_split[0].strip()
                line_right = line_split[1].strip()
                
                if line_left == 'fake':
                    line_right_split = line_right.split(sep=':', maxsplit=1)
                    if len(line_right_split) != 2:
                        raise ReadGroupListError('invalid fake group line format {!r}'.format(line))
                    
                    group_name = line_right_split[0].strip()
                    group_pkg_list = line_right_split[1].split()
                    group = 'fake', group_name, tuple(group_pkg_list)
                else:
                    raise ReadGroupListError('unknown group line format {!r}'.format(line))
            else:
                group = line
            
            if group in group_list:
                raise ReadGroupListError('duplication of group {!r}'.format(line))
            
            group_list.append(group)
    
    return tuple(group_list)

def get_pkg_list(cmd, arg=None, ignore_process_error=None):
    assert isinstance(cmd, tuple)
    assert arg is None or isinstance(arg, (str, tuple, list))
    
    if arg is not None:
        if isinstance(arg, str):
            cmd += arg,
        elif isinstance(arg, (tuple, list)):
            cmd += arg
        else:
            assert False
    
    if ignore_process_error is None:
        ignore_process_error = False
    
    subprocess_stderr = subprocess.DEVNULL if ignore_process_error else None
    try:
        raw_result = subprocess.check_output(cmd, stderr=subprocess_stderr)
    except subprocess.CalledProcessError as e:
        if ignore_process_error:
            raw_result = e.output
        else:
            raise
    if not isinstance(raw_result, bytes):
        raw_result = b''
    
    pkg_list = []
    
    for raw_word in raw_result.split():
        word = raw_word.decode('utf-8', 'replace').strip()
        
        if not word:
            continue
        
        pkg_list.append(word)
    
    return tuple(pkg_list)

def get_info_ctx(group_list):
    info_ctx = InfoCtx()
    info_ctx.group_list = group_list
    
    query_explicit_list = list(get_pkg_list(PACMAN_QUERY_EXPLICIT_CMD))
    
    info_ctx.query_group_map = {}
    info_ctx.sync_group_map = {}
    for group in info_ctx.group_list:
        if isinstance(group, (tuple, list)) and \
                len(group) == 3 and group[0] == 'fake':
            assert isinstance(group[2], (tuple, list))
            sync_list = list(group[2])
            if group[2]:
                # XXX need not empty list for PACMAN_QUERY_IMPLICIT_CMD
                query_list = get_pkg_list(
                        PACMAN_QUERY_IMPLICIT_CMD,
                        arg=group[2],
                        ignore_process_error=True,
                        )
            else:
                query_list = ()
        elif isinstance(group, str):
            sync_list = list(get_pkg_list(PACMAN_SYNC_GROUP_CMD, arg=group))
            query_list = get_pkg_list(
                    PACMAN_QUERY_GROUP_CMD,
                    arg=group,
                    ignore_process_error=True,
                    )
        else:
            raise NotImplementedError('unknown group format')
        
        for pkg in query_list:
            if pkg in query_explicit_list:
                query_explicit_list.remove(pkg)
        
        for pkg in tuple(sync_list):
            if pkg in query_list:
                sync_list.remove(pkg)
        
        info_ctx.query_group_map[group] = tuple(query_list)
        info_ctx.sync_group_map[group] = tuple(sync_list)
    
    info_ctx.query_explicit_list = tuple(query_explicit_list)
    
    return info_ctx

def show_info_ctx(info_ctx):
    print('explicit installed:')
    
    if info_ctx.query_explicit_list:
        for pkg in info_ctx.query_explicit_list:
            print('{}{}'.format(' ' * 4, pkg))
    else:
        print('{}(none)'.format(' ' * 4))
    
    for group in info_ctx.group_list:
        if not info_ctx.query_group_map[group] and not info_ctx.sync_group_map[group]:
            continue
        
        if isinstance(group, (tuple, list)) and \
                len(group) == 3 and group[0] == 'fake':
            print('\n{} fake group:'.format(group[1]))
        elif isinstance(group, str):
            print('\n{} group:'.format(group))
        else:
            raise NotImplementedError('unknown group format')
        
        for pkg in info_ctx.query_group_map[group]:
            print('{}{}'.format(' ' * 4, pkg))
        
        for pkg in info_ctx.sync_group_map[group]:
            print('{}{} [not installed for this group]'.format(' ' * 4, pkg))

def main():
    parser = argparse.ArgumentParser(
            description='tool, that show (in nice view) what packages are installed on computer',
            )
    parser.add_argument(
            'groups',
            metavar='GROUP-LIST-FILE-PATH',
            help='path to file with installed group names',
            )
    
    args = parser.parse_args()
    
    group_list = read_group_list(args.groups)
    info_ctx = get_info_ctx(group_list)
    show_info_ctx(info_ctx)
