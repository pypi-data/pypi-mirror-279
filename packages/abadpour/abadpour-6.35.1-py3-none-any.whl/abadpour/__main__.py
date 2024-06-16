import argparse
from abadpour import NAME, VERSION
from abadpour.build import build
from abadpour.logger import logger
from blueness.argparse.generic import ending

parser = argparse.ArgumentParser(NAME, description=f"{NAME}-{VERSION}")
parser.add_argument(
    "task",
    type=str,
    help="build|version",
)
args = parser.parse_args()

success = False
if args.task == "build":
    success = build()
elif args.task == "version":
    print(f"{NAME}-{VERSION}")
    success = True
else:
    success = None

ending(logger, NAME, args.task, success)
