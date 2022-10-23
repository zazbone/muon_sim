from argparse import ArgumentParser
from pathlib import Path


parser = ArgumentParser(description="Muon sim software command line interface")
parser.add_argument(
	"generate",
	help="""\
		Generate muons dataset with the parameters set in given config file.
		See [config] argument
		""",
	type=Path
)

parser.add_argument(
	"config",
	help="Create default config file for the [generate] argument"
)

args = parser.parse_args()
print((Path() / args.generate).absolute())