# SPDX-FileCopyrightText: 2024 CERN
#
# SPDX-License-Identifier: BSD-4-Clause

import gmsh
import numpy as np


def read_mesh_2D(mesh):
    """Based on a gmsh surfacer mesh object get the mesh connectivity and nodes

    :param mesh:
        A gmsh mesh object.

    :param vol_tag:
        The volume tag. Default = -1 i.e. all volumes are taken.

    :return:
        The nodal coordinates and the connectivity.
        Also return the boundary nodes list.
    """
    # get the element info
    elementTypes, elementTags, elementNodes = mesh.getElements(dim=2)

    # get node connectivity
    elementNodes = np.array(elementNodes[0], dtype=np.int32)

    # dependent on the element type, determine the number of nodes per element
    if elementTypes[0] == 2:
        num_nodes_per_element = 3
    else:
        print(f"gmsh surface element type {elementTypes[0]} is unknown!")

    # the number of elements
    num_el = np.int32(len(elementNodes) / num_nodes_per_element)

    # reshape
    elementNodes.shape = (num_el, num_nodes_per_element)

    # we get all the nodes that are specified in the model
    node_tags_all, p_all, parametric_all = mesh.getNodes()

    # this is how many nodes there are in total
    num_nodes_all = len(node_tags_all)

    # these are all the nodes in the model
    p_all.shape = (num_nodes_all, 3)
    # they are not sorted correctly
    index_table = np.zeros((num_nodes_all, 2), dtype=np.int32)
    index_table[:, 0] = node_tags_all
    index_table[:, 1] = np.linspace(0, num_nodes_all - 1, num_nodes_all)
    index_table = index_table[np.argsort(index_table[:, 0]), :]

    # print('In total there are {} nodes.'.format(num_nodes_all))

    # this function gives us all the nodes for all brick elements
    # they are in the same order as the element nodes returned by getElements
    # so they are not unique.
    node_tags, node_coords, parametric_coords = mesh.getNodesByElementType(elementTypes[0], -1)

    # the node tags are repeated so we get a unique list
    unique_node_tags = np.unique(node_tags)

    node_coords.shape = (len(node_tags), 3)

    # we determine the number of nodes from the unique list of node tags
    num_nodes = len(np.unique(node_tags))

    # print('There are {} nodes in the hexahedral mesh.'.format(num_nodes))

    # we now make an array of unique mesh nodes.
    p = np.zeros((num_nodes, 3))

    for i in range(num_nodes):
        p[i, :] = mesh.getNode(unique_node_tags[i])[0]
        # p[i, :] = p_all[index_table[i, 1], :]

    # we now need to translate the connectivity
    # we first copy the old table
    c = elementNodes.copy()

    # we now iterate over the elements
    for i, ee in enumerate(elementNodes):
        for j in range(num_nodes_per_element):
            c[i, j] = np.where(unique_node_tags == ee[j])[0]

    return p, c


def read_mesh_3D(mesh, vol_tag=-1):
    """Based on a gmsh mesh object get the mesh connectivity and nodes

    :param mesh:
        A gmsh mesh object.

    :param vol_tag:
        The volume tag. Default = -1 i.e. all volumes are taken.

    :return:
        The nodal coordinates and the connectivity.
        Also return the boundary nodes list.
    """
    # get the element info
    elementTypes, elementTags, elementNodes = mesh.getElements(dim=3, tag=vol_tag)

    # get node connectivity
    elementNodes = np.array(elementNodes[0], dtype=np.int32)

    # dependent on the element type, determine the number of nodes per element
    if elementTypes[0] == 4:
        num_nodes_per_element = 4
    elif elementTypes[0] == 5:
        num_nodes_per_element = 8
    elif elementTypes[0] == 12:
        num_nodes_per_element = 27
    elif elementTypes[0] == 17:
        num_nodes_per_element = 20
    elif elementTypes[0] == 93:
        num_nodes_per_element = 64
    elif elementTypes[0] == 99:
        num_nodes_per_element = 32
    else:
        print(f"gmsh element type {elementTypes[0]} is unknown!")

    # the number of elements
    num_el = np.int32(len(elementNodes) / num_nodes_per_element)

    # reshape
    elementNodes.shape = (num_el, num_nodes_per_element)

    # we get all the nodes that are specified in the model
    node_tags_all, p_all, parametric_all = mesh.getNodes()

    # this is how many nodes there are in total
    num_nodes_all = len(node_tags_all)

    # these are all the nodes in the model
    p_all.shape = (num_nodes_all, 3)
    # they are not sorted correctly
    index_table = np.zeros((num_nodes_all, 2), dtype=np.int32)
    index_table[:, 0] = node_tags_all
    index_table[:, 1] = np.linspace(0, num_nodes_all - 1, num_nodes_all)
    index_table = index_table[np.argsort(index_table[:, 0]), :]

    # print('In total there are {} nodes.'.format(num_nodes_all))

    # this function gives us all the nodes for all brick elements
    # they are in the same order as the element nodes returned by getElements
    # so they are not unique.
    node_tags, node_coords, parametric_coords = mesh.getNodesByElementType(elementTypes[0], -1)

    # the node tags are repeated so we get a unique list
    unique_node_tags = np.unique(node_tags)

    node_coords.shape = (len(node_tags), 3)

    # we determine the number of nodes from the unique list of node tags
    num_nodes = len(np.unique(node_tags))

    # print('There are {} nodes in the hexahedral mesh.'.format(num_nodes))

    # we now make an array of unique mesh nodes.
    p = np.zeros((num_nodes, 3))

    for i in range(num_nodes):
        p[i, :] = mesh.getNode(unique_node_tags[i])[0]
        # p[i, :] = p_all[index_table[i, 1], :]

    # we now need to translate the connectivity
    # we first copy the old table
    c = elementNodes.copy()

    # we now iterate over the elements
    for i, ee in enumerate(elementNodes):
        for j in range(num_nodes_per_element):
            c[i, j] = np.where(unique_node_tags == ee[j])[0]

    # we now get the boundary node information
    boundary_tags = gmsh.model.getBoundary([(3, -1)])

    b_node_tags, b_node_coords, b_parametric_coords = gmsh.model.mesh.getNodes(
        boundary_tags[0][0], boundary_tags[0][1], includeBoundary=True
    )

    b_node_coords.shape = (len(b_node_tags), 3)

    boundary_nodes = []

    # HERE we need to improve! I could not get
    # it running without comparing the node coordinates
    # something with the sorting is extremely cumbersome
    # we need again to translate them
    for i in range(len(b_node_tags)):
        # difference to my points
        difference = p.copy()

        difference[:, 0] -= b_node_coords[i, 0]
        difference[:, 1] -= b_node_coords[i, 1]
        difference[:, 2] -= b_node_coords[i, 2]

        # distance
        distance = np.sqrt(np.sum(difference**2, axis=1))

        boundary_nodes.append(np.argmin(distance))

        # find the node
        # node_number = np.where(unique_node_tags == bb)[0]
        # if len(node_number) == 1:
        #     boundary_nodes.append(node_number[0])

    boundary_nodes = np.unique(boundary_nodes)

    return p, c, boundary_nodes, b_node_coords, p_all
