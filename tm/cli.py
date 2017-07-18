# -*- coding: utf-8 -*-

"""Console script for tmm."""

import click
import sys
import os
import shlex
import pprint
import re
from pprint import pprint
import tm


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """This is my custom help message"""


    if ctx.invoked_subcommand == None:

        sessions = tm.tmux_sessions()

        if len(sessions)<=0:
            return ctx.invoke(add)

        tm.list_tmux_sessions(sessions,show_add=True)

        ask = click.prompt("Select a session to resume",type=int)

        if ask == 0:
            return ctx.invoke(add)

        if ask<1 or ask>len(sessions):
            click.echo("Invalid Selection")
            return ctx.invoke(main)

        session = sessions[(ask-1)]

        cmd_str = tm.resume_session(session)
        tm.cmd(cmd_str)
	# cmd('tmux attach -t {0}'.format(sessions[(ask-1)]))

    else:
        pass


@main.command()
def add():

    valid = False

    while not valid:
        name = click.prompt("Name new session")
        valid = True
        if re.search(':',name):
            click.echo("Invalid character. Cannot use ':' in session name")
            valid = False

    sessions = tm.tmux_sessions()

    for s in sessions:
        if name == s.split(':')[0]:
            tm.cmd(tm.resume_session(s))
            return

    command = "tmux new-session -s '{0}'".format(name)

    return tm.cmd(command)

@main.command()
def kill():
    sessions = tm.tmux_sessions()
    valid = False
    err = 0
    while not valid:
        tm.list_tmux_sessions(sessions)
        if err>0:
            click.echo("Invalid Selection")
        if err>5:
            click.echo("Too many errors")
            return
        ask = click.prompt("Select session to kill",type=int)
        if ask>0 and ask<=len(sessions):
            valid = True
        else:
            err += 1

    session = sessions[(ask-1)]

    command = tm.kill_session(session)

    return tm.cmd(command)



