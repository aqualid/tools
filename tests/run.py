#!/usr/bin/env python

import sys
import os
import pytest


# ==============================================================================
def run(args=None):
    cur_dir = os.path.abspath(os.path.dirname(__file__))

    if args is None:
        args = sys.argv[1:]
    else:
        if not args:
            args = []
        else:
            args = list(args)

    args.extend(['-x', cur_dir])

    return pytest.main(args)

# ==============================================================================
if __name__ == '__main__':
    sys.exit(run())
