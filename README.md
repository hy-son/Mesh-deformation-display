# Mesh-deformation-display

## Project architecture:
- **mesh_deformation** : Folder where are stored the .def files. 
- **mesh_deformed** : Folder where are stored mesh deformed
- **mesh_original** : Folder where are stored the non deformed mesh
- *display_results.py* : Script using the .def file to display the displacement value on an original mesh
- *compute_deformation.py* : Script aligning the deformed files with the original and generate the `.def`

## Installation:
1. Create a new conda environment with python 3.7
`conda env create --file environment.yml python=3.7`
1. Move your original mesh to `mesh_original`
1. Move your deformed mesh to 'mesh_deformation'
1. Run `main.py` to compute the deformation of all files in the folder

