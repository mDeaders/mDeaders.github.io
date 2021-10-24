import sys
from engine import generator
from engine.utils import log, InternalError

try:
    generator.build_all()
except InternalError as err:
    log(err)
    print(f"\nBuild failed.")
    sys.exit(1)
