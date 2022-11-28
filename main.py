from pathlib import Path
from tqdm import tqdm
from compute_deformation import Compare
from display_results import Results
import logging
import argparse


def main(original_folder: str = r"mesh_original",
         mesh_deformed: str = r"mesh_deformed",
         only_icp: bool = False) -> None:
    """Compute the deformation between 2 files.

    :param original_folder: Where are stored the original files.
    :param mesh_deformed: Where are stored the deformed files.
    :param only_icp: bool, if the alignment is only done with ICP.
    :return: None
    """
    original_folder = str(original_folder)
    mesh_deformed = str(mesh_deformed)

    files = []
    files.extend(list(Path(original_folder).glob("*.stl")))
    files.extend(list(Path(original_folder).glob("*.obj")))
    files.reverse()

    logging.basicConfig(level=logging.DEBUG, filename=f'logs.log', filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s')
    log = logging.getLogger("Deformation")
    log.info(f"Start working on {str(len(files))} files\n\n")

    for ori in tqdm(files):
        log.info("---------------------------------")
        name = ori.name
        try:
            log.info(f"Start working on {name}")
            compare = Compare(f"{original_folder}/{name}", f"{mesh_deformed}/{name}", only_icp=only_icp, log=log)
            compare.align()
            compare.save_def()

            display = Results(Path(f"{original_folder}/{name}"), Path(f"mesh_deformation/{ori.stem}.def"), "vertex")
            display.errors_corrections()
            display.export_vtk(f"mesh_deformation/{ori.stem}.vtk")

        except Exception as e:
            log.error("FATAL ERROR: ")
            log.error(str(e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tool to compute the deformation to go from one mesh to it's target"
    )
    parser.add_argument("-o", "--path_original", type=str, default=r"mesh_original",
                        help="Where are saved the original files.")
    parser.add_argument("-d", "--path_deformed", type=str, default=r"mesh_deformed",
                        help="Where are saved the deformed files.")
    parser.add_argument("-i", "--only_icp", type=bool, default=False,
                        help="Set if the alignment is done with only the ICP methods (default:False).")
    args = parser.parse_args()

    main(original_folder=args.path_original, mesh_deformed=args.path_deformed, only_icp=args.only_icp)
