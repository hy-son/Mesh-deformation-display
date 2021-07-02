import trimesh
import numpy as np
from pathlib import Path

from vedo import show
from vedo.utils import trimesh2vedo
"""## False data"""

def create_dummy_data(mesh_original_path=Path(r"mesh_original"), mesh_deformation_file_path=Path(r"mesh_deformation"),
                      mesh_deformed_path=Path(r"mesh_deformed")):
    """
    This function will create a cone mesh and a deformation file to test the display.
    :return: None, create a mesh.obj and mesh.def files.
    """
    mesh = trimesh.creation.cone(radius= 10, height= 10)
    v,f = trimesh.remesh.subdivide_to_size(mesh.vertices, mesh.faces,  max_edge= 0.5 , max_iter=10)
    mesh = trimesh.Trimesh(vertices=v, faces=f)

    number_edges = len(mesh.edges)
    number_vertices = len(mesh.vertices)

    number_edges,number_vertices

    from math import sin, cos

    displacement_vertices = []
    for x,_,z in mesh.vertices:
        displacement_vertices.append([0.2*abs(cos(z)) * 0.1 * np.random.random_sample(),0.2*cos(x), 0.2*np.random.random_sample()])

    displacement_vertices = np.array(displacement_vertices)
    displacement_vertices = np.around(displacement_vertices,  decimals = 3)

    #Create dummy files
    mesh_save_path = mesh_original_path / "mesh.obj"
    mesh.export(mesh_save_path)
    def_save_path = mesh_deformation_file_path / "mesh.def"
    with open(def_save_path, "w") as file:
        for d in displacement_vertices:
            file.write(f"{d[0]},{d[1]},{d[2]}\n")

    # Save the deformed files
    mesh.vertices = mesh.vertices + displacement_vertices
    meshdef_save_path = mesh_deformed_path / "mesh.obj"
    mesh.export(meshdef_save_path)

    return displacement_vertices

# Show displacement

class Results():
    def __init__(self, mesh_file, results_file, type_results="vertex"):
        """
        Args: 
        - mesh_file (Path) 3D file to load (obj, stl)
        - results_file (Path)  path to the deformation file
        - type_results (str) : "vertex" or "edge"  
        
        """
        # Tests inputs
        if not isinstance(mesh_file, Path):
            raise Exception("mesh_file should be a pathlib.Path instance") 
        
        if not isinstance(results_file, Path):
            raise Exception("results_file should be a pathlib.Path instance") 

        if not type_results in ["vertex", "edge"]:
            raise Exception("type_results should be 'vertex' or 'edge' not '%s'"%(type_results))

        # Store data
        self.name = mesh_file.name
        self.extension = mesh_file.suffix
        self.type_results = type_results
        self.mesh = trimesh.load(str(mesh_file), process=False)
        self.results_file = results_file
        self.load_results()
        
    def errors_corrections(self):
        """
        Correct mesh errors
        """
        # fix normal so we see full part
        trimesh.repair.fix_normals(self.mesh) 
        trimesh.repair.fix_inversion(self.mesh)
        trimesh.repair.fix_winding(self.mesh)
        # Count errors faces
        err = trimesh.repair.broken_faces(self.mesh)
        if len(err)>0:
            print("WARNING: Broken %S faces detected in mesh"%len(err))

    def load_results(self):
        """
        Load deformation results from a text file.
        The deformation file must store the deformation as def_x,def_y,def_z
        """
        with open(self.results_file, "r") as file:
            lines = file.readlines()
            count = 0
            deformation = []
            # For each line, extract the deformation vector the store it
            for line in lines:
                vec = []
                [vec.append(float(i)) for i in line.split(",")]
                deformation.append(vec)
            deformation = np.array(deformation)

        if self.type_results == "vertex":
            self.deformation = deformation
        elif self.type_results == "edge":
            raise Exception("Not implemented")

    def apply_results(self,display="x" ,color_map="viridis"):
        """
        Apply the deformation results to the mesh.
        Args
        -display (str): ("x","y","z","n", "t") Display the x,y,z, norme or total of the deformation
        -color_map (srt): ("viridis") (see matplotlib.pyplot.colormaps)
        """
        display = str(display).lower()
        self.display_type = display
        # Select the x,y, z or norme value of the displacement
        if display == "x":
            self.display_deformation = np.array([i[0] for i in self.deformation])
        elif display == "y":
            self.display_deformation = np.array([i[1] for i in self.deformation])
        elif display == "z":
            self.display_deformation = np.array([i[2] for i in self.deformation])
        elif display == "n":
            self.display_deformation = np.sqrt (self.deformation[:,0]**2 + self.deformation[:,1]**2 + self.deformation[:,2]**2)
        elif display == "t":
            self.display_deformation = np.sum(self.deformation, axis=1)
        else:
            raise Exception("display must be 'x','y','z', 'n' or 't' not %s"%display)

        self.mesh.visual.vertex_colors = trimesh.visual.interpolate(self.display_deformation, color_map=color_map)

    def vedo_display(self):
        """Display the results in a 3D graph with vendo"""
        disp = trimesh2vedo(self.mesh)
        disp.pointColors(self.display_deformation, cmap='jet')
        disp.addScalarBar(title= f"{self.name} colored \n by {self.display_type} ")

        show(disp)

if __name__ == "__main__":
    create_dummy_data()
    test = Results(Path("mesh_original/mesh.obj"), Path("mesh_deformation/mesh.def"), "vertex")
    test.errors_corrections()
    test.apply_results(display="x")
    test.vedo_display() # First visualisation

