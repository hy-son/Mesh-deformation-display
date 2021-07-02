from pathlib import Path
from tqdm import tqdm
from compute_deformation import Compare
from display_results import Results
import logging

files = []
files.extend(list(Path(r"mesh_original").glob("*.stl")))
files.extend(list(Path(r"mesh_original").glob("*.obj")))
files.reverse()

logging.basicConfig(level=logging.DEBUG, filename= f'logs.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger("Deformation")
log.info(f"Start working on {str(len(files)) files}\n\n")

for ori in tqdm(files):
    log.info("---------------------------------")
    name = ori.name
    log.info(f"Start working on {name}")
    compare = Compare(f"mesh_original/{name}", f"mesh_deformed/{name}")
    compare.align()
    compare.save_def()

    display = Results(Path(f"mesh_original/{name}"), Path(f"mesh_deformation/{ori.stem}.def"), "vertex")
    display.errors_corrections()

    display.apply_results(display="t")
    display.vedo_display(to_file=True)

