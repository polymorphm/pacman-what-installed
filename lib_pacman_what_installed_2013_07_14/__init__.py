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
            
            if line in group_list:
                raise ReadGroupListError('duplication of group name {!r}'.format(line))
            
            group_list.append(line)
    
    return tuple(group_list)

def get_pkg_list(cmd, arg=None):
    assert isinstance(cmd, tuple)
    assert arg is None or isinstance(arg, str)
    
    if arg is not None:
        cmd += (arg,)
    
    raw_result = subprocess.check_output(cmd)
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
        query_list = get_pkg_list(PACMAN_QUERY_GROUP_CMD, arg=group)
        sync_list = list(get_pkg_list(PACMAN_SYNC_GROUP_CMD, arg=group))
        
        for pkg in query_list:
            if pkg in query_explicit_list:
                query_explicit_list.remove(pkg)
        
        for pkg in tuple(sync_list):
            if pkg in query_list:
                sync_list.remove(pkg)
        
        info_ctx.query_group_map[group] = query_list
        info_ctx.sync_group_map[group] = tuple(sync_list)
    
    info_ctx.query_explicit_list = tuple(query_explicit_list)
    
    return info_ctx

def show_info_ctx(info_ctx):
    print('explicit installed:')
    
    for pkg in info_ctx.query_explicit_list:
        print('{}{}'.format(' ' * 4, pkg))
    
    for group in info_ctx.group_list:
        if not info_ctx.query_group_map[group] and not info_ctx.sync_group_map[group]:
            continue
        
        print('\n{} group:'.format(group))
        
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
