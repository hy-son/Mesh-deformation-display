from pathlib import Path

from numpy import savetxt
from trimesh.registration import mesh_other, icp
from numpy import asarray
from trimesh import load_mesh

class Compare():
    def __init__(self, mesh_orignal, mesh_deformed, save_path="mesh_deformation", log=None):
        """
        This class will align two files using the principal axes of inertia and refined the alignement with an
         interative closest point (trimesh.registration.mesh_other) and save the vertices movement in a .def file
        :param mesh_orignal: str or pathlib.Path, path to the orignal mesh
        :param mesh_deformed: str or pathlib.Path, path to the deformed mesh
        :param save_path: str or pathlib.Path, path to save the .def file. The .def file will have the same name as the
                            original mesh
        """
        self.mesh_original_path = Path(mesh_orignal)
        self.mesh_deformed_path = Path(mesh_deformed)
        self.name = self.mesh_original_path.stem
        self.save_path = Path(save_path)
        self.log = log

    def logging(self,txt, lvl = "info"):
        if self.log:
            if lvl=="info":
                self.log.info(str(txt))
            elif lvl== "debug":
                self.log.debug(str(txt))

    def align(self):
        mesh_original = load_mesh(self.mesh_original_path, process=False)
        mesh_deformed = load_mesh(self.mesh_deformed_path, process=False)
        # For optimisation reason, not all points are used for the alignment.
        if mesh_deformed.vertices.shape[0] > 100000:
            samples= mesh_deformed.vertices.shape[0] // 100
        elif mesh_deformed.vertices.shape[0] > 1000:
            samples= mesh_deformed.vertices.shape[0] // 10
        else:
            samples = mesh_deformed.vertices.shape[0] // 2
        self.logging(f"Meshes loaded, they will be aligned with {samples} samples")
        mesh_to_other, cost = mesh_deformed.register(mesh_original, samples=samples)
        #mesh_to_other, cost= mesh_deformed.register(mesh_original) # To a rigid alignement
        #mesh_to_other, transformed ,cost = icp(mesh_deformed.vertices,mesh_original.vertices)  # To a rigid alignement
        mesh_aligned = mesh_deformed.apply_transform(mesh_to_other)
        deformation = asarray(mesh_aligned.vertices - mesh_original.vertices)
        self.logging("Meshes aligned and deformation computed")
        self.deformation = deformation

    def save_def(self):
        """
        Save the deformation matrix as a .def
        """
        save_path = str(self.save_path / (str(self.name) + ".def" ))
        savetxt(save_path, self.deformation, fmt="%.8f", delimiter=',')
        self.logging(f"Deformation saved in {str(save_path)}")

# Test
if __name__ == "__main__":
    from display_results import Results, create_dummy_data

    create_dummy_data()
    name= "mesh"
    compare = Compare(f"mesh_original/{name}.obj", f"mesh_deformed/{name}.obj")
    compare.align()
    compare.save_def()

    display = Results(Path(f"mesh_original/{name}.obj"), Path(f"mesh_deformation/{name}.def"), "vertex")
    display.errors_corrections()

    display.apply_results(display="t")
    display.vedo_display()
