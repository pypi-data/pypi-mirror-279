#!/usr/bin/env python

from typing import List, Sequence
from cmds import Arguments, Command, CommandGroup
from dataclasses import dataclass


@dataclass
class CustomArgs(Arguments):
    a: int = 0
    b: int = 1
    c: str = 'apple'
    d: bool = True


class Cmd0(Command):
    def command(self) -> str | Sequence[str]:
        return f'echo {self.args.a}'


class Cmd1(Command):
    def command(self) -> str | Sequence[str]:
        return f'echo {self.args.d}'


def test_single():
    arg = CustomArgs()
    cmd0 = Cmd0(arg)
    cmd0.run()
    print('print result:')
    print(cmd0)


def test_group():
    arg = CustomArgs()
    group = CommandGroup(arg, [Cmd0, Cmd1])
    group.run()
    print('print result:')
    print(group)


if __name__ == '__main__':
    # TODO: support recursive command Group
    # TODO: --help message for command group
    # test_single()
    test_group()
