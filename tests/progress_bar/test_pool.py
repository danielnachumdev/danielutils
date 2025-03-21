import unittest
from typing import Any
try:
    from danielutils import ProgressBarPool, AsciiProgressBar, AttrContext, bprint
except:
    from ...danielutils import ProgressBarPool, AsciiProgressBar, AttrContext, bprint

pool = ProgressBarPool(
    AsciiProgressBar,
    3,
    individual_options=[
        dict(iterator=range(3), desc="deco"),
        dict(iterator=range(3), desc="wrapper"),
        dict(iterator=range(3), desc="inner")
    ]
)


class MockStdout:
    def __init__(self) -> None:
        self.writes = []

    def write(self, text: Any) -> None:
        self.writes.append(text)

    def flush(self) -> None: ...


class TestProgressBarPool(unittest.TestCase):
    def test1(self):
        with AttrContext(bprint, "stream", out := MockStdout()):
            bar = AsciiProgressBar(range(10), position=0)
            for i in bar:
                bar.write(i)
        expected = [' |                                                  | 0.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K', '0\n',
                    ' |                                                  | 0.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K',
                    ' |#####                                             | 1.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A', '\x1b[2K',
                    ' |#####                                             | 1.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K', '1\n',
                    ' |#####                                             | 1.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K',
                    ' |##########                                        | 2.00/10.00it [0.00<?, 999.60it/s]\n',
                    '\x1b[1A', '\x1b[2K',
                    ' |##########                                        | 2.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K', '2\n',
                    ' |##########                                        | 2.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K',
                    ' |###############                                   | 3.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A', '\x1b[2K',
                    ' |###############                                   | 3.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K', '3\n',
                    ' |###############                                   | 3.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K',
                    ' |####################                              | 4.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A', '\x1b[2K',
                    ' |####################                              | 4.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K', '4\n',
                    ' |####################                              | 4.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K',
                    ' |#########################                         | 5.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A', '\x1b[2K',
                    ' |#########################                         | 5.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K', '5\n',
                    ' |#########################                         | 5.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K',
                    ' |##############################                    | 6.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A', '\x1b[2K',
                    ' |##############################                    | 6.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K', '6\n',
                    ' |##############################                    | 6.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K',
                    ' |###################################               | 7.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A', '\x1b[2K',
                    ' |###################################               | 7.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K', '7\n',
                    ' |###################################               | 7.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K',
                    ' |########################################          | 8.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A', '\x1b[2K',
                    ' |########################################          | 8.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K', '8\n',
                    ' |########################################          | 8.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K',
                    ' |#############################################     | 9.00/10.00it [0.00<?, 1001.74it/s]\n',
                    '\x1b[1A', '\x1b[2K',
                    ' |#############################################     | 9.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K', '9\n',
                    ' |#############################################     | 9.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A',
                    '\x1b[2K',
                    ' |##################################################| 10.00/10.00it [0.00<?, 0.00it/s]\n',
                    '\x1b[1A', '\x1b[2K',
                    ' |##################################################| 10.00/10.00it [0.00<?, 0.00it/s]\n']
        expected = [line.split('[')[0] if '\n' in line else line for line in expected]
        got = [line.split('[')[0] if '\n' in line else line for line in out.writes]
        self.assertListEqual(expected, got)
