#!/usr/bin/env python

import sys
import os
import pytest


# ==============================================================================
def run():
    cur_dir = os.path.abspath(os.path.dirname(__file__))

    args = sys.argv[1:]
    args.extend(['-x', cur_dir])

    return pytest.main(args)

# ==============================================================================
if __name__ == '__main__':
    sys.exit(run())
