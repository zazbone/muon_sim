from argparse import ArgumentParser
from pathlib import Path
from muon_sim.sampler import MuonSampler

parser = ArgumentParser(description="Muon sim software command line interface")
parser.add_argument(
    "run",
    help="""\
    muon | geometry | photon | pe
    """,
    type=str,
)
parser.add_argument(
    "-n",
    "--nevent",
    help="""\
		Number of muons generated if run muon is selected
		""",
    type=int,
)
parser.add_argument(
    "-f",
    "--file",
    help="""\
		Relative path of the output file.
		""",
    type=Path,
)
ARGS = parser.parse_args()


if ARGS.run.lower() == "muon":
    sampler = MuonSampler((0, 0), 0.4, (0, 0.6), (50, 100))
    sampler.save_to(ARGS.nevent, ARGS.file)
else:
    raise NotImplementedError
