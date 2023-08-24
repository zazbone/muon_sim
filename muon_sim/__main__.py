from argparse import ArgumentParser
from pathlib import Path
from muon_sim.sampler import MuonSampler
from muon_sim.geometry import FullGeometry, Vector, Ray
import pandas as pd
import numpy as np

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

run_kind = ARGS.run.lower()
if run_kind == "muon":
    sampler = MuonSampler(Vector(0, 0, 0), 0.4, (-0.6, 0), (50, 100))
    sampler.save_to(ARGS.nevent, ARGS.file)
elif run_kind == "geometry":
    geom = FullGeometry(Vector(0, 0, -0.3), 0.6, 0.4, Vector(0, 0, 1))
    muons = pd.read_parquet(ARGS.file, engine="pyarrow")
    print(muons.head(100))
    raise NotImplemented
    muons_ray = Ray(
        Vector(muons["x0"], muons["y0"], muons["z0"]),
        Vector(muons["dx"], muons["dy"], muons["dz"])
    )
    (lmb1, lmb2), cross = geom.ray_intersect(muons_ray)
    r1 = muons_ray.get_pos(lmb1)
    r2 = muons_ray.get_pos(lmb2)
    d = np.where(cross,
        r2.translate(-r1).norm(),
        None
    )
    
    
else:
    raise NotImplementedError
