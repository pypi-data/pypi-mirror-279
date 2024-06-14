# SPDX-FileCopyrightText: 2024 CERN
#
# SPDX-License-Identifier: BSD-4-Clause

import pathlib
from typing import Optional

from roxieapi.output.parser import RoxieOutputParser

from roxieinterfaces.geom.geom import HoleDef, StepGenerator
from roxieinterfaces.mesh.stepplot import StepPlotter


def make_endspacer_step_files(
    xml_file: pathlib.Path,
    output_directory: str,
    z_max: float,
    n_straight: int = 1,
    gen_endspacers: bool = True,
    gen_coil_blocks: bool = False,
    gen_coils: bool = False,
    plot: bool = False,
    apply_sym: bool = False,
    add_hole: Optional[HoleDef] = None,
    mesh_size: float = 10.0,
    mesh_size_factor: float = 4.0,
    opt_step: int = 1,
) -> None:
    """Make all step files based on the roxie outputs in a
    certain directory.

    :param xml_file:
        Path to the Roxie output xml file

    :param output_directory:
        The directory for step file output.

    :param z_max:
        The maximum lingitudinal extension.

    :param n_straight:
        The number of straight sections in the geometry.

    :param gen_endspacers:
        If True, Endspacers will be generated (central posts, Headspacers, wedges)

    :param gen_wedges:
        If True, Endspacers will be generated (central posts, Headspacers, wedges)
    :param gen_coil_blocks:
        If True, Coil blocks (space between endspacers) will be generated
    :param gen_coils:
        If True, each single coil will be generated
    :param apply_sym:
        Flag to specify if symmetry around the xz plane is
        applied.

    :param add_hole:
        Add a hole to the inner post. Either None (no hole) or Holedef object: `HoleDef(z_pos,d_thread,d_head,l_head)`

    :param mesh_size:
        Set the size of the mesh (for plotting)

    :param mesh_size_factor:
        Set the mesh size factor (for plotting)

    :param opt_step:
        The optimization step of the run(default = 1)

    :return:
        None.
    """

    # read the output
    output = RoxieOutputParser(str(xml_file))
    wedges = output.opt[opt_step].wedgeGeometries3D
    coils = output.opt[opt_step].coilGeometries3D
    stepGen = StepGenerator(n_straight=n_straight)
    stepGen.find_max_z(wedges, z_max)
    stepGen.mesh_size = mesh_size
    stepGen.set_apply_symmetry(apply_sym)
    if add_hole:
        stepGen.add_hole(add_hole)

    stepGen.set_generate_step(pathlib.Path(output_directory))

    if plot:
        sp = StepPlotter(mesh_size_factor=mesh_size_factor, max_mesh_size=mesh_size, store_grids=False, plot=True)
        stepGen.set_step_plotter(sp)

    if gen_endspacers:
        stepGen.get_all_endspacer_geoms(wedges)
    if gen_coil_blocks:
        stepGen.get_all_coil_block_geoms(wedges)
    if gen_coils:
        stepGen.get_all_coil_geoms(coils)

    if plot:
        sp.plotter.show()
