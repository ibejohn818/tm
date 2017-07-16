# -*- coding: utf-8 -*-

"""Main module."""

import re
import sys
import subprocess
import shlex
import click

def resume_session(session):
    key = session.split(':')[0]

    cmd = 'tmux attach -t {0}'.format(key)

    return cmd

def kill_session(session):

    key = session.split(':')[0]

    command = 'tmux kill-session -t {0}'.format(key)

    return command

def cmd(inp):
    """ Run a shell command

    inp -- (string) command to run including all arguments

    returns list((string) command output,(int) return code)
    """
    command = shlex.split(inp)
    com = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = ''.join(com.communicate())
    return out, com.returncode

def list_tmux_sessions(sessions):

    for k,v in enumerate(sessions):
        k = k+1
        click.echo('{0}) {1}'.format(k,v))

    return sessions

def tmux_sessions():

    s = cmd('tmux list-sessions');

    sess = [];

    s = s[0].split("\n")

    for i, v in enumerate(s):
        if not re.search(':',v):
            continue;
        index = i+1
        sess.append(v)

    return sess
