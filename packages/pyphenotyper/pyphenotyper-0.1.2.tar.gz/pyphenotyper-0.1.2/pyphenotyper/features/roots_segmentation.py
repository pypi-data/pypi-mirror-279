import math
import os
import warnings
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple, Union, Optional

import cv2
import networkx as nx
import numpy as np
import pandas as pd
import skan
import skimage
from rich.progress import track
from skan import Skeleton, summarize

import pyphenotyper.features.rsml as rsml
from pyphenotyper.logger_config import logger


def load_in_mask(path: str) -> Optional[np.ndarray]:
    """
    This function takes in a path to the mask, loads it in, segments it, removes all the object that are smaller than
    an average area of all segmented instances, transfers the image back to BGR
    :param path: Path to the mask image.
    :type path: str
    :return: Loaded in mask image with root segmentation in BGR format.
    :rtype: np.ndarray
    """
    # Check if the path is a string
    if not isinstance(path, str):
        warnings.warn(
            f"Expected 'path' to be a string, but got {type(path).__name__}.")
        return None
    # Read the mask
    mask = cv2.imread(path, 0)
    if mask is None:
        raise ValueError(f"Could not read the image at {path}")
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    return mask


def load_in_seedlings_template(template_path: str) -> Optional[np.ndarray]:
    """
    This function loads in the template with the seed positions
    :param template_path: Path to the template image with seed positions.
    :type template_path: str
    :return: Loaded template image with seed positions.
    :rtype: np.ndarray
    """
    # Check if the path is a string
    if not isinstance(template_path, str):
        warnings.warn(
            f"Expected 'path' to be a string, but got {type(template_path).__name__}.")
        return None
    template = cv2.imread(template_path, 0)
    if template is None:
        raise ValueError(f"Could not read the image at {template_path}")
    return template


def get_plants_bboxes(path: str, template_path: str) -> List[List[int]]:
    """
    This function takes in the paths to the images, finds and returns the bounding boxes for each seed possible position
    :param path: Path to a mask image.
    :type path: str
    :param template_path: Path to the template image with seed positions.
    :type template_path: str
    :return: Array with the y, y_max, x, x_max coordinates that represent the bounding
             boxes for each seed possible position.
    :rtype: List[List[int]]
    """
    # load in images
    mask = load_in_mask(path)
    template = load_in_seedlings_template(template_path)
    # resize and prepare the template
    mask_seeding_position = cv2.resize(
        template, (mask.shape[1], mask.shape[0]))
    mask_seeding_position[mask_seeding_position < 200] = 0
    mask_seeding_position[mask_seeding_position != 0] = 255
    # segment the template to get the bounding boxes for each seed position
    mask_seeding_position_label = skimage.measure.label(
        mask_seeding_position).astype('uint8')
    _, template_segmented, stats, _ = cv2.connectedComponentsWithStats(
        mask_seeding_position_label)
    plants = []
    stats = stats[1::]

    # loop through all the stats, get coordinates, transform them into y, y_max, x, x_max and append to an array

    for j in range(len(stats)):
        if j == len(stats[1::]):
            point = stats[j][0] + stats[j][2]
        else:
            point = stats[j][0] + stats[j][2] + int((stats[j + 1][0] - stats[j][0] - stats[j][2]) / 2)
        plants.append([stats[j][1], stats[j][1] + stats[j][3], stats[j][0], point])
    return plants


def determine_starting_nodes(branch: pd.DataFrame) -> List[int]:
    """
    Determines all the starting points in the branch
    :param branch: DataFrame summarizing the skeleton of the branch with columns 'node-id-src' and 'node-id-dst'.
    :type branch: pd.DataFrame
    :return: List of node IDs that are starting points.
    :rtype: List[int]
    """
    # get uniques src and dst nodes
    src_nodes = branch['node-id-src'].unique()
    dst_nodes = branch['node-id-dst'].unique()
    starting_nodes = []
    # loop through all src nodes if it's not in dst nodes -> append to starting nodes array
    for node in src_nodes:
        if node not in dst_nodes:
            starting_nodes.append(node)
    return starting_nodes


def getting_coords_for_starting_nodes(branch: pd.core.frame.DataFrame) -> List[Tuple[int, int]]:
    """
    Finds coordinates for all the starting nodes in the branch
    :param branch: DataFrame with all the branches in it (graph representation).
    :type branch: pd.DataFrame
    :return: List of tuples with starting nodes coordinates (y, x).
    :rtype: List[Tuple[int, int]]
    """
    starting_nodes_list = determine_starting_nodes(branch)
    start_nodes_coordinates = []
    for id in starting_nodes_list:
        x = branch[branch['node-id-src'] == id]['image-coord-src-1'].iloc[0]
        y = branch[branch['node-id-src'] == id]['image-coord-src-0'].iloc[0]
        start_nodes_coordinates.append((y, x))
    return start_nodes_coordinates


def map_coords_to_node_ids(coordinates: List[Tuple[int, int]], branch: pd.DataFrame) -> List[int]:
    """
    Map coordinates to node IDs.
    This function takes a list of coordinates and a DataFrame representing
    a branch, and maps each coordinate to its corresponding node ID.
    :param coordinates: List of coordinates (y, x).
    :type coordinates: List[Tuple[int, int]]
    :param branch: DataFrame with all the branches in it (graph representation).
    :type branch: pd.DataFrame
    :return: List of node IDs corresponding to the provided coordinates.
    :rtype: List[int]
    """
    node_ids = []
    for y, x in coordinates:
        if len(branch[(branch['image-coord-src-1'] == x) & (branch['image-coord-src-0'] == y)]['node-id-src']) != 0:
            node_ids.append(
                branch[(branch['image-coord-src-1'] == x) & (branch['image-coord-src-0'] == y)]['node-id-src'].iloc[0])
    return node_ids


def can_be_skeletonized(image: np.ndarray) -> bool:
    """
    Check if there is at least one connected component of two or more pixels in the given image, to determine if it
    can be skeletonized or not.

    :param image: A numpy array representing the image.
    :type image: np.ndarray
    :return: True if there is a connected component of two or more pixels (can be skeletonized), False otherwise.
    :rtype: bool
    """
    rows, cols = image.shape
    visited = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def bfs(start: Tuple[int, int]) -> bool:
        """
        Perform Breadth-First Search (BFS) to check for connected pixels with value 1.

        :param start: The starting pixel coordinates.
        :return: True if a connected component of two or more pixels is found, False otherwise.
        """
        queue = deque([start])
        visited.add(start)
        component_size = 0

        while queue:
            x, y = queue.popleft()
            component_size += 1
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
                    if image[nx, ny] == 1:
                        visited.add((nx, ny))
                        queue.append((nx, ny))

        # Check if the component size is 2 or more
        return component_size > 1

    for i in range(rows):
        for j in range(cols):
            if image[i, j] == 1 and (i, j) not in visited:
                if bfs((i, j)):
                    return True

    return False


def process_plant(plant: Tuple[int, int, int, int], img: np.ndarray, starts_c: List[Tuple[int, int, int]],
                  n: int) -> None:
    """
    Process a single plant to find the most central starting node.
    :param plant: Bounding box coordinates of the plant (y1, y2, x1, x2).
    :type plant: Tuple[int, int, int, int]
    :param img: Image array.
    :type img: np.ndarray
    :param starts_c: List to store the starting node coordinates and distance for each plant.
    :type starts_c: List[Tuple[int, int, int]]
    :param n: Index of the current plant.
    :type n: int
    """
    subset = img[plant[0]:plant[1], plant[2]:plant[3]]
    subset_elements = img[plant[0]:, plant[2]:plant[3]]
    subset_gray = cv2.cvtColor(subset, cv2.COLOR_BGR2GRAY)
    subset_elements_gray = cv2.cvtColor(subset_elements, cv2.COLOR_BGR2GRAY)
    subset_bin = ((subset_gray > 0) * 1).astype('uint8')
    subset_elements_bin = ((subset_elements_gray > 0) * 1).astype('uint8')
    subset_skeleton = skimage.morphology.skeletonize(subset_bin)
    subset_elements_skeleton = skimage.morphology.skeletonize(
        subset_elements_bin)
    if len(np.unique(subset_skeleton)) > 1 and can_be_skeletonized(subset_skeleton):
        subset_skeleton_ob = Skeleton(subset_skeleton)
        subset_branch = summarize(subset_skeleton_ob)
        subset_skeleton_elem_ob = Skeleton(subset_elements_skeleton)
        subset_elem_branch = summarize(subset_skeleton_elem_ob)
        G = nx.from_pandas_edgelist(subset_elem_branch, source='node-id-src', target='node-id-dst',
                                    edge_attr='branch-distance')
        starting_nodes_coordinates = getting_coords_for_starting_nodes(
            subset_branch)
        node_ids_mapped = map_coords_to_node_ids(
            starting_nodes_coordinates, subset_elem_branch)
        y_start, x_start = 0, 0
        max_number_of_elements = -1
        for k in range(len(node_ids_mapped)):
            current_node = node_ids_mapped[k]
            last_element = sorted(
                nx.node_connected_component(G, current_node))[-1]
            if last_element - current_node > max_number_of_elements:
                y_start, x_start = starting_nodes_coordinates[k]
                max_number_of_elements = last_element - current_node
        starts_c[n] = (x_start, y_start, 0)


def get_most_central_starting_node_for_each_plant(path: str, template_path: str) -> \
        List[Tuple[int, int, int]]:
    """
    Get the most central starting node for each plant.
    This function identifies all starting nodes for each plant, determines the one closest to
    the center of the bounding box for each plant, and appends its coordinates and distance to the center.
    :param path: Path to the mask image.
    :type path: str
    :param template_path: Path to the template image with seed positions.
    :type template_path: str
    :return: List of tuples with the x, y coordinates and distance to the center of the bounding box
             for seed location of each plant.
    :rtype: List[Tuple[int, int, int]]
    """
    img = load_in_mask(path)
    plants = get_plants_bboxes(path, template_path)
    number_of_plants = len(plants)
    starts_c = [(0, 0, 0)] * number_of_plants
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_plant, plant, img, starts_c, n)
                   for n, plant in enumerate(plants)]
        for future in futures:
            future.result()
    return starts_c


def determine_primary_roots_locations(path: str, template_path: str) -> List[List[int]]:
    """
    Based on the location of the bounding boxes in which the seeds are located,
    get a slice of the mask where the primary root is supposed to be
    (x min : x max, y min : bottom of the image) and return the coordinates.
    :param path: Path to the mask image.
    :type path: str
    :param template_path: Path to the template image with seed positions.
    :type template_path: str
    :return: List of coordinates [y1, x1, x_right_bound] for each plant.
    :rtype: List[List[int]]
    """
    primary_roots_locations = []
    # get the bounding boxes where seeds can be located for each plant
    plants = get_plants_bboxes(path, template_path)
    # loop through all the bounding boxes
    for i in range(1, len(plants) + 1):
        if i < len(plants):
            # get the coordinates of the previous plant bounding box
            y1, y2, x1, x2 = plants[i - 1]
            # get the coordinates of the current plant bounding box ( only right bound is needed to find the slice
            # that is needed)
            _, _, x_right_bound, _ = plants[i]
            # append the coordinates to the array (the right bound for each plant is the starting coordinate for the
            # next plant -> width slice = from start point of the n's plant to start of the n + 1 plant )
            primary_roots_locations.append([y1, x1, x_right_bound])
        # if it's the last plant the right bound is the right bound of its bounding box
        elif i == len(plants):
            y1, y2, x1, x2 = plants[i - 1]
            primary_roots_locations.append([y1, x1, x2])
    return primary_roots_locations


def map_root_to(coordinates: Tuple[int, int], plant_num: int, branch: pd.DataFrame,
                offset_y: int, offset_x: int, root_type: str, target: float) -> pd.DataFrame:
    """
    Map root to a specific plant and root type based on coordinates and offset.
    :param coordinates: Coordinates to map (y, x).
    :type coordinates: Tuple[int, int]
    :param plant_num: Plant number to which the root belongs.
    :type plant_num: int
    :param branch: DataFrame containing branch information.
    :type branch: pd.DataFrame
    :param offset_y: Y offset to add to the coordinates.
    :type offset_y: int
    :param offset_x: X offset to add to the coordinates.
    :type offset_x: int
    :param root_type: Type of the root to map.
    :type root_type: str
    :param target: Target branch distance.
    :type target: float
    :return: Updated DataFrame with mapped root information.
    :rtype: pd.DataFrame
    """
    condition_1 = (
            (branch['image-coord-dst-0'] == coordinates[0] + offset_y) &
            (branch['image-coord-dst-1'] == coordinates[1] + offset_x) &
            (branch['branch-distance'] == target)
    )
    branch.loc[condition_1, 'root_type'] = root_type
    branch.loc[condition_1, 'plant'] = plant_num
    return branch


def are_consecutive(lst: List[int], num1: np.int32, num2: np.int32) -> bool:
    """
    Determine if two numbers appear consecutively in the list.
    This function iterates through the list, checking if num1 is immediately followed by num2 at any position.
    If such a pair is found, the function returns True, indicating that num1 and num2 are consecutive in the list.
    If the list does not contain num1 followed directly by num2, the function returns False.
    :param lst: The list of elements to be checked. The elements should be of a type that supports comparison.
    :type lst: List[int]
    :param num1: The first number to check for consecutiveness.
    :type num1: np.int32
    :param num2: The second number to check for consecutiveness.
    :type num2: np.int32
    :return: True if num1 is immediately followed by num2 in the list, otherwise False.
    :rtype: bool
    :example:
    >>> are_consecutive([1, 2, 3, 4, 5], 2, 3)
    True
    >>> are_consecutive([1, 2, 4, 5], 3, 4)
    False
    """
    for i in range(len(lst) - 1):
        if lst[i] == num1 and lst[i + 1] == num2:
            return True
    return False


def prepare_data_for_segmentation(path: str, template_path: str) -> List[np.ndarray]:
    """
    Prepare all the data for the segmentation.
    This function prepares the following data for segmentation:
        - primary_root_locations: array with the coordinates to slice the image and focus on each plant's primary root
        - start_node_coordinates: array with the coordinates of the most central starting nodes for each plant
        - plant_bboxes: bounding boxes representing the possible locations for seeds for each plant
        - connected_mask: mask where all the starting nodes that are close enough to the central node for each plant are connected
    :param path: Path to the mask image.
    :type path: str
    :param template_path: Path to the template image with seed positions.
    :type template_path: str
    :return: List containing primary_root, skeleton, primary_root_locations, start_node_coordinates,
             plant_bboxes, and connected_mask.
    :rtype: List[np.ndarray]
    """
    # Get the coordinates that are used to slice the image and focus on each primary root
    primary_roots_locations = determine_primary_roots_locations(
        path, template_path)
    # Transform mask to binary for a more accurate skeleton
    mask = load_in_mask(path)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    mask = ((mask > 0) * 1).astype('uint8')
    # Get the starting node that is the part of the largest skeleton in the selected area representing the possible
    # seed location
    start_node_coordinates = get_most_central_starting_node_for_each_plant(
        path, template_path)
    # Get bounding boxes for each plant's possible seed location
    plants_bboxes = get_plants_bboxes(path, template_path)
    return [primary_roots_locations, start_node_coordinates, plants_bboxes, mask]


def adjust_size(mask: np.ndarray, slice_boundaries: Tuple[int, int, int], start_x: np.int64, start_y: np.int64,
                left: int, right: int, edge_tolerance: int = 150) -> \
        Union[List[Union[int, str]], List[Union[int, pd.DataFrame, object, np.ndarray]]]:
    """
    Adjust the size of the mask based on slice boundaries and edge tolerance.
    This function slices the mask based on provided boundaries and edge tolerance, skeletonizes
    the subset, and returns various properties including the last node,
    the branch DataFrame, the skeleton object, the mask subset, the adjusted start coordinates,
    the start node ID, the distance, and the graph.
    :param mask: The mask image.
    :type mask: np.ndarray
    :param slice_boundaries: List containing the y_min, x_min, and x_max boundaries for slicing.
    :type slice_boundaries: List[int]
    :param start_x: The x-coordinate of the starting point.
    :type start_x: np.int64
    :param start_y: The y-coordinate of the starting point.
    :type start_y: np.int64
    :param left: The left edge tolerance factor.
    :type left: int
    :param right: The right edge tolerance factor.
    :type right: int
    :param edge_tolerance: The edge tolerance for slicing, default is 150.
    :type edge_tolerance: int
    :return: List containing the last node, the branch DataFrame, the skeleton object, the mask subset,
             the adjusted start x-coordinate, the start node ID, the distance, and the graph.
             Returns ['error'] if the start node ID cannot be found.
    :rtype: Union[List[Union[int, str]], List[Union[int, pd.DataFrame, skan.csr.Skeleton, np.ndarray]]]
    """
    mask_subset = mask[
                  slice_boundaries[0]::,
                  slice_boundaries[1] - edge_tolerance * left:slice_boundaries[2] + edge_tolerance * right]
    mask_subset_skeleton = skimage.morphology.skeletonize(mask_subset)
    mask_subset_skeleton_ob = Skeleton(mask_subset_skeleton)
    mask_subset_branch = summarize(mask_subset_skeleton_ob)
    start_x += edge_tolerance * left
    unique_last_nodes = mask_subset_branch['node-id-dst'].unique()[::-1]
    end_points = []
    for item in unique_last_nodes:
        if item not in mask_subset_branch['node-id-src'].unique():
            end_points.append(item)
    if len(mask_subset_branch[(mask_subset_branch['image-coord-src-0'] == start_y) & (
            mask_subset_branch['image-coord-src-1'] == start_x)]['node-id-src']) == 0:
        return ['error']
    start_node_id = mask_subset_branch[
        (mask_subset_branch['image-coord-src-0'] == start_y) & (mask_subset_branch['image-coord-src-1'] == start_x)][
        'node-id-src'].iloc[0]
    G = nx.from_pandas_edgelist(mask_subset_branch, source='node-id-src', target='node-id-dst',
                                edge_attr='branch-distance')
    # get the last node - assume that it's the tip of the primary root for now
    last_node = max(G.nodes())
    # sort the nodes list to go from bottom to top
    un_sorted_nodes = list(G.nodes())
    sorted_nodes = sorted(un_sorted_nodes)
    # index for current node
    node_count = -1
    distance = 0
    while distance == 0:
        node_count -= 1
        if nx.has_path(G, start_node_id, last_node):
            distance = nx.dijkstra_path_length(
                G, start_node_id, last_node, weight='branch-distance')
        else:
            last_node = sorted_nodes[node_count]
    distance = nx.dijkstra_path_length(
        G, start_node_id, last_node, weight='branch-distance')
    return [last_node, mask_subset_branch, mask_subset_skeleton_ob, mask_subset, start_x, start_node_id, distance, G]


def locate_tip_of_root(graph: nx.classes.graph.Graph, start_node_id: int) -> Tuple[int, float]:
    """
    Locates the tip of the root by finding the farthest node from the starting node in a graph.
    :param graph: The graph representing the root structure.
    :type graph: nx.Graph
    :param start_node_id: The identifier of the starting node.
    :type start_node_id: int
    :return: A tuple containing the identifier of the last node (assumed tip of the primary root) and the distance to it.
    :rtype: Tuple[int, float]
    """
    # Get the last node - assume that it's the tip of the primary root for now
    last_node = max(graph.nodes())
    # Sort the nodes list to go from bottom to top
    un_sorted_nodes = list(graph.nodes())
    sorted_nodes = sorted(un_sorted_nodes)
    # Index for current node
    node_count = -1
    distance = 0
    # While distance is 0, loop through all nodes to find the first that is connected to the starting node and save the distance
    while distance == 0:
        node_count -= 1
        if nx.has_path(graph, start_node_id, last_node):
            distance = nx.dijkstra_path_length(
                graph, start_node_id, last_node, weight='branch-distance')
        else:
            last_node = sorted_nodes[node_count]
    return last_node, distance


def small_protrusions(row: pd.DataFrame, next_row: pd.DataFrame, mask_full_branch: pd.DataFrame, plant_num: int,
                      offset_y: int, offset_x: int) -> Tuple[pd.DataFrame, bool, bool]:
    """
    Eliminates small protrusions by mapping roots to the mask based on branch distances.
    :param row: The current data row containing node and coordinate information.
    :type row: pd.DataFrame
    :param next_row: The next data row containing node and coordinate information, or None if there is no next row.
    :type next_row: pd.DataFrame
    :param mask_full_branch: The full branch mask data, whose type is dependent on the specific application.
    :type mask_full_branch: Any
    :param plant_num: The identifier number for the plant.
    :type plant_num: int
    :param offset_y: The offset value for the y-coordinate.
    :type offset_y: int
    :param offset_x: The offset value for the x-coordinate.
    :type offset_x: int
    :return: A tuple containing the updated mask for the full branch, a boolean indicating if the protrusion was small and mapped, and a boolean indicating if the nodes were consecutive.
    :rtype: Tuple[pd.DataFrame, bool, bool]
    """
    if next_row is not None:
        if row["node-id-src"] == next_row["node-id-src"] and row["node-id-dst"] == next_row["node-id-dst"]:
            if next_row["branch-distance"] > row["branch-distance"]:
                y = row['image-coord-dst-0']
                x = row['image-coord-dst-1']
                distance_current_row = row['branch-distance']
                mask_full_branch = map_root_to((y, x), plant_num, mask_full_branch, offset_y, offset_x,
                                               'Primary', distance_current_row)
                return mask_full_branch, True, True
            else:
                return mask_full_branch, False, True
    return mask_full_branch, False, False


def large_protruisions(row: pd.DataFrame, mask_full_branch: pd.DataFrame, plant_num: int, offset_y: int,
                       offset_x: int, last_duplicated: bool, path: List[int]) -> Tuple[pd.DataFrame, bool]:
    """
    Eliminates large protrusions by mapping roots to the mask based on the root path.
    :param row: A data row containing node and coordinate information.
    :type row: pd.DataFrame
    :param mask_full_branch: The full branch mask data, whose type is dependent on the specific application.
    :type mask_full_branch: pd.DataFrame
    :param plant_num: The identifier number for the plant.
    :type plant_num: int
    :param offset_y: The offset value for the y-coordinate.
    :type offset_y: int
    :param offset_x: The offset value for the x-coordinate.
    :type offset_x: int
    :param last_duplicated: The last duplicated node data, whose type is dependent on the specific application.
    :type last_duplicated: bool
    :param path: A list of node IDs representing the path.
    :type path: List[int]
    :return: A tuple containing the updated mask for the full branch and the last duplicated node data.
    :rtype: Tuple[pd.DataFrame, bool]
    """
    end_node = row["node-id-dst"]
    if end_node in path:
        consecutive = are_consecutive(
            path, row["node-id-src"], row["node-id-dst"])
        if consecutive:
            y = row['image-coord-dst-0']
            x = row['image-coord-dst-1']
            distance_current_row = row['branch-distance']
            mask_full_branch = map_root_to((y, x), plant_num, mask_full_branch, offset_y, offset_x,
                                           'Primary', distance_current_row)
    return mask_full_branch, last_duplicated


def eleminate_root_cut_off(mask: np.ndarray, plant: Tuple[int, int, int], start_x: int, start_y: int,
                           plant_num: int, x_last_node: int, offset_x: int) -> \
        Optional[Tuple[int, pd.DataFrame, skan.csr.Skeleton, np.ndarray, int, int, int, nx.classes.graph.Graph, int]]:
    """
    Adjusts the mask and plant parameters to eliminate root cut-off issues by modifying offsets.

    :param mask: The mask data, whose type is dependent on the specific application.
    :type mask: np.ndarray
    :param plant: A tuple representing plant parameters. Expected to contain (plant_id, plant_left, plant_right).
    :type plant: Tuple[int, int, int]
    :param start_x: The starting x-coordinate for the adjustment process.
    :type start_x: int
    :param start_y: The starting y-coordinate for the adjustment process.
    :type start_y: int
    :param plant_num: The identifier number for the plant.
    :type plant_num: int
    :param x_last_node: The x-coordinate of the last node.
    :type x_last_node: int
    :param offset_x: The offset value for the x-coordinate.
    :type offset_x: int
    :return: A tuple containing the last node, mask subsets, start x-coordinate, start node ID, distance, graph, and updated offset_x if adjustment was made. Otherwise, returns None.
    :rtype: Optional[Tuple[int, pd.DataFrame, skan.csr.Skeleton, np.ndarray, int, int, int, nx.classes.graph.Graph, int]]
    """
    # Define the adjustment parameters
    adjust_l, adjust_r = 0, 0
    if x_last_node + offset_x - 150 - plant[1] < 0:
        adjust_l = 1
    elif plant[2] - x_last_node - 150 - offset_x < 0:
        adjust_r = 1
    # Adjust size and update values if necessary
    if adjust_l or adjust_r:
        vals = adjust_size(mask, plant, start_x, start_y, adjust_l, adjust_r)
        if vals[0] != 'error':
            last_node, mask_subset_branch, mask_subset_skeleton_ob, mask_subset, start_x, start_node_id, distance, G = vals
            if adjust_l:
                offset_x -= 150
            return last_node, mask_subset_branch, mask_subset_skeleton_ob, mask_subset, start_x, start_node_id, distance, G, offset_x
    # Return default values if no adjustment is made
    return None


def segmentation(path: str, template_path: str) -> Optional[List]:
    """
    Segments root structures from an image based on a provided template.
    The function works through several steps:
    1. Preparing data: It first prepares the data by extracting necessary components like the root
       locations, bounding boxes, and mask of the root system.
    2. Processing each plant: For each detected plant, it processes subsets of the mask to identify
       root structures.
    3. Skeletonization: Applies skeletonization to simplify the root structures into minimal
       representations.
    4. Graph construction: Constructs a graph from the skeletonized image to represent the root
       structures.
    5. Path finding: Uses Dijkstra's algorithm to find the longest path in the graph, representing
       the primary root.
    6. Visualization: Draws the identified primary roots and updates the distances list.
    :param path: The file path to the image to be processed.
    :type path: str
    :param template_path: Path to the template image with seed positions.
    :type template_path: str
    :return: List containing the mask_full_branch DataFrame, and the mask_full_skeleton_ob object.
    :rtype: List
    """
    # prepare needed data
    primary_roots_locations, start_node_coordinates, plants_bboxes, mask = prepare_data_for_segmentation(
        path, template_path)
    full_skeleton = skimage.morphology.skeletonize(mask)
    if len(np.unique(full_skeleton)) == 1:
        warnings.warn(
            "Given mask is empty")
        return None

    else:
        mask_full_skeleton_ob = Skeleton(full_skeleton)
        mask_full_branch = summarize(mask_full_skeleton_ob)
        mask_full_branch['root_type'] = "None"
        mask_full_branch['plant'] = "None"

    # loop through all the primary roots locations
    for plant_num, plant in enumerate(primary_roots_locations):
        mask_subset = mask[plant[0]::, plant[1]:plant[2]]
        # skeletonize mask and get a branch
        mask_subset_skeleton = skimage.morphology.skeletonize(mask_subset)
        if len(np.unique(mask_subset_skeleton)) > 1 and can_be_skeletonized(mask_subset_skeleton):
            mask_subset_skeleton_ob = Skeleton(mask_subset_skeleton)
            mask_subset_branch = summarize(mask_subset_skeleton_ob)
            # get offset for the coordinates to visualise everything on the input image using the coordinates from
            # the slice
            offset_y, _, offset_x, _ = plants_bboxes[plant_num]
            # get the coordinates of the root start for the current plant
            start_x, start_y, _ = start_node_coordinates[plant_num]
            # if there is no such starting node present in the branch skip this plant
            if len(mask_subset_branch[(mask_subset_branch['image-coord-src-0'] == start_y) & (
                    mask_subset_branch['image-coord-src-1'] == start_x)]['node-id-src']) == 0:
                logger.info(
                    f'no starting nodes found for x - {start_x} y - {start_y}')
                continue
            # else get the node id by the y and x coordinates
            start_node_id = mask_subset_branch[(mask_subset_branch['image-coord-src-0'] == start_y) & (
                    mask_subset_branch['image-coord-src-1'] == start_x)]['node-id-src'].iloc[0]
            G = nx.from_pandas_edgelist(mask_subset_branch, source='node-id-src', target='node-id-dst',
                                        edge_attr='branch-distance')
            # get the tip of the root and distance to it
            last_node, distance = locate_tip_of_root(G, start_node_id)
            x_last_node = mask_subset_branch[mask_subset_branch['node-id-dst'] == last_node]['image-coord-src-1'].iloc[
                0]
            cut_off_check = eleminate_root_cut_off(
                mask, plant, start_x, start_y, plant_num, x_last_node, offset_x)
            if cut_off_check is not None:
                last_node, mask_subset_branch, mask_subset_skeleton_ob, mask_subset, start_x, start_node_id, distance, G, offset_x = cut_off_check
            if distance != 0:
                # get the shortest path from the starting point to the end point
                path = nx.dijkstra_path(
                    G, source=start_node_id, target=last_node, weight='branch-distance')
                # loop through the branch to visualise the root system and if the node is in the path viasualise it
                # as a primary root
                for i in range(len(mask_subset_branch)):
                    current_row = mask_subset_branch.iloc[i]
                    next_row = mask_subset_branch.iloc[i + 1] if i + 1 < len(mask_subset_branch) else None
                    mask_full_branch, last_duplicated, sp_present = small_protrusions(current_row, next_row,
                                                                                      mask_full_branch, plant_num,
                                                                                      offset_y, offset_x)
                    if sp_present or last_duplicated:
                        continue
                    mask_full_branch, last_duplicated = large_protruisions(current_row, mask_full_branch, plant_num,
                                                                           offset_y, offset_x, last_duplicated, path)
    return [mask_full_branch, mask_full_skeleton_ob]


def draw_root(
        coordinates: np.array,
        image: np.array,
        x_offset: float,
        y_offset: float,
        colour: list = (0, 0, 0),
        thickness: int = 1,
) -> np.array:
    """
    This function visualises the given coordinates on the image with the provided colour and thickness.
    :param coordinates: array of (y, x) coordinates that has to be visualised
    :param image: image for visualisation
    :param x_offset: left bound for the current plant - used to draw on the real image using the coordinates from the sliced image that focuses on a certain plant
    :param y_offset: top bound for the current plant - used to draw on the real image using the coordinates from the sliced image that focuses on a certain plant
    :param colour: colour with which to draw
    :param thickness: thickness of the line, with 1 being the default single pixel
    :return: returns image where the given coordinates are highlighted with the provided colour
    """
    # loop through all the coordinates pairs and visualise them
    for y, x in coordinates:
        y += y_offset
        x += x_offset
        # Make the lines a bit thicker so that they're more visible
        for i in range(-thickness, thickness + 1):
            for j in range(-thickness, thickness + 1):
                if 0 <= y + i < image.shape[0] and 0 <= x + j < image.shape[1]:
                    image[y + i, x + j] = colour
    return image


def get_closest_cord(subset_branch: pd.DataFrame, row: pd.DataFrame) -> pd.DataFrame:
    """
    Things function finds the closest branch to the given row, and returns the branch that has the closest angle to the given row.
    :param subset_branch: dataframe with all the branches.
    :param row: specific row of the dataframe with the branch information.
    :return: new_row: row of the dataframe with the branch information that has the closest angle to the given row. If no row is close to it, it returns an empty dataframe.
    """
    # Get the coordinates of the point
    point_x = row["image-coord-dst-1"]
    point_y = row["image-coord-dst-0"]
    # Get the angle of the row
    angle = row["angle"]
    # Set the distance for the closest branches
    threshold_distance = 45
    # Calculate the distance between the source point and all the other points
    src_distance = np.sqrt(
        (subset_branch["coord-src-1"] - point_x) ** 2
        + (subset_branch["coord-src-0"] - point_y) ** 2
    )
    # Filter the dataframe to the branches that are close to the source point, but not the same branch, and not the primary root.
    filtered_df = subset_branch[
        (
                ((src_distance <= threshold_distance))
                & ~(subset_branch["node-id-src"] == row["node-id-src"])
                & ~(subset_branch["node-id-dst"] == row["node-id-dst"])
        )
        & (subset_branch["root_type"] != "Primary")
        ]
    # If there are branches that are close to the source point, find the one with the closest angle to the given row.
    if not filtered_df.empty:
        new_row = filtered_df.iloc[(
                                           filtered_df["angle"] - angle).abs().argsort()[:1]]
        return new_row
    else:
        return pd.DataFrame()


def get_x_y(row: pd.DataFrame) -> Tuple[float, float, float, float]:
    """
    This function returns the start and destinations coordinates of a branch.
    :param row: row of the dataframe with the branch information.
    :return: x_src: x coordinate of the source point.
    :return: y_src: y coordinate of the source point.
    :return: x_dst: x coordinate of the destination point.
    :return: y_dst: y coordinate of the destination point.
    """
    x_src = row["image-coord-src-0"]
    y_src = row["image-coord-src-1"]
    x_dst = row["image-coord-dst-0"]
    y_dst = row["image-coord-dst-1"]
    return x_src, y_src, x_dst, y_dst


def calculate_angle(row: pd.DataFrame) -> float:
    """
    This function calculates the angle of a branch in degrees.
    :param row: row of the dataframe with the branch information.
    :return: angle_degrees: angle of the branch in degrees.
    """
    # Get the coordinates of the branch
    x1, y1, x2, y2 = get_x_y(row)
    # Calculate the angle of the branch
    delta_x = x2 - x1
    delta_y = y2 - y1
    # Calculate the angle in radians
    angle_radians = math.atan2(delta_y, delta_x)
    # Convert the angle to degrees
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees


def follow_lateral_path(subset_branch):
    """
    This function checks for each branch from the primary root, and follows the path of the lateral root.
    :param subset_branch: subset of the dataframe with all the branches. It should have an additional 'plant' and 'root_type' column, with primary roots marked as 'Primary' and the rest as 'None'.
    :return: subset_branch: dataframe with the roots assigned to the plants.
    """
    subset_branch_plant = subset_branch[subset_branch["plant"] != "None"]
    for plant in sorted(subset_branch_plant["plant"].unique()):
        # We convert the plant to an integer if it is not NaN
        if plant == "None" or np.isnan(plant):
            continue
        plant = int(plant)
        # Filter the dataframe to the current plant and only the primary roots
        filtered_df = subset_branch[subset_branch["plant"] == plant]
        filtered_df = filtered_df[filtered_df["root_type"] == "Primary"]

        root_id = 0

        # Iterate over the rows where the plant is the current plant and the root type is primary
        for index, row in filtered_df.iterrows():
            following_path = True
            # Reset the steps taken
            steps_taken = 0
            # Start from the primary root and follow the root path to the end.
            while following_path:
                # If it's the first step, so comming from the primary root, find the closest row to the primary root.
                if steps_taken == 0:
                    # Find the closest row to the primary root
                    closest_row = get_closest_cord(subset_branch, row)
                elif steps_taken > 10:
                    following_path = False
                    continue
                else:
                    # Find the closest row to the previous row
                    closest_row = get_closest_cord(subset_branch, closest_row)
                # Check if no closest row found, then stop following the path
                if closest_row.empty:
                    following_path = False
                    continue
                # Update the index and row with the closest one found
                index = closest_row.index[0]
                # Find the complete row in the original dataframe
                closest_row = subset_branch.loc[index]
                # Assign the plant to the closest row
                subset_branch.loc[index, "plant"] = plant
                subset_branch.loc[index, "root_type"] = "Lateral"
                subset_branch.loc[index, "root_id"] = f"Lateral_{root_id}"
                # Increment the steps taken
                steps_taken += 1
            root_id += 1
    return subset_branch


def assign_unassigned_branches(subset_branch: pd.DataFrame, subset_skeleton_ob_arr: Skeleton, img2: np.array,
                               colors: list = [(0, 128, 255), (240, 32, 160), (255, 0, 0), (255, 0, 255),
                                               (0, 255, 0)]) -> Tuple[pd.DataFrame, np.array]:
    """
    This function assigns the unassigned branches to the closest plant. It iterates over the rows where the plant is "None" and assigns the closest plant to the current row.
    :param subset_branch: subset of the dataframe with all the branches. It should have an additional 'plant' and 'root_type' column, with primary roots marked as 'Primary' and the rest as 'None'.
    :param subset_skeleton_ob_arr: skeleton object array of the image.
    :param colors: list of colors to draw the lateral roots with.
    :param img2: image off the petri dish to draw the roots on.
    :return: subset_branch: dataframe with the roots assigned to the plants.
    """
    # Filter the dataframe to the rows where the plant is "None".
    # This is the roots that have not been assigned to any plant yet.
    none_plants_df = subset_branch[subset_branch["plant"] == "None"]
    # Iterate over the rows where plant is "None"
    for index, row in none_plants_df.iterrows():
        # Initialize the minimum distance and the closest plant
        min_distance = np.inf
        # Initialize the closest index
        closest_plant = None

        closest_root_id = None
        # Coordinates of the source point
        src_x = row["image-coord-src-0"]
        src_y = row["image-coord-src-1"]
        # Find the closest point where plant is not "None"
        for target_index, target_row in subset_branch[
            subset_branch["root_id"] != "None"
        ].iterrows():
            # Coordinates of the destination point
            dst_x = target_row["image-coord-dst-0"]
            dst_y = target_row["image-coord-dst-1"]
            # Calculate the Euclidean distance
            distance = np.sqrt((src_x - dst_x) ** 2 + (src_y - dst_y) ** 2)
            # If the plant has a closer distance than the current minimum distance, update the minimum distance and the closest plant
            if distance < min_distance:
                min_distance = distance
                closest_plant = target_row["plant"]
                closest_root_id = target_row["root_id"]
                closest_index = target_index
        # Assign the closest plant to the current row
        subset_branch.at[index, "plant"] = closest_plant
        subset_branch.loc[index, "root_type"] = "Lateral"
        subset_branch.loc[index, "root_id"] = closest_root_id
        # Get the path coordinates and draw on the image
        if min_distance == np.inf or closest_plant is None:
            continue

        xy = subset_skeleton_ob_arr.path_coordinates(closest_index)
        img2 = draw_root(xy, img2, 0, 0, colors[int(closest_plant)])
    return subset_branch, img2


def draw_lateral(subset_branch: pd.DataFrame, subset_skeleton_ob_arr: Skeleton, img2: np.array,
                 colors: list = [(0, 128, 255), (240, 32, 160), (255, 0, 0), (255, 0, 255), (0, 255, 0)]) -> np.array:
    """
    This function draws the lateral roots on the image. It uses the subset_dataframe and draaws each cordinate of the lateral branches.
    :param subset_branch: subset of the dataframe with all the branches. It should have an additional 'plant' and 'root_type' column, with primary roots marked as 'Primary' and the rest as 'None'.
    :param subset_skeleton_ob_arr: skeleton object array of the image.
    :param img2: image off the petri dish to draw the roots on.
    :param colors: list of colors to draw the lateral roots with.
    :return: img2: image with the roots drawn on it.
    """
    # We look one more time over the dataframe, and draw all of the lateral roots on the image here.
    for index, row in subset_branch.iterrows():
        if row["root_type"] == "Primary" or row["plant"] is None or np.isnan(row["plant"]):
            continue
        xy = subset_skeleton_ob_arr.path_coordinates(index)
        img2 = draw_root(xy, img2, 0, 0, (colors[int(row["plant"])]))
    return img2


def get_lateral(
        subset_branch: pd.DataFrame, subset_skeleton_ob_arr: Skeleton, img: np.ndarray
) -> Tuple[np.array, pd.DataFrame]:
    """
    This function finds the lateral in the image pathwise. It follows all the roots comming from the primary root, and this way finds the path of the lateral root.
    If a root is not selected as a lateral, it is assigned to the closest primary root. If there is no primary root, the root is assigned to the closest root.
    The function returns the image with the roots drawn on it and the dataframe with the roots assigned to the plants.
    :param subset_branch: subset of the dataframe with all the branches. It should have an additional 'plant' and 'root_type' column, with primary roots marked as 'Primary' and the rest as 'None'.
    :param subset_skeleton_ob_arr: skeleton object array of the image.
    :param img: image off the petri dish to draw the roots on.
    :return: img2: image with the roots drawn on it.
    :return: subset_branch: dataframe with the roots assigned to the plants.
    """
    # Copy the image to draw on
    img2 = img.copy()
    # Calculate the angle of each branch
    subset_branch["angle"] = subset_branch.apply(calculate_angle, axis=1)
    subset_branch["root_id"] = "None"

    # Define the colors for the lateral roots
    colors = [(0, 128, 255), (240, 32, 160),
              (255, 0, 0), (255, 0, 255), (0, 255, 0)]
    subset_branch = follow_lateral_path(subset_branch)
    subset_branch, img2 = assign_unassigned_branches(
        subset_branch, subset_skeleton_ob_arr, img2, colors)

    img2 = draw_lateral(subset_branch, subset_skeleton_ob_arr, img2, colors)
    return img2, subset_branch


def apply_conversion_factor(number: float) -> float:
    """
    Apply the pixel to real-life conversion factor to a given number.
    :param number: The number to be converted.
    :return: The converted number.
    :example:
    >>> apply_conversion_factor(412)
    22.350813743218804
    """

    if not isinstance(number, (int, float)):
        raise TypeError("The input must be an integer or a float.")

    # The petri dish plate size in mm
    plate_size_mm = 150
    # The petri dish plate size in pixels
    plate_size_pixels = 2765
    # The conversion factor
    conversion_factor = plate_size_mm / plate_size_pixels
    return number * conversion_factor


def get_primary_landmarks(landmark_df):
    """
    Get the primary landmarks of the plant. These are the root top (starting of)
    and the root tip (ending of) the primary root. This function finds them by
    looking for the highest location of the primary root, and assumes that it's
    the top of the primary root. The lowest location of the primary root is
    assumed to be the tip of the primary root.

    :param landmark_df: The dataframe with the root information.
    :return: landmark_df_copy: The dataframe with the primary landmarks marked.
    """

    if not isinstance(landmark_df, pd.DataFrame):
        raise TypeError("The input must be a pandas DataFrame.")

    if len(landmark_df) == 0:
        return landmark_df

    # Make a copy of the dataframe because of SettingWithCopyWarning from pandas
    landmark_df_copy = landmark_df.copy()

    # Create subset with only primary root branches.
    primary_subset = landmark_df[landmark_df["root_type"] == "Primary"]

    # Find the primary root top by looking at the lowest node-id-src, which corresponds to the highest location of the primary root.
    primary_root_top_row = primary_subset.loc[primary_subset["node-id-src"].idxmin()]

    # Find the primary root tip by looking at the highest node-id-dst, which corresponds to the lowest location of the primary root.
    primary_root_tip_row = primary_subset.loc[primary_subset["node-id-dst"].idxmax()]

    # Change the landmark in the dataframe to the primary root tip and top.
    landmark_df_copy.loc[primary_root_tip_row.name, "landmark"] = "Primary_root_tip"
    landmark_df_copy.loc[primary_root_top_row.name, "landmark"] = "Primary_root_top"

    # cv2.circle(img, (primary_root_tip_row["image-coord-dst-1"], primary_root_tip_row["image-coord-dst-0"]), 10, (0, 0, 255), -1)
    # cv2.circle(img, (primary_root_top_row["image-coord-src-1"], primary_root_top_row["image-coord-src-0"]), 10, (255, 0, 255), -1)

    return landmark_df_copy


def get_lateral_landmarks(landmark_df):
    """
    Get the lateral landmarks of the plant. These are the ending of all the lateral roots.
    This function finds them by looking if the ending of each branch is not the starting of any other branch.
    Since sometimes lateral roots are not connected, it can give false landmarks. That's why, when the lateral root is not connected to the primary root, it's excluded.

    :param landmark_df: The dataframe with the root information.
    :return: landmark_df_copy: The dataframe with the lateral landmarks marked.
    """

    if not isinstance(landmark_df, pd.DataFrame):
        raise TypeError("The input must be a pandas DataFrame.")

    if len(landmark_df) == 0:
        return landmark_df

    # Make a copy of the dataframe because of SettingWithCopyWarning from pandas
    landmark_df_copy = landmark_df.copy()
    # Create subset with only lateral root branches.
    lateral_subset = landmark_df[landmark_df["root_type"] == "Lateral"]
    # Get the primary skeleton id
    primary_skeleton_id = landmark_df[landmark_df["root_type"] == "Primary"]["skeleton-id"].iloc[0]

    # Loop through each row in the lateral subset, and check if the ending of the branch is not the starting of any other branch.
    # Also checking if the lateral root is connected to the primary root.
    for index, row in lateral_subset.iterrows():
        if not landmark_df["node-id-src"].isin([row["node-id-dst"]]).any() and \
                row["skeleton-id"] == primary_skeleton_id:
            landmark_df_copy.loc[index, "landmark"] = "Lateral_root_tip"
            # cv2.circle(img, (row["image-coord-dst-1"], row["image-coord-dst-0"]), 10, (0, 255, 0), -1)

    return landmark_df_copy


def process_landmark_df(landmark_df):
    """
    This function processes the landmark dataframe to clean it up and only get the important things.
    It removes all "None", and renames the columns to "x" and "y".
    It also sorts the dataframe by the landmark name, and resets the index.

    :param landmark_df: The dataframe with the root information.
    :return: landmark_df_processed: The processed dataframe with the landmarks.
    """
    if not isinstance(landmark_df, pd.DataFrame):
        raise TypeError("The input must be a pandas DataFrame.")
    if len(landmark_df) == 0:
        return landmark_df
    # Remove all "None" branches, since these are not of value.
    landmark_df = landmark_df[landmark_df["landmark"] != "None"]
    # Drop all rows with NaN values
    landmark_df = landmark_df.dropna()

    if len(landmark_df) == 0:
        return landmark_df
    # Remove the primary root top, because for this one we need source points. We add it later.
    landmark_df_processed = landmark_df[landmark_df["landmark"] != "Primary_root_top"]

    # Only keep relevant columns
    landmark_df_processed = landmark_df_processed[
        ["landmark", "image-coord-dst-0", "image-coord-dst-1", "root_id", "image-coord-src-0"]
    ]
    # Rename columns for more clarity
    landmark_df_processed = landmark_df_processed.rename(
        columns={"image-coord-dst-0": "y", "image-coord-dst-1": "x", "image-coord-src-0": "y_src"}
    )

    # Add the primary root top back to the dataframe
    new_row = landmark_df[landmark_df["landmark"] == "Primary_root_top"]
    new_row = new_row[["landmark", "image-coord-src-0", "image-coord-src-1", "root_id", "node-id-src"]]
    new_row = new_row.rename(
        columns={"image-coord-src-0": "y", "image-coord-src-1": "x", "node-id-src": "y_src"}
    )

    landmark_df_processed.loc[len(landmark_df_processed)] = new_row.iloc[0]

    # Sort the dataframe by the landmark name
    landmark_df_processed = landmark_df_processed.sort_values(by=["root_id"])
    # Reset the index
    landmark_df_processed = landmark_df_processed.reset_index(drop=True)

    return landmark_df_processed


def get_landmarks(subset_plant):
    """
    This is the main function for getting the landmarks of a root structure.
    It first gets the primary landmarks, and then the lateral landmarks.
    After both, it cleans up the dataframe.

    :param subset_plant: The dataframe with the root information.
    :return: landmark_df: The processed dataframe with the landmarks.
    """
    # Create a copy of the dataframe to avoid SettingWithCopyWarning from pandas
    landmark_df = subset_plant.copy()
    # Add a column for the landmarks
    landmark_df["landmark"] = "None"
    # Get the primary landmarks
    landmark_df = get_primary_landmarks(landmark_df)
    # Get the lateral landmarks
    landmark_df = get_lateral_landmarks(landmark_df)
    # Process the landmark dataframe
    landmark_df = process_landmark_df(landmark_df)

    return landmark_df


def draw_landmarks(landmarked_img, landmark_df):
    """
    This function draws the landmarks on the image. It does this by drawing a circle at the x and y coordinates of the landmarks.

    :param landmarked_img: The image of the petri dish.
    :param landmark_df: The dataframe with the landmarks.
    :return: landmarked_img: The image with the landmarks drawn on it.
    """
    # Loop through the rows of the dataframe
    root_id = 0
    landmark_df = landmark_df.sort_values(by=["y_src"])
    for index, row in landmark_df.iterrows():
        if row["landmark"] == "Primary_root_tip":
            color = (255, 0, 255)
            landmark_df.loc[index, "root_id"] = "Primary Tip"
            row["root_id"] = "Primary Tip"
        elif row["landmark"] == "Primary_root_top":
            color = (255, 0, 0)
            landmark_df.loc[index, "root_id"] = "Primary Top"
            row["root_id"] = "Primary Top"
        elif row["landmark"] == "Lateral_root_tip":
            color = (0, 255, 0)
            landmark_df.loc[index, "root_id"] = f"L{root_id}"
            row["root_id"] = f"L{root_id}"
            root_id += 1
        # Get the x and y coordinates of the landmark
        x = int(row["x"])
        y = int(row["y"])
        # Draw a circle at the x and y coordinates
        cv2.circle(landmarked_img, (x, y), 10, color, -1)
        landmarked_img = cv2.putText(landmarked_img, row["root_id"], (x, (y - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                                     1, (0, 0, 0), 2, cv2.LINE_AA)
    return landmarked_img


def find_shoot_plant(subset_plant, shoot_mask):
    """
    This function finds the shoot of the corrospondig plant. It does this by first getting the top of the primary root.
    Then we get all the masks from the shoot mask that are at the same x-coordinate, and above the top of the primary root.
    When there's multiple masks above the top of primary root, we choose all of them.

    :param subset_plant: The dataframe with the root information of only one plant.
    :param shoot_mask: The mask of the shoot.

    :return: new_shoot_mask: The mask of the shoot of the plant.
    """

    # Create subset with only primary root branches.
    primary_subset = subset_plant[subset_plant["root_type"] == "Primary"]
    # Find the primary root top by looking at the lowest node-id-src, which corresponds to the highest location of the primary root.
    primary_root_top_row = primary_subset.loc[primary_subset["node-id-src"].idxmin()]

    # Get the x and y coordinates of the primary root top
    primary_root_top_x = primary_root_top_row["image-coord-src-1"]
    primary_root_y = primary_root_top_row["image-coord-src-0"]

    # Create a black mask with the same size as the shoot mask
    new_shoot_mask = np.zeros_like(shoot_mask)

    # Get the components from the shopot mask
    label_count, labels, stats, centroids = cv2.connectedComponentsWithStats(shoot_mask)

    # Get the labels at the x-coordinate of the primary root top, and above the primary root top
    labels_at_x = labels[:primary_root_y, primary_root_top_x, ]
    # Get the unique labels in the labels at the x-coordinate of the primary root top
    unique_labels = np.unique(labels_at_x)
    # Remove the background label
    unique_labels = unique_labels[unique_labels != 0]

    # If there are unique labels, we set the mask to 255 at the corrosponding labels
    if unique_labels.size > 0:
        for label in unique_labels:
            new_shoot_mask[labels == label] = 255

    return new_shoot_mask


def merge_shoot_root(shoot_mask, root_mask):
    """
    This function adds two masks together. The masks have to be the same size, and only have 2 unique values: 0 and 255.

    :param shoot_mask: The mask of the shoot.
    :param root_mask: The mask of the roots.
    """
    # Make a copy of the root mask
    shoot_root_mask = root_mask.copy()
    # Add the shoot mask to the root mask
    shoot_root_mask[shoot_mask == 255] = 255
    return shoot_root_mask


def add_shoot_image_mask(image, shoot_mask):
    """
    This function adds the shoot mask to the image. It does this by setting the pixels of the shoot mask to a specific color in the image.

    :param image: The image of the petri dish.
    :param shoot_mask: The mask of the shoot.
    :return: image: The image with the shoot mask added to it.
    """
    image[shoot_mask == 255] = [10, 88, 32]
    return image


def prepare_data_for_rxml(subset_plant: pd.DataFrame, skeleton_ob_loc: Skeleton) -> pd.DataFrame:
    rows = []

    for index, row in subset_plant.iterrows():
        yx = skeleton_ob_loc.path_coordinates(index)
        for y, x in yx:
            new_row = {"plant": row["plant"], "root_id": row["root_id"], "x": x, "y": y, "z": 0}
            rows.append(new_row)

    rxml_data = pd.DataFrame(rows, columns=["plant", "root_id", "x", "y", "z"])

    return rxml_data


def measure_folder(folder_dir: str, template_path: str) -> pd.DataFrame:
    """
    This function checks for each timeline, each petri dish. It uses the binary root masks for this.
    It starts with segmenting the roots, and finding the primary roots. After this, it uses the get_lateral function
    to find the lateral roots of every plant. It saves the primary, lateral, and total root length of each plant into an Excel file.
    :param folder_dir: Directory with the location of all the timeline folders.
    :param template_path: Path to the template image with seed positions.
    """
    # Loop through all the timelines
    for timeline in os.listdir(folder_dir):
        # Loop through all the petri dishes in each timeline
        for petri_dish in track(os.listdir(f"{folder_dir}/{timeline}"),
                                description=f' Segmenting and Measuring plants for petri dish - {timeline}'):
            # Check if the file is a png file
            if petri_dish.endswith(".png"):
                # Get the path to the petri dish
                path_to_petri_dish = f"{folder_dir}/{timeline}/{petri_dish}"
                # Get the path to the root masks
                path_to_masks = f"{folder_dir}/{timeline}/{petri_dish[:-4]}"
                # Get the path to the root mask
                for mask in os.listdir(path_to_masks):
                    # Make sure that the mask is the root mask
                    if mask.endswith("root_mask.png"):
                        mask_path = f"{path_to_masks}/{mask}"
                    elif mask.endswith("shoot_mask.png"):
                        shoot_mask_path = f"{path_to_masks}/{mask}"
                        shoot_mask = cv2.imread(shoot_mask_path, 0)

                # Read the image
                image = cv2.imread(path_to_petri_dish)

                # Convert the image to RGB
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                # Perform segmentation and find the primary roots
                primary_root_segmentation = segmentation(
                    mask_path, template_path)
                if primary_root_segmentation is not None:
                    branch_loc, skelton_ob_loc = primary_root_segmentation
                    # Find the lateral roots
                    branch_loc.to_csv("branch_loc.csv", index=False)
                    image, subset_branch = get_lateral(
                        branch_loc, skelton_ob_loc, image)
                    subset_branch["plant"] = subset_branch["plant"] + 1

                    # Draw the primary roots on the image
                    for index, row in subset_branch.iterrows():
                        if row["root_type"] == "Primary":
                            yx = skelton_ob_loc.path_coordinates(index)
                            image = draw_root(yx, image, 0, 0, (0, 0, 255))
                    # Set the root_id to primary for each primary root type
                    subset_branch.loc[subset_branch['root_type'] == 'Primary', 'root_id'] = 'Primary'

                    # Save the segmented image
                    cv2.imwrite(f'{path_to_masks}/image_mask.png', image)

                    rsml.get_rsml(subset_branch, skelton_ob_loc, f"{path_to_masks}/root_structure.rsml")

                    # Create a DataFrame to store the measurements
                    measurement_df = pd.DataFrame(
                        columns=["plant", "Primary_length(mm)", "Lateral_length(mm)", "Total_length(mm)"])
                    # Loop over all the plants in the subset_branch to get the primary, lateral, and total root length of each plant
                    for x in subset_branch["plant"].unique():
                        if math.isnan(x):
                            continue
                        img_mask = np.zeros_like(image)
                        landmarked_img = image.copy()
                        plant_df = pd.DataFrame(
                            columns=["plant", "Primary_length(mm)", "Lateral_length(mm)", "Total_length(mm)"])

                        os.makedirs(f"{path_to_masks}/plant_{x}", exist_ok=True)

                        # Skip the plants that are not assigned to any plant
                        subset_plant = subset_branch[subset_branch["plant"] == x]
                        subset_plant.to_excel(f'{path_to_masks}/plant_{x}/plant_data.xlsx')
                        # Filter the DataFrame to keep the primary and lateral root lengths
                        subset_plant_primary = subset_plant[subset_plant["root_type"] == "Primary"]
                        subset_plant_lateral = subset_plant[subset_plant["root_type"] == "Lateral"]
                        # Calculate the primary, lateral, and total root length of the plant
                        primary_length = subset_plant_primary["branch-distance"].sum()
                        lateral_length = subset_plant_lateral["branch-distance"].sum()
                        # Calculate the total root length of the plant
                        total_length = primary_length + lateral_length
                        # Apply the conversion factor
                        total_length = apply_conversion_factor(total_length)
                        primary_length = apply_conversion_factor(primary_length)
                        lateral_length = apply_conversion_factor(lateral_length)

                        for index, row in subset_plant.iterrows():
                            yx = skelton_ob_loc.path_coordinates(index)
                            img_mask = draw_root(yx, img_mask, 0, 0, (255, 255, 255))

                        cv2.imwrite(f'{path_to_masks}/plant_{x}/root_mask.png', img_mask)

                        # Create a new row for the DataFrame
                        new_row = {"plant": x, "Primary_length(mm)": primary_length,
                                   "Lateral_length(mm)": lateral_length, "Total_length(mm)": total_length}

                        plant_df.loc[len(plant_df)] = new_row
                        plant_df.to_excel(f'{path_to_masks}/plant_{x}/plant_measurements.xlsx')
                        # Add the new row to the DataFrame
                        measurement_df.loc[len(measurement_df)] = new_row

                        landmark_df = get_landmarks(subset_plant)
                        landmarked_img = draw_landmarks(landmarked_img, landmark_df)
                        cv2.imwrite(f'{path_to_masks}/plant_{x}/landmarked_image.png', landmarked_img)
                        landmark_df[["landmark", "y", "x", "root_id"]].to_excel(
                            f'{path_to_masks}/plant_{x}/landmarks.xlsx')

                        new_shoot_mask = find_shoot_plant(subset_plant, shoot_mask)
                        shoot_root_mask = merge_shoot_root(new_shoot_mask, img_mask)
                        image = add_shoot_image_mask(image, new_shoot_mask)
                        cv2.imwrite(f'{path_to_masks}/plant_{x}/shoot_mask.png', new_shoot_mask)
                        cv2.imwrite(f'{path_to_masks}/plant_{x}/shoot_root_mask.png', shoot_root_mask)

                    # Save the measurements to an Excel file
                    measurement_df.to_excel(f'{path_to_masks}/measurements.xlsx')
                    cv2.imwrite(f'{path_to_masks}/image_mask.png', image)
                else:
                    measurement_df = pd.DataFrame(
                        columns=["plant", "Primary_length(mm)", "Lateral_length(mm)", "Total_length(mm)"])
                    new_row = {"plant": 0, "Primary_length(mm)": 0,
                               "Lateral_length(mm)": 0, "Total_length(mm)": 0}
                    measurement_df.loc[len(measurement_df)] = new_row
                    measurement_df.to_excel(f'{path_to_masks}/measurements.xlsx')


def get_timeserie_num(string: str) -> str:
    """
    This function takes the file name of petri dishes in and finds the timeserie number in it.
    The petri dishes have 2 types of locations for the timeserie number. This function finds the correct one, no matter which one it is.

    :param string: File name of the petri dish.
    :return: timeserie: The timeserie number of the petri dish.
    :example:
    >>> get_timeserie_num("034_43-13-ROOT1-2023-08-08_control_pH7_-Fe+B_col0_02-Fish Eye Corrected.png")
    13
    >>> get_timeserie_num("43-11-ROOT1-2023-08-08_pvdCherry_OD01_f6h1_03-Fish Eye Corrected.png")
    11
    """

    if not isinstance(string, str):
        raise TypeError("The input must be a string.")
    # Replace the _ with - to make it easier to split the string
    new_x = string.replace("_", "-")
    # Split the string by the - character
    timeserie = new_x.split("-")[2]

    # If the timeserie is not a digit, it means that the timeserie is in another location in the string.
    if not timeserie.isdigit():
        # Split the string by the - character
        timeserie = new_x.split("-")[1]

    return timeserie


def add_petri_dish(petri_dishes: dict, num: int) -> dict:
    """
    This function adds a new petri dish to the dictionary of petri dishes.
    :param petri_dishes: Dictionary of petri dishes.
    :param num: Number of the petri dish.
    :return: petri_dishes: Dictionary of petri dishes.
    :example:
    >>> add_petri_dish({}, 1)
    {1: {}}
    """
    if not isinstance(petri_dishes, dict):
        raise TypeError("The input must be a dictionary.")
    if not isinstance(num, int):
        raise TypeError("The input must be an integer.")
    # Convert the number to an integer
    key = int(num)
    # Add the petri dish to the dictionary
    petri_dishes[key] = {}
    return petri_dishes


def add_plant_petri_dish(petri_dishes: dict, num: int, plant: int, primary_length: float, lateral_length: float,
                         total_length: float) -> dict:
    """
    This function adds a plant to the petri dish in the dictionary of petri dishes.
    It also adds the primary, lateral, and total root length of the plant to the petri dish.
    :param petri_dishes: Dictionary of petri dishes.
    :param num: Number of the petri dish.
    :param plant: Number of the plant.
    :param primary_length: Primary root length of the plant.
    :param lateral_length: Lateral root length of the plant.
    :param total_length: Total root length of the plant.
    :return: petri_dishes: Dictionary of petri dishes.
    :example:
    >>> add_plant_petri_dish({1: {}}, 1, 1, 100, 50, 150)
    {1: {1: {'primary_length': 100, 'lateral_length': 50, 'total_length': 150}}}
    """
    if not isinstance(petri_dishes, dict):
        raise TypeError("The petri dish input must be a dictionary.")
    if not isinstance(num, int):
        raise TypeError("The num input must be an integer.")
    if not isinstance(plant, int):
        raise TypeError("The plant input must be an integer.")
    if not isinstance(primary_length, (int, float)):
        raise TypeError("The primary_length input must be a float or int.")
    if not isinstance(lateral_length, (int, float)):
        raise TypeError("The lateral_length input must be a float or int.")
    if not isinstance(total_length, (int, float)):
        raise TypeError("The total_length input must be a float or int.")

    key = int(num)
    petri_dishes[key][plant] = {
        "primary_length": primary_length,
        "lateral_length": lateral_length,
        "total_length": total_length
    }
    return petri_dishes


"""
Do we still need this either?
def sort_key(filename: str) -> Tuple[int, int]:
    Extract numerical parts from the filename and return them as a tuple.
    This function splits the filename by the '-' character and converts the
    first two parts to integers, which are then returned as a tuple.
    :param filename: The filename to be processed.
    :type filename: str
    :return: A tuple of integers extracted from the filename.
    :rtype: Tuple[int, int]
    parts = filename.split('-')
    return int(parts[0]), int(parts[1])
def sort_file_names_for_timeseries(dir_name: str) -> List[str]:
    Sort filenames in a directory for time series analysis.
    This function lists all filenames in the specified directory, filters out
    hidden files, sorts the filenames using the `sort_key` function, and
    returns the full paths of the sorted filenames.
    :param dir_name: The directory containing the files to be sorted.
    :type dir_name: str
    :return: A list of full paths to the sorted filenames.
    :rtype: List[str]
    file_names = os.listdir(dir_name)
    file_names = [file for file in file_names if file != '.DS_Store']
    sorted_filenames = sorted(file_names, key=sort_key)
    full_file_names = [os.path.join(dir_name, f_name)
                       for f_name in sorted_filenames]
    return full_file_names
def time_series(masks_dir: str, images_dir: str, output_dir: str, template_path: str) -> pd.DataFrame:
    Process a time series of root images for segmentation and analysis.
    This function processes a series of root images from a specified directory, performing segmentation
    to identify primary and lateral roots. It saves the segmented images to the output directory.
    :param masks_dir: Directory containing the mask images.
    :type masks_dir: str
    :param images_dir: Directory containing the original images.
    :type images_dir: str
    :param output_dir: Directory to save the segmented images.
    :type output_dir: str
    :param template_path: Path to the seed locations template
    :type template_path: str
    :return: List containing branch information for each processed image.
    :rtype: List
    files_sorted = sort_file_names_for_timeseries(masks_dir)
    for mask_path in files_sorted:
        print(mask_path)
        image_name = mask_path[mask_path.rfind(
            '/') + 1:mask_path.rfind('_root')]
        img2 = cv2.imread(f'{images_dir}{image_name}_original_padded.png')
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        # Perform segmentation
        branch_loc, skelton_ob_loc = segmentation(mask_path, template_path)
        img2, subset_branch = get_lateral(branch_loc, skelton_ob_loc, img2)
        for index, row in subset_branch.iterrows():
            if row["root_type"] == "Primary":
                yx = skelton_ob_loc.path_coordinates(index)
                img2 = draw_root(yx, img2, 0, 0, (0, 0, 255))
        # Save the segmented image
        cv2.imwrite(f'{output_dir}{image_name}_segmented.png', img2)
    return subset_branch
Not sure if we need this anymore ?
def measure_folder(masks_dir: str, images_dir: str, output_dir: str, template_path: str) -> pd.DataFrame:
    masks = []
    images = []
    for filename in os.listdir(masks_dir):
            mask_path = f"{masks_dir}/{filename}"
            masks.append(mask_path)
    for filename in os.listdir(images_dir):
            image_path = f"{images_dir}/{filename}"
            images.append(image_path)
    print(len(masks), len(images))
    i = 0
    for mask, image in zip(masks, images):
            print(image)
            image = cv2.imread(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # Perform segmentation
            branch_loc, skelton_ob_loc = segmentation(mask, template_path)
            image, subset_branch = get_lateral(branch_loc, skelton_ob_loc, image)
            for index, row in subset_branch.iterrows():
                if row["root_type"] == "Primary":
                    yx = skelton_ob_loc.path_coordinates(index)
                    image = draw_root(yx, image, 0, 0, (0, 0, 255))
            cv2.imwrite(f'{output_dir}/{i}segmented.png', image)
            pd.DataFrame.to_csv(subset_branch, f'{output_dir}/{i}measurements.csv')
            i += 1
    return subset_branch
branch = time_series('/Users/work_uni/Documents/GitHub/AIxPlant_Science/overlapping_roots/final_pipeline_masks/masks/',
                     '/Users/work_uni/Documents/GitHub/AIxPlant_Science/overlapping_roots/final_pipeline_masks/input_images/',
                     '/Users/work_uni/Documents/GitHub/AIxPlant_Science/overlapping_roots/final_pipeline_masks/output/',
                     '/Users/work_uni/Documents/GitHub/AIxPlant_Science/overlapping_roots/seeding_template.tif')
"""
