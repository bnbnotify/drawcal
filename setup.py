#!/usr/bin/env python

import os
import sys
from setuptools import setup, find_packages

# make sure the lib is in the path
sys.path.insert(0, os.path.abspath('lib'))

try:
    import drawcal
    print(f"found drawcal {drawcal}")

except ImportError as e:
    import traceback; traceback.print_exc()
    print("could not import drawcal, aborting")
    sys.exit(1)

setup(
    name="drawcal",
    version=drawcal.__version__,
    author=drawcal.__author__,
    packages=find_packages("lib"),
    package_dir={"": "lib"},
    scripts = ["bin/drawcal"],
    zip_safe=False
)
