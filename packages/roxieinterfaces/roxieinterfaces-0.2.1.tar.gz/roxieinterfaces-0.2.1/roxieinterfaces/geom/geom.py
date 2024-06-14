# SPDX-FileCopyrightText: 2024 CERN
#
# SPDX-License-Identifier: BSD-4-Clause

import logging
import pathlib
from dataclasses import dataclass
from typing import Dict, Optional

import gmsh
import numpy as np
import numpy.typing as npt
from roxieapi.commons.types import Coil3DGeometry, WedgeGeometry, WedgeSurface
from roxieapi.output.parser import RoxieOutputParser

from roxieinterfaces.geom.bsplines import BSpline_3D
from roxieinterfaces.mesh.stepplot import StepPlotter


@dataclass
class HoleDef:
    z_pos: float
    d_thread: float
    d_head: float
    l_head: float


def optional_features(func):  # -> Callable[[], None]:
    """Decorator applying optional features for generation of blocks. Controlled by flags from StepGenerator
    * Apply symmetry
    * Write step file
    * write vtk file
    * plot output
    """

    def wrapper(*args, **kwargs):
        obj: StepGenerator = args[0]
        if obj.model_name:
            gmsh.model.add(obj.model_name)
        func(*args, **kwargs)
        if obj.apply_sym:
            obj._apply_symmetry()

        for target, hole in obj._hole_def.items():
            if obj.model_name and obj.model_name.startswith(target):
                surf = args[1]
                if isinstance(surf, WedgeSurface):
                    r_y = np.linalg.norm(surf.upper_edge[0, :2])

                    obj._add_hole(r_y, hole.z_pos, hole.d_thread, hole.d_head, hole.l_head)

        if obj.output_step_folder and obj.model_name:
            step_name = str(obj.output_step_folder / (obj.model_name + ".step"))
            gmsh.write(step_name)
        if obj.step_plotter:
            obj.step_plotter.plot_current_gmsh_model()
        if obj.output_vtk_folder and obj.model_name:
            vtk_name = str(obj.output_vtk_folder / (obj.model_name + ".vtk"))
            gmsh.write(vtk_name)

        # Cleanup
        obj.model_name = None
        gmsh.clear()

    return wrapper


class StepGenerator:
    """Class for generating step files from a roxie xml output.

    From an already loaded RoxieOutputParser object, this class can extract coils,
    coilblocks (between endspacers) and endspacers as step files.
    """

    def __init__(self, n_straight=1) -> None:
        """
        Initializes an instance of the class.

        Parameters:
            n_straight (int): The number of straight sections in the geometry.

        Returns:
            None
        """
        self.logger = logging.getLogger("StepGenerator")
        self.n_straight = n_straight
        self.max_z = 0.0
        self.min_z = 0.0
        self.add_z = 10.0

        self.apply_sym: bool = False
        self.step_plotter: Optional[StepPlotter] = None

        self._hole_def: Dict[str, HoleDef] = {}

        self.model_name: Optional[str] = None
        self.output_step_folder: Optional[pathlib.Path] = None
        self.output_vtk_folder: Optional[pathlib.Path] = None
        self._name_cntr = 0

        self.mesh_size = 100.0
        # initialize gmsh
        if not gmsh.isInitialized():
            gmsh.initialize()
        gmsh.option.setString("Geometry.OCCTargetUnit", "MM")
        gmsh.option.setNumber("General.Verbosity", 2)

    def set_generate_step(self, output_folder: pathlib.Path):
        self.output_step_folder = output_folder

    def set_generate_vtk(self, output_folder: pathlib.Path):
        self.output_vtk_folder = output_folder

    def set_model_name(self, name: str):
        self.model_name = name

    def set_apply_symmetry(self, apply_sym: bool):
        self.apply_sym = apply_sym

    def set_step_plotter(self, plotter: StepPlotter):
        self.step_plotter = plotter

    def add_hole(self, hole: HoleDef, target="central_post") -> None:
        """Add holes to generated profiles

        :param hole: The Hole definition ()
        :type hole: HoleDef
        :param target: The endspacer target to add a hole, defaults to "central_post"
                    One of "central_post", "headspacer", "wedge", "coilblock"
        :type target: str, optional
        """
        self._hole_def[target] = hole

    def find_max_z(self, wedges: Dict[int, WedgeGeometry], add_z: float = 10.0) -> None:
        """Find the maximum z extension over all Wedges. Use this for future headspacer generation

        :param wedges: The wedge dict from the parser
        :param add_z: The additional z value to add. Must be > 0
        """

        max_z = 0.0
        min_z = 0.0
        if add_z <= 0:
            raise ValueError("add_z must be > 0")

        for _, wedge in wedges.items():
            if wedge.inner_surface is not None:
                max_z = max(
                    max_z,
                    np.max(np.abs(wedge.inner_surface.lower_edge[:, 2])),
                    np.max(np.abs(wedge.inner_surface.upper_edge[:, 2])),
                )
                min_z = min(
                    min_z,
                    np.min(np.abs(wedge.inner_surface.lower_edge[:, 2])),
                    np.min(np.abs(wedge.inner_surface.upper_edge[:, 2])),
                )
            if wedge.outer_surface is not None:
                max_z = max(
                    max_z,
                    np.max(np.abs(wedge.outer_surface.lower_edge[:, 2])),
                    np.max(np.abs(wedge.outer_surface.upper_edge[:, 2])),
                )
                min_z = min(
                    min_z,
                    np.min(np.abs(wedge.outer_surface.lower_edge[:, 2])),
                    np.min(np.abs(wedge.outer_surface.upper_edge[:, 2])),
                )

        self.max_z = max_z
        self.min_z = min_z
        self.add_z = add_z

    def _apply_symmetry(self):
        ent_3d = gmsh.model.getEntities(3)
        solid_cpy = gmsh.model.occ.copy(ent_3d)
        gmsh.model.occ.synchronize()
        ent_3d = gmsh.model.getEntities(3)
        gmsh.model.occ.mirror(solid_cpy, 1, 0, 0, 0)
        gmsh.model.occ.synchronize()
        gmsh.model.occ.fuse([ent_3d[0]], [ent_3d[1]])
        gmsh.model.occ.synchronize()

    def _add_hole(
        self,
        R_out: float,
        z_pos_hole_winding_test: float = 40.0,
        d_thread: float = 3.1,
        d_head: float = 5.6,
        length_skrew_head=7.0,
    ) -> None:
        """_summary_

        :param R_out:
            The outer mandrel radius

        :param z_pos_hole_winding_test:
            This is the z position of the hole for the winding tests.

        :param d_thread:
            Diameter of the thread of the screw

        :param d_head:
            Diameter of the head of the screw

        :param length_screw_head:
            The length of the screw head.
        """
        radii_hole_winding_test = (d_thread / 2.0, d_head / 2.0)

        # add a cylinder
        _ = gmsh.model.occ.add_cylinder(
            0.0,
            0.0,
            z_pos_hole_winding_test,
            0.0,
            1.3 * R_out,
            0.0,
            radii_hole_winding_test[0],
        )

        _ = gmsh.model.occ.add_cylinder(
            0.0,
            R_out - length_skrew_head,
            z_pos_hole_winding_test,
            0.0,
            1.3 * R_out,
            0.0,
            radii_hole_winding_test[1],
        )

        _ = gmsh.model.occ.cut([[3, 1]], [[3, 2], [3, 3]])

        gmsh.model.occ.synchronize()

    def _make_endspacer(
        self,
        surface: WedgeSurface,
        z_back=None,
    ) -> None:
        """
        Make a solid for a CT end spacer.
        This function is designed for cylindrical mandrel surfaces only.

        :param filename:
            The filename for the step file.

        :param points_bottom:
            The inner points.

        :param points_top:
            The outer points.

        :param z_back:
            The z position of the 'back' side. If this should be an
            inner post, set this to None. If it is an endspacer set
            the maximum z position.
            Default 'None'.
        :return:
            None
        """
        points_bottom = surface.lower_edge
        points_top = surface.upper_edge

        # the number of points
        _ = points_bottom.shape[0]
        targ_h = self.mesh_size

        # first we make the spline curves of the front of the end spacer,
        # this means the curvy part

        # these are the containers for the intersections between
        # generators and mandrel surface
        points_front_top = points_top[self.n_straight :, :]
        points_front_bottom = points_bottom[self.n_straight :, :]

        # compute the accelerator coordinates at the beginning of the end spacer
        # this code was copied from ROXCCT where curved mandrels are possible.
        # We keep the software structure in case we want to use this code in the future.

        # these are the points on the back, i.e. the straight section
        points_back_outer = points_front_top.copy()
        points_back_inner = points_front_bottom.copy()

        if z_back is None:
            points_back_outer[:, 2] = points_top[0, 2]
            points_back_inner[:, 2] = points_bottom[0, 2]
        else:
            points_back_outer[:, 2] = z_back
            points_back_inner[:, 2] = z_back

        # we make parameter vectors
        t_ft = np.arctan2(np.abs(points_front_top[:, 1]), np.abs(points_front_top[:, 0]))
        t_fb = np.arctan2(np.abs(points_front_bottom[:, 1]), np.abs(points_front_bottom[:, 0]))
        t_bt = np.arctan2(np.abs(points_back_outer[:, 1]), np.abs(points_back_outer[:, 0]))
        t_bb = np.arctan2(np.abs(points_back_inner[:, 1]), np.abs(points_back_inner[:, 0]))

        # and also some knot vectors, the splines should compress sufficiently.
        knots_ft = t_ft[::2].copy()
        knots_fb = t_fb[::2].copy()
        knots_bt = t_bt[::2].copy()
        knots_bb = t_bb[::2].copy()

        knots_ft[-1] = 0.5 * np.pi
        knots_fb[-1] = 0.5 * np.pi
        knots_bt[-1] = 0.5 * np.pi
        knots_bb[-1] = 0.5 * np.pi

        bspline_ft = BSpline_3D()
        bspline_fb = BSpline_3D()
        bspline_bt = BSpline_3D()
        bspline_bb = BSpline_3D()

        bspline_ft.fit_bspline_curve(t_ft, points_front_top, knots_ft, debug=False, degree=3)
        bspline_fb.fit_bspline_curve(t_fb, points_front_bottom, knots_fb, debug=False, degree=3)
        bspline_bt.fit_bspline_curve(t_bt, points_back_outer, knots_bt, debug=False, degree=3)
        bspline_bb.fit_bspline_curve(t_bb, points_back_outer, knots_bb, debug=False, degree=3)

        gmsh_ft, p_tags_ft = bspline_ft.to_gmsh_spline(gmsh.model.occ, target_meshsize=targ_h)
        gmsh_fb, p_tags_fb = bspline_fb.to_gmsh_spline(gmsh.model.occ, target_meshsize=targ_h)

        p0_arc_bt = gmsh.model.occ.addPoint(0.0, 0.0, points_back_outer[0, 2], targ_h)
        p1_arc_bt = gmsh.model.occ.addPoint(
            points_back_outer[0, 0],
            points_back_outer[0, 1],
            points_back_outer[0, 2],
            targ_h,
        )
        p2_arc_bt = gmsh.model.occ.addPoint(
            points_back_outer[-1, 0],
            points_back_outer[-1, 1],
            points_back_outer[-1, 2],
            targ_h,
        )

        p0_arc_bb = gmsh.model.occ.addPoint(0.0, 0.0, points_back_inner[0, 2], targ_h)
        p1_arc_bb = gmsh.model.occ.addPoint(
            points_back_inner[0, 0],
            points_back_inner[0, 1],
            points_back_inner[0, 2],
            targ_h,
        )
        p2_arc_bb = gmsh.model.occ.addPoint(
            points_back_inner[-1, 0],
            points_back_inner[-1, 1],
            points_back_inner[-1, 2],
            targ_h,
        )

        gmsh_bt = gmsh.model.occ.addCircleArc(p1_arc_bt, p0_arc_bt, p2_arc_bt)
        gmsh_bb = gmsh.model.occ.addCircleArc(p1_arc_bb, p0_arc_bb, p2_arc_bb)

        gmsh.model.occ.synchronize()

        line1 = gmsh.model.occ.addLine(p_tags_ft[0], p1_arc_bt)
        line2 = gmsh.model.occ.addLine(p_tags_ft[-1], p2_arc_bt)

        line3 = gmsh.model.occ.addLine(p_tags_fb[0], p1_arc_bb)
        line4 = gmsh.model.occ.addLine(p_tags_fb[-1], p2_arc_bb)

        line5 = gmsh.model.occ.addLine(p1_arc_bt, p1_arc_bb)
        line6 = gmsh.model.occ.addLine(p2_arc_bt, p2_arc_bb)

        line7 = gmsh.model.occ.addLine(p_tags_ft[0], p_tags_fb[0])
        line8 = gmsh.model.occ.addLine(p_tags_ft[-1], p_tags_fb[-1])

        loop1 = gmsh.model.occ.addCurveLoop([gmsh_ft, line7, gmsh_fb, line8])
        loop2 = gmsh.model.occ.addCurveLoop([gmsh_ft, line1, gmsh_bt, line2])
        loop3 = gmsh.model.occ.addCurveLoop([gmsh_bt, line6, gmsh_bb, line5])
        loop4 = gmsh.model.occ.addCurveLoop([gmsh_fb, line4, gmsh_bb, line3])
        loop5 = gmsh.model.occ.addCurveLoop([line1, line5, -line3, -line7])
        loop6 = gmsh.model.occ.addCurveLoop([line2, line6, -line4, -line8])

        surf1 = gmsh.model.occ.addBSplineFilling(loop1, type="Stretch")
        surf2 = gmsh.model.occ.addBSplineFilling(loop2, type="Stretch")
        surf3 = gmsh.model.occ.addBSplineFilling(loop3, type="Stretch")
        surf4 = gmsh.model.occ.addBSplineFilling(loop4, type="Stretch")
        surf5 = gmsh.model.occ.addBSplineFilling(loop5, type="Stretch")
        surf6 = gmsh.model.occ.addBSplineFilling(loop6, type="Stretch")

        surface_loop = [gmsh.model.occ.addSurfaceLoop([surf1, surf2, surf3, surf4, surf5, surf6])]
        _ = gmsh.model.occ.addVolume(surface_loop)

        gmsh.model.occ.synchronize()

        # clean up
        ent_2d = gmsh.model.getEntities(2)
        gmsh.model.occ.remove(ent_2d)
        ent_1d = gmsh.model.getEntities(1)
        gmsh.model.occ.remove(ent_1d)
        ent_0d = gmsh.model.getEntities(0)
        gmsh.model.occ.remove(ent_0d)

        gmsh.option.setNumber("Mesh.MeshSizeFactor", 10)

        gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
        gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)
        gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 0)

        gmsh.model.occ.synchronize()

    def _make_wedge(
        self,
        points_front_bottom: npt.NDArray[np.float64],
        points_front_top: npt.NDArray[np.float64],
        points_back_bottom: npt.NDArray[np.float64],
        points_back_top: npt.NDArray[np.float64],
    ) -> None:
        targ_h = self.mesh_size

        # we extract the 'curvy' part
        p_llc = points_front_bottom[self.n_straight :, :]
        p_lrc = points_front_top[self.n_straight :, :]
        p_ulc = points_back_bottom[self.n_straight :, :]
        p_urc = points_back_top[self.n_straight :, :]

        # the number of points
        n_llc = p_llc.shape[0]
        n_lrc = p_lrc.shape[0]
        n_ulc = p_ulc.shape[0]
        n_urc = p_urc.shape[0]

        # we make a parameter vector
        t_llc = np.linspace(0.0, 1.0, n_llc)
        t_lrc = np.linspace(0.0, 1.0, n_lrc)
        t_ulc = np.linspace(0.0, 1.0, n_ulc)
        t_urc = np.linspace(0.0, 1.0, n_urc)

        bspline_llc = BSpline_3D()
        bspline_lrc = BSpline_3D()
        bspline_ulc = BSpline_3D()
        bspline_urc = BSpline_3D()

        bspline_llc.fit_to_points(t_llc, p_llc)
        bspline_lrc.fit_to_points(t_lrc, p_lrc)
        bspline_ulc.fit_to_points(t_ulc, p_ulc)
        bspline_urc.fit_to_points(t_urc, p_urc)

        # get the spline degrees
        k_llc = bspline_llc.degree
        k_ulc = bspline_ulc.degree
        k_lrc = bspline_lrc.degree
        k_urc = bspline_urc.degree

        # Define the B-Spline curves for gmsh
        points_list_llc = []
        points_list_lrc = []
        points_list_ulc = []
        points_list_urc = []

        for _, cpt in enumerate(bspline_llc.get_control_points()):
            points_list_llc.append(gmsh.model.occ.addPoint(cpt[0], cpt[1], cpt[2], targ_h))

        for _, cpt in enumerate(bspline_lrc.get_control_points()):
            points_list_lrc.append(gmsh.model.occ.addPoint(cpt[0], cpt[1], cpt[2], targ_h))

        for _, cpt in enumerate(bspline_ulc.get_control_points()):
            points_list_ulc.append(gmsh.model.occ.addPoint(cpt[0], cpt[1], cpt[2], targ_h))

        for _, cpt in enumerate(bspline_urc.get_control_points()):
            points_list_urc.append(gmsh.model.occ.addPoint(cpt[0], cpt[1], cpt[2], targ_h))

        multiplicities_llc = np.ones((len(bspline_llc.knots[k_llc:-k_llc]),))
        multiplicities_llc[0] = k_llc + 1
        multiplicities_llc[-1] = k_llc + 1

        multiplicities_ulc = np.ones((len(bspline_ulc.knots[k_ulc:-k_ulc]),))
        multiplicities_ulc[0] = k_ulc + 1
        multiplicities_ulc[-1] = k_ulc + 1

        multiplicities_urc = np.ones((len(bspline_urc.knots[k_urc:-k_urc]),))
        multiplicities_urc[0] = k_urc + 1
        multiplicities_urc[-1] = k_urc + 1

        multiplicities_lrc = np.ones((len(bspline_lrc.knots[k_lrc:-k_lrc]),))
        multiplicities_lrc[0] = k_lrc + 1
        multiplicities_lrc[-1] = k_lrc + 1

        # the splines for the four corners
        C_llc = gmsh.model.occ.addBSpline(
            points_list_llc,
            degree=k_llc,
            knots=bspline_llc.knots[k_llc:-k_llc],
            multiplicities=multiplicities_llc,
        )

        C_lrc = gmsh.model.occ.addBSpline(
            points_list_lrc,
            degree=k_lrc,
            knots=bspline_lrc.knots[k_lrc:-k_lrc],
            multiplicities=multiplicities_lrc,
        )

        C_ulc = gmsh.model.occ.addBSpline(
            points_list_ulc,
            degree=k_ulc,
            knots=bspline_ulc.knots[k_ulc:-k_ulc],
            multiplicities=multiplicities_ulc,
        )

        C_urc = gmsh.model.occ.addBSpline(
            points_list_urc,
            degree=k_urc,
            knots=bspline_urc.knots[k_urc:-k_urc],
            multiplicities=multiplicities_urc,
        )

        # the splines for the cable ends
        C0_west = gmsh.model.occ.addBSpline([points_list_ulc[0], points_list_llc[0]], degree=1)
        C0_east = gmsh.model.occ.addBSpline([points_list_urc[0], points_list_lrc[0]], degree=1)

        C0_south = gmsh.model.occ.addBSpline([points_list_lrc[0], points_list_llc[0]], degree=1)
        C0_north = gmsh.model.occ.addBSpline([points_list_urc[0], points_list_ulc[0]], degree=1)

        C1_west = gmsh.model.occ.addBSpline([points_list_llc[-1], points_list_ulc[-1]], degree=1)
        C1_east = gmsh.model.occ.addBSpline([points_list_lrc[-1], points_list_urc[-1]], degree=1)

        C1_south = gmsh.model.occ.addBSpline([points_list_llc[-1], points_list_lrc[-1]], degree=1)
        C1_north = gmsh.model.occ.addBSpline([points_list_ulc[-1], points_list_urc[-1]], degree=1)

        # Create a BSpline surface filling the six sides of the cable:
        Side1 = gmsh.model.occ.addWire([C0_west, C_llc, C1_west, C_ulc])
        Side2 = gmsh.model.occ.addWire([C0_east, C_lrc, C1_east, C_urc])

        Side3 = gmsh.model.occ.addWire([C0_north, C_ulc, C1_north, C_urc])
        Side4 = gmsh.model.occ.addWire([C0_south, C_llc, C1_south, C_lrc])

        Side5 = gmsh.model.occ.addWire([C0_south, C0_east, C0_north, C0_west])
        Side6 = gmsh.model.occ.addWire([C1_south, C1_east, C1_north, C1_west])

        s1 = gmsh.model.occ.addBSplineFilling(Side1, type="Stretch")
        s2 = gmsh.model.occ.addBSplineFilling(Side2, type="Stretch")
        s3 = gmsh.model.occ.addBSplineFilling(Side3, type="Stretch")
        s4 = gmsh.model.occ.addBSplineFilling(Side4, type="Stretch")
        s5 = gmsh.model.occ.addBSplineFilling(Side5, type="Stretch")
        s6 = gmsh.model.occ.addBSplineFilling(Side6, type="Stretch")

        # make a solid
        vol = gmsh.model.occ.addSurfaceLoop([s1, s2, s3, s4, s5, s6])

        gmsh.model.occ.synchronize()

        gmsh.model.occ.addVolume([vol])

        gmsh.model.occ.synchronize()

        # now add the straight section
        pp1 = gmsh.model.occ.addPoint(
            points_front_bottom[0, 0],
            points_front_bottom[0, 1],
            points_front_bottom[0, 2],
            targ_h,
        )

        pp2 = gmsh.model.occ.addPoint(
            points_front_top[0, 0],
            points_front_top[0, 1],
            points_front_top[0, 2],
            targ_h,
        )

        pp3 = gmsh.model.occ.addPoint(points_back_top[0, 0], points_back_top[0, 1], points_back_top[0, 2], targ_h)

        pp4 = gmsh.model.occ.addPoint(
            points_back_bottom[0, 0],
            points_back_bottom[0, 1],
            points_back_bottom[0, 2],
            targ_h,
        )

        gmsh.model.occ.synchronize()

        l1 = gmsh.model.occ.addLine(pp1, pp2)
        l2 = gmsh.model.occ.addLine(pp2, pp3)
        l3 = gmsh.model.occ.addLine(pp3, pp4)
        l4 = gmsh.model.occ.addLine(pp4, pp1)

        l5 = gmsh.model.occ.addLine(pp1, points_list_llc[0])
        l6 = gmsh.model.occ.addLine(pp2, points_list_lrc[0])
        l7 = gmsh.model.occ.addLine(pp3, points_list_urc[0])
        l8 = gmsh.model.occ.addLine(pp4, points_list_ulc[0])

        # the sides of the straight section
        c1 = gmsh.model.occ.addCurveLoop([l1, l2, l3, l4])
        ss1 = gmsh.model.occ.addSurfaceFilling(c1)

        c2 = gmsh.model.occ.addCurveLoop([l1, l6, C0_south, -l5])
        ss2 = gmsh.model.occ.addSurfaceFilling(c2)

        c3 = gmsh.model.occ.addCurveLoop([l2, l7, -C0_east, -l6])
        ss3 = gmsh.model.occ.addSurfaceFilling(c3)

        c4 = gmsh.model.occ.addCurveLoop([l3, l8, -C0_north, -l7])
        ss4 = gmsh.model.occ.addSurfaceFilling(c4)

        c5 = gmsh.model.occ.addCurveLoop([l4, l5, C0_west, -l8])
        ss5 = gmsh.model.occ.addSurfaceFilling(c5)

        # make a solid
        vol_s = gmsh.model.occ.addSurfaceLoop([ss1, ss2, ss3, ss4, ss5, s5])

        gmsh.model.occ.synchronize()
        gmsh.model.occ.addVolume([vol_s])
        gmsh.model.occ.synchronize()
        gmsh.model.occ.fuse([(3, vol)], [(3, vol_s)])
        gmsh.model.occ.synchronize()

        # clean up
        ent_2d = gmsh.model.getEntities(2)
        gmsh.model.occ.remove(ent_2d)
        ent_1d = gmsh.model.getEntities(1)
        gmsh.model.occ.remove(ent_1d)
        ent_0d = gmsh.model.getEntities(0)
        gmsh.model.occ.remove(ent_0d)

        gmsh.model.occ.synchronize()

    @optional_features
    def _create_central_post_geom(self, surface: WedgeSurface) -> None:
        """
        Create the inner post geometry for a given surface.

        Parameters:
        - surface: The surface object containing the lower and upper edge coordinates. (Surface)

        """
        self._make_endspacer(surface, z_back=None)

    @optional_features
    def _create_headspacer_geom(self, surface: WedgeSurface) -> None:
        """Create a Headspacer geometry for a given surface

        :param surface: The surface object containing lower and upper edge coordinates (Surface)
        :type surface: WedgeSurface
        """
        z_val = 0.0
        if surface.lower_edge[-1, 2] > 0:
            if self.max_z:
                z_val = self.max_z + self.add_z
            else:
                z_val = max(surface.lower_edge[-1, 2], surface.upper_edge[-1, 2]) + self.add_z
        else:
            if self.min_z:
                z_val = self.min_z - self.add_z
            else:
                z_val = min(surface.lower_edge[-1, 2], surface.upper_edge[-1, 2]) - self.add_z

        self._make_endspacer(surface, z_back=z_val)

    @optional_features
    def _create_wedge_geom(self, surface_inner: WedgeSurface, surface_outer: WedgeSurface) -> None:
        """
        Create a wedge geometry based on two input surfaces.

        Args:
            surface_inner (Surface): The inner surface of the wedge.
            surface_outer (Surface): The outer surface of the wedge.

        Returns:
            Solid: The generated wedge geometry.

        Raises:
            Exception: If the wedge could not be generated from the input surfaces.
        """
        points_front_bottom = surface_outer.lower_edge
        points_front_top = surface_outer.upper_edge
        points_back_bottom = surface_inner.lower_edge
        points_back_top = surface_inner.upper_edge
        self._make_wedge(points_front_bottom, points_front_top, points_back_bottom, points_back_top)

    @optional_features
    def _create_coil_geometry(self, coil: Coil3DGeometry) -> None:
        """
        Generate the geometry of a coil.

        :param coil: The 3D geometry of the coil.
        :type coil: Coil3DGeometry
        """
        nodes = coil.geometry.nodes

        self._make_wedge(nodes[::4, :], nodes[1::4, :], nodes[3::4, :], nodes[2::4, :])

    def get_coil_geom(self, coil: Coil3DGeometry) -> None:
        if not self.model_name:
            self.model_name = f"coil_{self._name_cntr}"
            self._name_cntr += 1
        self._create_coil_geometry(coil)

    def get_coil_block_geom(
        self,
        wedge_inner: WedgeGeometry,
        wedge_outer: WedgeGeometry,
    ) -> None:
        """Geometry for a coil block between two wedges

        :param wedge_inner: Wedge defining the inner geometry of the coil block
        :param wedge_outer: Wedge defining the outer geometry of the coil block
        :return: A cq.Workplane containing the generated cad data
        """
        surface_inner = wedge_inner.outer_surface
        surface_outer = wedge_outer.inner_surface
        if surface_inner is None:
            raise ValueError("Outer endspacer is missing inner surface for defining coil block")
        if surface_inner is None or surface_outer is None:
            raise ValueError("Inner endspacer is missing outer surface for defining coil block")
        if len(surface_inner.lower_edge) != len(surface_inner.upper_edge):
            raise ValueError("Wedge lower and upper surface with different number of points.")
        if len(surface_outer.lower_edge) != len(surface_outer.upper_edge):
            raise ValueError("Wedge lower and upper surface with different number of points.")
        if len(surface_inner.lower_edge) != len(surface_outer.lower_edge):
            raise ValueError("Different discretisation of inner and outer surface Cannot proceed.")

        if not self.model_name:
            self.model_name = f"coilblock_{self._name_cntr}"
            self._name_cntr += 1
        return self._create_wedge_geom(surface_inner, surface_outer)

    def get_wedge_geom(self, wedge: WedgeGeometry) -> None:
        """Geometry forWedge

        :param wedge: The wedge geometry object
        :return: A cq.Workplane containing the generated cad data
        """
        surface_inner = wedge.inner_surface
        surface_outer = wedge.outer_surface
        if surface_inner is None or surface_outer is None:
            raise ValueError("Cannot generate Wedge for wedge without both inner and outer surface defined")
        if len(surface_inner.lower_edge) != len(surface_inner.upper_edge):
            raise ValueError("Wedge lower and upper surface with different number of points.")
        if len(surface_outer.lower_edge) != len(surface_outer.upper_edge):
            raise ValueError("Wedge lower and upper surface with different number of points.")
        if len(surface_inner.lower_edge) != len(surface_outer.lower_edge):
            raise ValueError("Different discretisation of inner and outer surface Cannot proceed.")

        if not self.model_name:
            self.model_name = f"wedge_{self._name_cntr}"
            self._name_cntr += 1

        return self._create_wedge_geom(surface_inner, surface_outer)

    def get_central_post_geom(self, wedge: WedgeGeometry) -> None:
        """Return the geometry for an Inner post

        :param wedge: The wedge geometry object
        :return: A cq.Workplane containing the generated cad data
        """
        surface = wedge.outer_surface
        if surface is None:
            raise TypeError("Cannot generate Inner post for Wedge without outer surface")
        if len(surface.lower_edge) != len(surface.upper_edge):
            raise ValueError("Wedge lower and upper surface with different number of points.")

        if not self.model_name:
            self.model_name = f"central_post_{self._name_cntr}"
            self._name_cntr += 1

        return self._create_central_post_geom(surface)

    def get_headspacer_geom(self, wedge: WedgeGeometry) -> None:
        """Geometry for head spacer

        :param wedge: The wedge geometry object
        :return: A cq.Workplane containing the generated cad data
        """
        surface = wedge.inner_surface
        if surface is None:
            raise TypeError("Cannot generate Headspacer for wedge without inner surface")
        if len(surface.lower_edge) != len(surface.upper_edge):
            raise ValueError("Wedge lower and upper surface with different number of points.")

        if not self.model_name:
            self.model_name = f"headspacer_{self._name_cntr}"
            self._name_cntr += 1

        return self._create_headspacer_geom(surface)

    def get_endspacer_geom(self, wedge: WedgeGeometry) -> None:
        """Generate an Endspacer for the given geometry. This can be either a central post, a wedge, or a headspacer

        :param wedge: _description_
        :return: _description_
        """
        if wedge.inner_surface is None and wedge.outer_surface is None:
            raise TypeError("Cannot generate Endspacer for wedge without inner or outer surface defined")
        if wedge.inner_surface is None:
            return self.get_central_post_geom(wedge)
        if wedge.outer_surface is None:
            return self.get_headspacer_geom(wedge)

        return self.get_wedge_geom(wedge)

    def get_all_coil_geoms(self, coils: Dict[int, Coil3DGeometry]) -> None:
        """
        Generate the geometry of all coils.

        :param coils: The 3D geometry of the coils.
        :type coils: Dict[int, Coil3DGeometry]

        :return: The generated coil geometry.
        :rtype: List[cq.Shape]
        """
        for idx, coil in coils.items():
            self.logger.debug(f"Generating coil geometry for coil idx {idx}")
            self.model_name = f"coil_{idx}"
            self.get_coil_geom(coil)

    def get_all_coil_block_geoms(self, wedges: Dict[int, WedgeGeometry]) -> None:
        """
        Generate the geometry of all coil blocks.

        :param wedges: The 3D of all wedges
        :type coils: Dict[int, WedgeGeometry]

        :return: The generated coil geometry.
        :rtype: List[cq.Shape]
        """
        blocks = {}

        for wedge in wedges.values():
            for idx, blk in enumerate([wedge.block_inner, wedge.block_outer]):
                if blk == 0:
                    continue
                if blk not in blocks:
                    blocks[blk] = {0: None, 1: None}

                if blocks[blk][idx] is None:
                    blocks[blk][idx] = wedge
                else:
                    raise ValueError(f"Overwriting block {blk} wedge {idx}")
        for idx, block in blocks.items():
            self.logger.debug(f"Generating coil geometry for block idx {idx}")
            self.model_name = f"coilblock_{idx}"
            self.get_coil_block_geom(block[0], block[1])

    def get_all_endspacer_geoms(self, wedges: Dict[int, WedgeGeometry]) -> None:
        """
        Generate the geometry of all endspacers.

        :param wedges: The 3D of all wedges
        :type coils: Dict[int, WedgeGeometry]

        :return: The generated endspacer geometry.
        :rtype: List[cq.Shape]
        """
        name_cntr_tmp = self._name_cntr
        for idx, wedge in wedges.items():
            self.logger.debug(f"Generating endspacer geometry for endspacer idx {idx}")
            self._name_cntr = idx
            self.model_name = None  # Let geometry generate name
            self.get_endspacer_geom(wedge)
        self._name_cntr = name_cntr_tmp

    def get_from_parser(
        self,
        parser: RoxieOutputParser,
        opt_step=1,
        generate_endspacers=True,
        generate_coil_blocks=True,
        generate_conductors=True,
    ) -> None:
        """
        From a parsed roxie output, get CAD geometries for endspacers, coil blocks, and conductors.

        :param parser: (RoxieOutputParser) The parser object to retrieve geometries from.
        :param generate_endspacers: (bool) Whether to generate endspacers geometries. Defaults to True.
        :param generate_coil_blocks: (bool) Whether to generate coil block geometries. Defaults to True.
        :param generate_conductors: (bool) Whether to generate conductor geometries. Defaults to True.
        :param opt_step: (int) The optimization step number. Defaults to 1
        :return: (Tuple[Optional[List[cq.Shape]], Optional[List[cq.Shape]], Optional[List[cq.Shape]]])
                    A tuple containing three optional lists of geometries: endspacers, coil_blocks, and conductors.
        """
        if generate_endspacers:
            self.get_all_endspacer_geoms(parser.opt[opt_step].wedgeGeometries3D)
        if generate_coil_blocks:
            self.get_all_coil_block_geoms(parser.opt[opt_step].wedgeGeometries3D)
        if generate_conductors:
            self.get_all_coil_geoms(parser.opt[opt_step].coilGeometries3D)
