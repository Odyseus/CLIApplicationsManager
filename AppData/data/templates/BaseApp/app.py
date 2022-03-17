#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from AppData.{{APP-SLUG-CAMEL}}App.cli import main

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.append("--help")

    sys.exit(main())
