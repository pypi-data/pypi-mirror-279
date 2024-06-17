"""
Usage:
    pulses [--gpio <gpio>] [--initial <initialMethod>] [--loop <loopMethod>]
                           [--final <finalMethod>] [--delay <delayMethod>]
                           [--min <min>] [--max <max>] [--delay-val <delay>]
                           [--verbose]

Options:
    -g --gpio=<gpio>         GPIO to use [default: 12]
    -i --initial=<method>    Initial method [default: linear]
    -l --loop=<method>       Loop method [default: sin]
    -f --final=<method>      Final method [default: linear]
    -d --delay=<method>      Delay method [default: constant]

    -m --min=<min>           Minimum value [default: 2]
    -M --max=<max>           Maximum value [default: 50]
    -D --delay-val=<delay>   Base delay value [default: 0.01]

    -V --verbose             Verbose mode [default: True]

    -h --help                Show help.
    -v --version             Show version.

"""  # NOQA

import argparse

from pulses import VERSION

epilogue = """
"""


class Formatter(argparse.RawDescriptionHelpFormatter,
                argparse.ArgumentDefaultsHelpFormatter):
    """
    We want to show the default values and show the description
    and epilogue not reformatted, so we create our own formatter class
    """
    pass


parser = argparse.ArgumentParser(prog="pulses",
                                 description="Pulse your LED(s)",
                                 epilog=epilogue,
                                 formatter_class=Formatter)

parser.add_argument('-g', '--gpio', type=int, default=12,
                    metavar="<gpio>",
                    help="GPIO to use")
parser.add_argument('-i', '--initial', type=str, default='linear',
                    metavar="<initial method>",
                    help="Initial method")
parser.add_argument('-l', '--loop', type=str, default='sin',
                    metavar="<loop method>",
                    help="Loop method")
parser.add_argument('-f', '--final', type=str, default='linear',
                    metavar="<final method>",
                    help="Final method")
parser.add_argument('-d', '--delay', type=str, default='constant',
                    metavar="<delay method>",
                    help="Delay method")

parser.add_argument('-m', '--min', type=int, default=2,
                    metavar="<min>",
                    help="Minimum value")
parser.add_argument('-M', '--max', type=int, default=50,
                    metavar="<max>",
                    help="Max value")
parser.add_argument('-D', '--delay-val', type=float, default=0.01,
                    metavar="<delay value>",
                    help="Base delay value")

parser.add_argument('-V', '--verbose', action='store_true', default=False,
                    help="Verbose mode")

parser.add_argument('--version', action='version',
                    version=f'%(prog)s {VERSION}')
