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
@click.pass_context
def add(ctx):

    name = click.prompt("Name new session")

    if re.search(':',name):
        click.echo("Invalid character. Cannot use ':' in session name")
        ctx.invoke(add)

    sessions = tm.tmux_sessions()

    for s in sessions:
        if '{0}{1}'.format(name,':') in s:
            comm = tm.resume_session('{0}{1}'.format(name,':'))
            tm.cmd(comm)


    command = "tmux new-session -s '{0}'".format(name)

    return tm.cmd(command)

@main.command()
def kill():
    sessions = tm.tmux_sessions()

    if len(sessions)<=0:
        click.echo("No active sessions")
        exit(0)

    ask = click.prompt("Select a session to kill",type=int)

    if ask>0 and ask<=len(sessions):
        session = sessions[(ask-1)]
        command = tm.kill_session(session)
        return tm.cmd(command)



