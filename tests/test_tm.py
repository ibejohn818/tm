#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `tm` package."""

import pytest

from click.testing import CliRunner

from textwrap import *
from tm import tm
from tm import cli
import click
import subprocess
import inspect

@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')

@pytest.fixture
def session_list():
    slist = [
            'session 1:some text',
            'session 2:some more text',
            'session 3:some more text'
            ]
    return slist


def test_list_tmux_sessions(session_list, monkeypatch):
    global cap
    cap = ''
    def click_echo(s):
        global cap
        cap = '{0}{1}\n'.format(cap,s)

    monkeypatch.setattr(click, 'echo', click_echo)

    tm.list_tmux_sessions(session_list)

    assert 'session 1:' in cap
    assert ':some more text' in cap

def test_tmux_sessions(monkeypatch):

    def tm_cmd(arg):
        s = dedent("""
        test1:text
        test2:text
        test3:text
        """)
        o = 0
        return s,o

    monkeypatch.setattr(tm,"cmd",tm_cmd)

    sess = tm.tmux_sessions()
    assert 'test1:text' in sess
    assert 'test2:text' in sess

def test_tmux_kill_session():

    cmd = tm.kill_session('test1:text')

    assert cmd == 'tmux kill-session -t test1'

def test_tmux_resume_session():

    cmd = tm.resume_session('test1:text')

    assert cmd == "tmux attach -t 'test1'"

def test_cmd(monkeypatch):

    class mock_obj(object):
        def __init__(self,cm):
            self.returncode = 0
            self.cmd = cm
        def communicate(self):
            return self.cmd

    def popen_mock(arg, **kwargs):
        com = mock_obj(arg)
        return com

    monkeypatch.setattr(subprocess,'Popen',popen_mock)

    res = tm.cmd('test func')

    assert res[0] == 'testfunc'
    assert res[1] == 0


def test_cli_main(monkeypatch):
    def tmux_session_mock():
        return []

    def mock_tm_cmd(s):
        print(s)

    monkeypatch.setattr(tm,'tmux_sessions',tmux_session_mock)
    monkeypatch.setattr(tm,'cmd',mock_tm_cmd)


    runner = CliRunner()
    res = runner.invoke(cli.main,input='1')
    assert 'Name new session:' in res.output

    runner = CliRunner()
    res = runner.invoke(cli.main,input='TestName\n')
    assert 'Name new session:' in res.output
    assert "tmux new-session -s 'TestName'" in res.output

    def tmux_session_mock():
        return [
                'test1:text',
                'test2:text'
                ]

    monkeypatch.setattr(tm,'tmux_sessions',tmux_session_mock)
    runner = CliRunner()
    res = runner.invoke(cli.main,input='1')
    assert "tmux attach -t 'test1'" in res.output

    runner = CliRunner()
    res = runner.invoke(cli.main,input='6\n1\n')
    assert "Invalid Selection" in res.output

    runner = CliRunner()
    res = runner.invoke(cli.main,input='0\nTestName\n')
    assert "Name new session:" in res.output

def test_cli_add(monkeypatch):

    def mock_tmux_sessions():
        return [
                'test1:text',
                'test2:text'
                ]

    def mock_cmd(s):
        print s

    monkeypatch.setattr(tm, 'tmux_sessions', mock_tmux_sessions)
    monkeypatch.setattr(tm, 'cmd', mock_cmd)

    runner = CliRunner()
    res = runner.invoke(cli.add,input='test3')

    assert 'Name new session: test3' in res.output
    assert "tmux new-session -s 'test3'" in res.output


    runner = CliRunner()
    res = runner.invoke(cli.add,input='test:test\ntest')
    assert 'Invalid' in res.output

    runner = CliRunner()
    res = runner.invoke(cli.add,input='test1\ntest1\n')
    assert "tmux attach -t 'test1'" in res.output

def test_cli_kill(monkeypatch):

    def mock_cmd(s):
        print(s)

    def mock_tmux_sessions():
        return [
                'test1:text',
                'test2:text'
                ]
    monkeypatch.setattr(tm, 'cmd', mock_cmd)
    monkeypatch.setattr(tm, 'tmux_sessions', mock_tmux_sessions)

    runner = CliRunner()
    res = runner.invoke(cli.kill, input='1')

    assert 'Select a session to kill:' in res.output
    assert 'tmux kill-session -t test1' in res.output

    runner = CliRunner()
    res = runner.invoke(cli.kill, input='6\n1\n')

    assert 'Invalid' in res.output

    def mock_tmux_sessions():
        return []

    monkeypatch.setattr(tm, 'tmux_sessions', mock_tmux_sessions)

    runner = CliRunner()
    res = runner.invoke(cli.kill)
    assert 'No active sessions' in res.output



