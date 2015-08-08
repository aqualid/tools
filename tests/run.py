#!/usr/bin/env python

if __name__ == '__main__':
    import sys
    import os
    import pytest

    curdir = os.path.dirname(__file__)
    os.chdir(curdir)

    sys.exit(pytest.main())
