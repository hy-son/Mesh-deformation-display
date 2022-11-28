# Mesh-deformation-display

This project compute the deformation between an original mesh and it's deformed version.
It take at inputs n pairs of 2 stl or obj files (the original and the deformed one) stored in the `mesh_deformed` and 
`mesh_orignal` folders.

The 2 files are aligned using two methods; first, with the principal axes of inertial, then this alignment is refined 
using the iterative closest point (ICP). This methods make that objects with symmetry may fail to be aligned, prefer 
object with lot of variation like the Stanford bunny used as example.

## Project architecture:
- **mesh_deformation** : Folder where are stored the `.def` and `.vtk` results files. 
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

## Generation of example file:
You can generate fake original and deformed file by using just running `display_results.py`. This will automatically 
call `create_dummy_data`, loading the sample mesh saved in `mesh_original` and apply a deformation on it (there are 
random value in this deformation), then save the deformed mesh in `mesh_deformed`.

## Uses:
Put as many pairs (two file with the same name) of original and deformed files into `mesh_deformed` and `mesh_original` 
folder and run `main.py`.
`main.py` will automatically detect all files with the same name and compute there deformation and generate 2 files in
`mesh_deformation`:
- `*.def`: A simple txt file containing the X,Y and Z deformation of every vertices
- `*.vtk`: A Paraview file, allowing to see the mesh and it's deformations.

Note:
In Paraview, the `t` deformation correspond to the sum of the X,Y and Z deformation and `n` is the normal of those 
deformation.

## Displayed data
Deformed files are saved in the `mesh_deformation` folder. The `vtk` file can be opened with the software Paraview.
For each files, the deformation are saved for each axis: x,y and z. Two other view are also represented;
`t` the total deformation (x+y+z), and `n` the normal of the deformation vector.


