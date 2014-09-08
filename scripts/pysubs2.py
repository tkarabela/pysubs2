#!/usr/bin/env python

import sys
import pysubs2

if __name__ == "__main__":
    cli = pysubs2.cli.Pysubs2CLI()
    rv = cli(sys.argv[1:])
    sys.exit(rv)
