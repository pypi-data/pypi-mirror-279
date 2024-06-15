"""
This module provides functions and utilities for exploring, processing, slicing,
and writing HDF5 files, specifically targeting the AnnData format and its components.
"""

from typing import Union, Optional
import threading
import h5py
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse import csc_matrix
import psutil
import anndata as ad
import slicers_read
import slicers_write

# Lock for locking mechanism of write_slice_h5ad.
write_lock = threading.Lock()


def explore_hdf5_file(file_path):
    """
    Recursively explores and prints the structure of an HDF5 file.

    Parameters:
        file_path (str): The path to the HDF5 file to explore.

    Outputs:
        This function prints the structure of the HDF5 file, including paths, dataset shapes, data
        types, compression (if applied) as well as the size of each dataset in gigabytes.
    """
    def explore_hdf5(item, path='/', indent=0):
        total_size_gb = 0
        indent_str = '    ' * indent

        if isinstance(item, h5py.Dataset):
            if '_index' in item.attrs:
                index_name = item.attrs['_index']
                print(f"{indent_str}{path} is a Dataset with index: {index_name}")
            else:
                dataset_size_gb = (np.prod(item.shape) * item.dtype.itemsize) / (1024 ** 3)
                total_size_gb += dataset_size_gb
                print(f"{indent_str}{path} is a Dataset with shape {item.shape}, "
                      f"dtype {item.dtype}, and size {dataset_size_gb:.4f} GB")

            # Add the compression information if available
            compression = item.compression if item.compression else "None"
            print(f"{indent_str}Compression: {compression}")

        elif isinstance(item, h5py.Group):
            index_info = ""
            if '_index' in item.attrs:
                index_name = item.attrs['_index']
                index_info = f" with index: {index_name}"
            print(f"{indent_str}{path} is a Group{index_info}")
            for key in item.keys():
                total_size_gb += explore_hdf5(item[key], path=f"{path}{key}/", indent=indent + 1)

        return total_size_gb

    with h5py.File(file_path, 'r') as f:
        total_size_gb = 0
        # Determine the dimensions of X depending on its format
        if isinstance(f['X'], h5py.Group):
            # Assume CSR or CSC format
            num_rows = f['obs'][f['obs'].attrs['_index']].shape[0]
            num_cols = f['var'][f['var'].attrs['_index']].shape[0]
            print(f"AnnData object with n_obs × n_vars = {num_rows} x {num_cols}")
        else:
            # Assume dense matrix
            n_obs, n_vars = f['X'].shape
            print(f"AnnData object with n_obs × n_vars = {n_obs} x {n_vars}")
            dataset_size_gb = (np.prod(f['X'].shape) * f['X'].dtype.itemsize) / (1024 ** 3)
            total_size_gb += dataset_size_gb  # Initialize total size with X dataset size

        total_size_gb += explore_hdf5(f)
        print(f"\nTotal size of the HDF5 file: {total_size_gb:.4f} GB")


def read_process_csr_matrix(
    source_group: h5py.Group,
    row_indices: np.ndarray,
    col_indices: np.ndarray
) -> csr_matrix:
    """
    Processes and slices a CSR (Compressed Sparse Row) matrix into memory.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the CSR matrix.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.

    Returns:
        csr_matrix: A sliced CSR matrix.
    """
    data_list = []
    indices_list = []
    total_indptr = np.zeros(len(row_indices) + 1, dtype=source_group['indptr'].dtype)
    current_length = 0

    # Iterate through the specified row indices to slice the CSR matrix
    for i, row_idx in enumerate(row_indices):
        data_start_idx = source_group['indptr'][row_idx]
        data_end_idx = source_group['indptr'][row_idx + 1]

        if data_start_idx < data_end_idx:
            # Extract data and indices for the current row
            data = source_group['data'][data_start_idx:data_end_idx]
            indices = source_group['indices'][data_start_idx:data_end_idx]

            # Mask to select columns of interest
            mask = np.isin(indices, col_indices)
            if np.any(mask):
                data = data[mask]
                indices = indices[mask]

                # Map indices to new indices based on the selected columns
                index_map = {col: idx for idx, col in enumerate(col_indices)}
                indices = np.array([index_map[i] for i in indices])

                data_list.append(data)
                indices_list.append(indices)

                current_length += data.shape[0]
                total_indptr[i + 1] = current_length
            else:
                total_indptr[i + 1] = current_length
        else:
            total_indptr[i + 1] = current_length

    data_array = (
        np.concatenate(data_list)
        if data_list
        else np.array([], dtype=source_group['data'].dtype)
    )
    indices_array = (
        np.concatenate(indices_list)
        if indices_list
        else np.array([], dtype=source_group['indices'].dtype)
    )
    indptr_array = total_indptr

    return csr_matrix((
        data_array,
        indices_array,
        indptr_array),
        shape=(len(row_indices), len(col_indices))
    )


def read_process_csc_matrix(
    source_group: h5py.Group,
    row_indices: np.ndarray,
    col_indices: np.ndarray
) -> csc_matrix:
    """
    Processes and slices a CSC (Compressed Sparse Column) matrix into memory.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the CSC matrix.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.

    Returns:
        csc_matrix: A sliced CSC matrix.
    """
    data_list = []
    indices_list = []
    total_indptr = np.zeros(len(col_indices) + 1, dtype=source_group['indptr'].dtype)
    current_length = 0

    # Iterate through the specified column indices to slice the CSC matrix
    for i, col_idx in enumerate(col_indices):
        data_start_idx = source_group['indptr'][col_idx]
        data_end_idx = source_group['indptr'][col_idx + 1]

        if data_start_idx < data_end_idx:
            # Extract data and indices for the current column
            data = source_group['data'][data_start_idx:data_end_idx]
            indices = source_group['indices'][data_start_idx:data_end_idx]

            # Mask to select rows of interest
            mask = np.isin(indices, row_indices)
            if np.any(mask):
                data = data[mask]
                indices = indices[mask]

                # Map indices to new indices based on the selected rows
                index_map = {row: idx for idx, row in enumerate(row_indices)}
                indices = np.array([index_map[i] for i in indices])

                data_list.append(data)
                indices_list.append(indices)

                current_length += data.shape[0]
                total_indptr[i + 1] = current_length
            else:
                total_indptr[i + 1] = current_length
        else:
            total_indptr[i + 1] = current_length

    data_array = (
        np.concatenate(data_list)
        if data_list
        else np.array([], dtype=source_group['data'].dtype)
    )
    indices_array = (
        np.concatenate(indices_list)
        if indices_list
        else np.array([], dtype=source_group['indices'].dtype)
    )
    indptr_array = total_indptr

    return csc_matrix((
        data_array,
        indices_array,
        indptr_array),
        shape=(len(row_indices), len(col_indices))
    )


def read_process_matrix(
    source_group: h5py.Group,
    row_indices: np.ndarray,
    col_indices: np.ndarray,
    is_csr: bool
) -> Union[csr_matrix, csc_matrix]:
    """
    Process and slice a matrix (CSR or CSC) into memory.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the matrix.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.
        is_csr (bool): True if the matrix is CSR, False if CSC.

    Returns:
        csr_matrix or csc_matrix: The sliced matrix.
    """
    if is_csr:
        result = slicers_read.read_process_csr_matrix(
          source_group.file.filename,
          source_group.name,
          row_indices,
          col_indices
        )
        return csr_matrix(
          (result[0], result[1], result[2]),
          shape=(len(row_indices),
          len(col_indices)
          )
        )
        # return read_process_csr_matrix(source_group, row_indices, col_indices)
    result = slicers_read.read_process_csc_matrix(
      source_group.file.filename,
      source_group.name,
      row_indices,
      col_indices
    )
    return csc_matrix(
      (result[0], result[1], result[2]),
      shape=(len(row_indices),
      len(col_indices)
      )
    )
    # return read_process_csc_matrix(source_group, row_indices, col_indices)


def read_process_categorical_group(
    source_group: h5py.Group,
    row_indices: np.ndarray,
    col_indices: np.ndarray
) -> pd.Categorical:
    """
    Process an HDF5 group representing a categorical variable, slicing based on
    the specified row or column indices.

    Args:
        source_group (h5py.Group): The source HDF5 group to process.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.

    Returns:
        pandas.Categorical: A categorical representation of the sliced data.
    """
    # Retrieve the 'categories' dataset from the source group
    categories = source_group['categories'][:]

    # Decode byte strings to UTF-8 if necessary
    if isinstance(categories[0], bytes):
        categories = [cat.decode('utf-8') for cat in categories]

    # Determine whether to slice based on row or column indices
    if 'var' in source_group.name:
        codes = source_group['codes'][col_indices]
    elif 'obs' in source_group.name:
        codes = source_group['codes'][row_indices]
    else:
        raise ValueError("Source group name must contain 'var' or 'obs'")

    # Ensure unique codes are integers
    unique_codes = np.unique(codes).astype(int)

    # Generate new categories based on the unique codes
    new_categories = [categories[i] if i < len(categories) else "NaN" for i in unique_codes]

    # Ensure the new categories are unique
    unique_new_categories, unique_indices = np.unique(new_categories, return_index=True)

    # Create a mapping from old codes to new codes using unique indices
    code_map = {
        old_code: new_index
        for new_index, old_code in enumerate(unique_codes[unique_indices])
    }

    # Map the old codes to the new codes, falling back to "NaN" for unknown codes
    new_codes = np.array(
        [
            code_map.get(code, len(unique_new_categories) - 1)
            for code in codes
        ],
        dtype=codes.dtype
    )

    # Return a pandas Categorical from the new codes and unique new categories
    return pd.Categorical.from_codes(new_codes, unique_new_categories)


def read_process_dataframe_group(
    source_group: h5py.Group,
    indices: np.ndarray,
    is_obs: bool,
) -> pd.DataFrame:
    """
    Processes and slices a dataframe group from an HDF5 file, maintaining the column order.

    Args:
        source_group (h5py.Group): The source HDF5 group containing the dataframe.
        indices (array-like): The indices to slice.
        is_obs (bool): True if the dataframe belongs to 'obs', False if it belongs to 'var'.

    Returns:
        pd.DataFrame: The sliced dataframe with the specified indices.
    """
    sliced_data = {}

    # Retrieve the column-order attribute and convert it to a list
    column_order = source_group.attrs.get('column-order', [])
    column_order = column_order.tolist() if isinstance(column_order, np.ndarray) else column_order

    # Iterate over all keys in the source group
    for key in source_group.keys():
        if key == "_index":
            continue  # Skip the index key
        item = source_group[key]
        if isinstance(item, h5py.Dataset):
            # Process datasets by slicing based on indices
            sliced_data[key] = item[indices]
        elif isinstance(item, h5py.Group):
            # Recursively process sub-groups
            sliced_data[key] = read_process_group(item, indices, indices)

    # Get the original indices from the parent 'obs' or 'var' group
    if is_obs:
        original_indices = (
            source_group[source_group.attrs["_index"]][indices]
        )
    else:
        original_indices = (
            source_group[source_group.attrs["_index"]][indices]
        )

    # Create the sliced DataFrame
    sliced_df = pd.DataFrame(sliced_data, index=original_indices.astype(str))

    # Reorder the columns based on the original column order if it is not empty
    if column_order:
        sliced_df = sliced_df[column_order]

    # Preserve the column-order attribute in the DataFrame's metadata
    sliced_df.attrs['column-order'] = column_order

    return sliced_df


def read_process_raw_group(source_group: h5py.Group, row_indices: np.ndarray) -> dict:
    """
    Process an HDF5 group representing a 'raw' group, slicing based on the specified row indices.

    Args:
        source_group (h5py.Group): The source HDF5 group to process.
        row_indices (array-like): The indices of the rows to slice.

    Returns:
        dict: A dictionary containing the sliced data from the 'raw' group.
    """
    sliced_data = {}

    def copy_group(group):
        """
        Recursively copy an HDF5 group into a dictionary.

        Args:
            group (h5py.Group): The HDF5 group to copy.

        Returns:
            dict: A dictionary representation of the HDF5 group.
        """
        data = {}
        for key in group.keys():
            item = group[key]
            if isinstance(item, h5py.Group):
                # Recursively copy sub-groups
                data[key] = copy_group(item)
            elif isinstance(item, h5py.Dataset):
                # Copy datasets
                data[key] = item[()]
        return data

    # Process the 'X' dataset within the 'raw' group
    if 'X' in source_group:
        parent_encoding_type = source_group['X'].attrs.get('encoding-type', None)
        is_csr = parent_encoding_type != "csc_matrix"
        # Get all column indices for slicing
        col_indices = np.arange(source_group['X'].attrs['shape'][1])
        sliced_data['X'] = read_process_matrix(source_group['X'], row_indices, col_indices, is_csr)

    # Process the 'var' dataframe within the 'raw' group
    if 'var' in source_group:
        # Slice the 'var' dataframe (use all rows with slice(None) since we want to keep
        # the unsliced version)
        sliced_data['var'] = read_process_dataframe_group(
            source_group['var'],
            slice(None),
            is_obs=False,
        )

    # Process the 'varm' group within the 'raw' group
    if 'varm' in source_group:
        # Recursively copy the 'varm' group
        sliced_data['varm'] = copy_group(source_group['varm'])

    return sliced_data


def read_process_obsp_group(source_group: h5py.Group, row_indices: np.ndarray) -> dict:
    """
    Process an HDF5 group representing an 'obsp' group, slicing based on the specified row indices.

    Args:
        source_group (h5py.Group): The source HDF5 group to process.
        row_indices (array-like): The indices of the rows to slice.

    Returns:
        dict: A dictionary containing the sliced data from the 'obsp' group.
    """
    sliced_data = {}
    for key in source_group.keys():
        item = source_group[key]
        if isinstance(item, h5py.Group):
            # Determine if the matrix is CSR or CSC
            parent_encoding_type = item.attrs.get('encoding-type', None)
            is_csr = parent_encoding_type != "csc_matrix"
            sliced_data[key] = read_process_matrix(item, row_indices, row_indices, is_csr)
        elif isinstance(item, h5py.Dataset):
            # Slice the dataset across both dimensions using row indices
            data = item[row_indices, :][:, row_indices]
            sliced_data[key] = data

    return sliced_data


def read_process_varp_group(source_group: h5py.Group, col_indices: np.ndarray) -> dict:
    """
    Process an HDF5 group representing a 'varp' group, slicing based on the
    specified column indices.

    Args:
        source_group (h5py.Group): The source HDF5 group to process.
        col_indices (array-like): The indices of the columns to slice.

    Returns:
        dict: A dictionary containing the sliced data from the 'varp' group.
    """
    sliced_data = {}
    for key in source_group.keys():
        item = source_group[key]
        if isinstance(item, h5py.Group):
            # Determine if the matrix is CSR or CSC
            parent_encoding_type = item.attrs.get('encoding-type', None)
            is_csr = parent_encoding_type != "csc_matrix"
            sliced_data[key] = read_process_matrix(item, col_indices, col_indices, is_csr)
        elif isinstance(item, h5py.Dataset):
            # Slice the dataset across both dimensions using column indices
            data = item[col_indices, :][:, col_indices]
            sliced_data[key] = data

    return sliced_data


def read_process_dataset(
    dataset: h5py.Dataset,
    row_indices: np.ndarray,
    col_indices: np.ndarray,
    parent_encoding_type: Optional[str] = None,
    parent_group_name: Optional[str] = None
) -> Optional[np.ndarray]:
    """
    Process an HDF5 dataset based on the specified row and column indices.

    Args:
        dataset (h5py.Dataset): The HDF5 dataset to process.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.
        parent_encoding_type (str, optional): The encoding type of the parent group.
            Default is None.
        parent_group_name (str, optional): The name of the parent group. Default is None.

    Returns:
        numpy.ndarray or None: The sliced data from the dataset or None if no processing is done.
    """
    data = None

    # Skip processing here as it will be handled by read_h5ad_process_matrix
    if parent_encoding_type in ['csr_matrix', 'csc_matrix']:
        return None

    # Scalar datasets
    if dataset.shape == ():
        data = (
            str(dataset[()], 'utf-8')
            if dataset.attrs['encoding-type'] == 'string'
            else dataset[()]
        )
    # 1-D datasets
    elif dataset.ndim == 1:
        data = (
            np.array([str(val, 'utf-8') for val in dataset[:]], dtype=object)
            if dataset.attrs['encoding-type'] == 'string-array'
            else dataset[:]
        )
    # 2-D datasets
    elif dataset.ndim == 2:
        if 'layers' in parent_group_name:
            # Slice across both dimensions
            data = np.empty((len(row_indices), len(col_indices)), dtype=dataset.dtype)
            for i, row in enumerate(row_indices):
                data[i, :] = dataset[row, col_indices]
        elif 'obsm' in parent_group_name:
            # Slice across rows using row_indices
            data = np.empty((len(row_indices), dataset.shape[1]), dtype=dataset.dtype)
            for i, row in enumerate(row_indices):
                data[i, :] = dataset[row, :]
        elif 'varm' in parent_group_name:
            # Slice across rows using col_indices
            data = np.empty((len(col_indices), dataset.shape[1]), dtype=dataset.dtype)
            for i, col in enumerate(col_indices):
                data[i, :] = dataset[col, :]

    return data


def read_process_group(
    source_group: h5py.Group,
    row_indices: np.ndarray,
    col_indices: np.ndarray
) -> dict:
    """
    Process an HDF5 group based on the specified row and column indices.

    Args:
        source_group (h5py.Group): The source HDF5 group to process.
        row_indices (array-like): The indices of the rows to slice.
        col_indices (array-like): The indices of the columns to slice.

    Returns:
        dict: A dictionary containing the sliced data.
    """
    # Get the encoding type of the parent group
    parent_encoding_type = source_group.attrs.get('encoding-type', None)
    sliced_data = {}

    # Process based on the encoding type
    if parent_encoding_type == 'csr_matrix':
        # CSR group - X and Layers
        sliced_data = read_process_matrix(source_group, row_indices, col_indices, is_csr=True)
    elif parent_encoding_type == 'csc_matrix':
        # CSC group - X and Layers
        sliced_data = read_process_matrix(source_group, row_indices, col_indices, is_csr=False)
    elif parent_encoding_type == 'categorical':
        # Categorical group inside Obs, Var, and Raw/Var
        sliced_data = read_process_categorical_group(source_group, row_indices, col_indices)
    elif 'obsp' in source_group.name:
        sliced_data = read_process_obsp_group(source_group, row_indices)
    elif 'varp' in source_group.name:
        sliced_data = read_process_varp_group(source_group, col_indices)
    elif 'obs' in source_group.name and parent_encoding_type == 'dataframe':
        sliced_data = read_process_dataframe_group(source_group, row_indices, is_obs=True)
    elif 'var' in source_group.name and parent_encoding_type == 'dataframe':
        sliced_data = read_process_dataframe_group(source_group, col_indices, is_obs=False)
    elif parent_encoding_type == 'raw':
        sliced_data = read_process_raw_group(source_group, row_indices)
    else:
        # Process nested groups and datasets usually when dictionary is encountered
        for key in source_group.keys():
            item = source_group[key]

            if isinstance(item, h5py.Dataset):
                # Process dataset
                sliced_data[key] = read_process_dataset(
                    item,
                    row_indices,
                    col_indices,
                    parent_encoding_type,
                    source_group.name
                )
            elif isinstance(item, h5py.Group):
                # Recursively process sub-group
                sliced_data[key] = read_process_group(item, row_indices, col_indices)

    return sliced_data


def read_slice_h5ad(
    file_path: str,
    rows: slice,
    cols: slice,
    include_raw: bool = False
) -> ad.AnnData:
    """
    Slice a .h5ad file based on specified rows and columns and return an AnnData object.

    Args:
        file_path (str): The path to the .h5ad file to be sliced.
        rows (slice): A slice object specifying the range of rows to include.
        cols (slice): A slice object specifying the range of columns to include.
        include_raw (bool, optional): If True, include the 'raw' group in the sliced data.
            Default is False.

    Returns:
        AnnData: An AnnData object containing the sliced data.

    Raises:
        MemoryError: If the slice size exceeds available memory when check_size is True.
        ValueError: If no rows or columns are available to slice.
    """
    with h5py.File(file_path, 'r') as f:
        # Get the total number of rows and columns
        num_rows = f['obs'][f['obs'].attrs['_index']].shape[0]
        num_cols = f['var'][f['var'].attrs['_index']].shape[0]

        # Generate row and column indices based on the slice objects
        row_indices = np.arange(
            rows.start or 0,
            rows.stop if rows.stop is not None else num_rows,
            rows.step or 1
        )
        col_indices = np.arange(
            cols.start or 0,
            cols.stop if cols.stop is not None else num_cols,
            cols.step or 1
        )

        # Ensure indices are within bounds
        row_indices = row_indices[row_indices < num_rows]
        col_indices = col_indices[col_indices < num_cols]

        row_indices = row_indices.astype(np.int64)
        col_indices = col_indices.astype(np.int64)

        if len(row_indices) == 0 or len(col_indices) == 0:
            raise ValueError("No rows or columns to slice")

        sliced_data = {}
        for key in f.keys():
            item = f[key]
            if item == 'raw' and not include_raw:
                continue
            if isinstance(item, h5py.Group):
                # Process h5py.Group items (X, layers, obs, ...)
                sliced_data[key] = read_process_group(item, row_indices, col_indices)
            elif isinstance(item, h5py.Dataset):
                # Process h5py.Dataset items (usually not the case, mostly for completeness)
                sliced_data[key] = read_process_dataset(item, row_indices, col_indices)

        # Extract data components from the sliced data
        x = sliced_data.pop('X')
        layers = sliced_data.pop('layers', {})
        obs = sliced_data.pop('obs')
        obsm = sliced_data.pop('obsm', {})
        obsp = sliced_data.pop('obsp', {})
        raw = sliced_data.pop('raw', {}) if include_raw else None
        uns = sliced_data.pop('uns', {})
        var = sliced_data.pop('var')
        varm = sliced_data.pop('varm', {})
        varp = sliced_data.pop('varp', {})

        # Create and return the AnnData object
        adata = ad.AnnData(
            X=x,
            layers=layers,
            obs=obs,
            obsm=obsm,
            obsp=obsp,
            raw=raw,
            uns=uns,
            var=var,
            varm=varm,
            varp=varp
        )

        return adata


def get_memory_info() -> tuple[int, float]:
    """
    Retrieves the available system memory in bytes and gigabytes.

    Returns:
        tuple: A tuple containing:
            - available_memory_b (int): The available memory in bytes.
            - available_memory_gb (float): The available memory in gigabytes.
    """
    available_memory_b = psutil.virtual_memory().available
    available_memory_gb = available_memory_b / (1024 ** 3)
    return available_memory_b, available_memory_gb


def calculate_batch_size(memory_fraction: float, num_cols: int, dtype_size: int) -> int:
    """
    Calculates the batch size for data processing based on the available memory,
    fraction of memory to use, number of columns, and data type size.

    Args:
        memory_fraction (float): The fraction of available memory to use.
        num_cols (int): The number of columns in the dataset.
        dtype_size (int): The size of the data type in bytes.

    Returns:
        int: The calculated batch size. Ensures a minimum batch size of 1.
    """
    available_memory_b, _ = get_memory_info()
    memory_to_use = available_memory_b * memory_fraction
    row_size = num_cols * dtype_size
    return max(1, int(memory_to_use // row_size))


def copy_attrs(
    source: h5py.AttributeManager,
    dest: h5py.AttributeManager,
    shape: tuple = None
) -> None:
    """
    Copies attributes from the source to the destination HDF5 object.

    Args:
        source (h5py.AttributeManager): The source HDF5 object containing attributes.
        dest (h5py.AttributeManager): The destination HDF5 object to copy the attributes to.
        shape (tuple, optional): The shape to set as an attribute in the destination.
            Default is None.

    Raises:
        ValueError: If the destination object is invalid.
    """
    # Ensure the destination object is valid before copying attributes
    if not dest or not hasattr(dest, 'attrs'):
        raise ValueError("Invalid destination object. Cannot copy attributes.")

    # Copy each attribute from the source to the destination
    for key, value in source.attrs.items():
        dest.attrs[key] = value

    # If a shape is provided, set it as an attribute in the destination
    if shape is not None:
        dest.attrs['shape'] = shape


def write_process_csr_matrix(
    source_group: h5py.Group,
    dest_file_path: str,
    row_indices: np.ndarray,
    col_indices: np.ndarray,
    batch_size: int
) -> None:
    """
    Processes and writes a CSR matrix to the destination HDF5 file with specified slicing.

    Args:
        source_group (h5py.Group): The source group containing the CSR matrix.
        dest_file_path (str): The path to the destination HDF5 file.
        row_indices (np.ndarray): The indices of the rows to include in the slice.
        col_indices (np.ndarray): The indices of the columns to include in the slice.
        batch_size (int): The size of the batch for processing large datasets.
    """
    with write_lock:
        with h5py.File(dest_file_path, 'a') as f_dest:
            # Create destination datasets with initial empty shapes and appropriate compression
            dest_group = f_dest.require_group(source_group.name)
            data_group = dest_group.create_dataset(
                'data', shape=(0,), maxshape=(None,), dtype=source_group['data'].dtype,
                compression=source_group['data'].compression
            )
            indices_group = dest_group.create_dataset(
                'indices', shape=(0,), maxshape=(None,), dtype=source_group['indices'].dtype,
                compression=source_group['indices'].compression
            )
            indptr_group = dest_group.create_dataset(
                'indptr', shape=(len(row_indices) + 1,), dtype=source_group['indptr'].dtype,
                compression=source_group['indptr'].compression
            )
            indptr_group[0] = 0

    # Initialize the total indptr array and current length counter
    total_indptr = np.zeros(len(row_indices) + 1, dtype=source_group['indptr'].dtype)
    current_length = 0

    # Process the data in batches
    for start in range(0, len(row_indices), batch_size):
        end = min(start + batch_size, len(row_indices))
        batch_row_indices = row_indices[start:end]

        for i, row_idx in enumerate(batch_row_indices, start=start):
            data_start_idx = source_group['indptr'][row_idx]
            data_end_idx = source_group['indptr'][row_idx + 1]

            if data_start_idx < data_end_idx:
                # Extract data and indices for the current row
                data = source_group['data'][data_start_idx:data_end_idx]
                indices = source_group['indices'][data_start_idx:data_end_idx]

                # Mask and map indices to the new column indices
                mask = np.isin(indices, col_indices)
                data = data[mask]
                indices = indices[mask]

                index_map = {col: i for i, col in enumerate(col_indices)}
                indices = np.array([index_map[i] for i in indices])

                # Write data to the destination datasets
                with write_lock:
                    with h5py.File(dest_file_path, 'a') as f_dest:
                        dest_group = f_dest.require_group(source_group.name)
                        data_group = dest_group['data']
                        indices_group = dest_group['indices']

                        data_group.resize((current_length + data.shape[0],))
                        indices_group.resize((current_length + indices.shape[0],))

                        data_group[current_length:current_length + data.shape[0]] = data
                        indices_group[current_length:current_length + indices.shape[0]] = indices

                current_length += data.shape[0]
                total_indptr[i + 1] = current_length

    # Write the indptr to the destination dataset
    with write_lock:
        with h5py.File(dest_file_path, 'a') as f_dest:
            dest_group = f_dest.require_group(source_group.name)
            indptr_group = dest_group['indptr']
            indptr_group[:] = total_indptr
            copy_attrs(source_group, dest_group, shape=(len(row_indices), len(col_indices)))


def write_process_csc_matrix(
    source_group: h5py.Group,
    dest_file_path: str,
    row_indices: np.ndarray,
    col_indices: np.ndarray,
    batch_size: int
) -> None:
    """
    Processes and writes a CSC matrix to the destination HDF5 file with specified slicing.

    Args:
        source_group (h5py.Group): The source group containing the CSC matrix.
        dest_file_path (str): The path to the destination HDF5 file.
        row_indices (np.ndarray): The indices of the rows to include in the slice.
        col_indices (np.ndarray): The indices of the columns to include in the slice.
        batch_size (int): The size of the batch for processing large datasets.
    """
    with write_lock:
        with h5py.File(dest_file_path, 'a') as f_dest:
            # Create destination datasets with initial empty shapes and appropriate compression
            dest_group = f_dest.require_group(source_group.name)
            data_group = dest_group.create_dataset(
                'data', shape=(0,), maxshape=(None,), dtype=source_group['data'].dtype,
                compression=source_group['data'].compression
            )
            indices_group = dest_group.create_dataset(
                'indices', shape=(0,), maxshape=(None,), dtype=source_group['indices'].dtype,
                compression=source_group['indices'].compression
            )
            indptr_group = dest_group.create_dataset(
                'indptr', shape=(len(col_indices) + 1,), dtype=source_group['indptr'].dtype,
                compression=source_group['indptr'].compression
            )
            indptr_group[0] = 0

    # Initialize the total indptr array and current length counter
    total_indptr = np.zeros(len(col_indices) + 1, dtype=source_group['indptr'].dtype)
    current_length = 0

    # Process the data in batches
    for start in range(0, len(col_indices), batch_size):
        end = min(start + batch_size, len(col_indices))
        batch_col_indices = col_indices[start:end]

        for i, col_idx in enumerate(batch_col_indices, start=start):
            data_start_idx = source_group['indptr'][col_idx]
            data_end_idx = source_group['indptr'][col_idx + 1]

            if data_start_idx < data_end_idx:
                # Extract data and indices for the current column
                data = source_group['data'][data_start_idx:data_end_idx]
                indices = source_group['indices'][data_start_idx:data_end_idx]

                # Mask and map indices to the new row indices
                mask = np.isin(indices, row_indices)
                data = data[mask]
                indices = indices[mask]

                index_map = {row: i for i, row in enumerate(row_indices)}
                indices = np.array([index_map[i] for i in indices])

                # Write data to the destination datasets
                with write_lock:
                    with h5py.File(dest_file_path, 'a') as f_dest:
                        dest_group = f_dest.require_group(source_group.name)
                        data_group = dest_group['data']
                        indices_group = dest_group['indices']

                        data_group.resize((current_length + data.shape[0],))
                        indices_group.resize((current_length + indices.shape[0],))

                        data_group[current_length:current_length + data.shape[0]] = data
                        indices_group[current_length:current_length + indices.shape[0]] = indices

                current_length += data.shape[0]
                total_indptr[i + 1] = current_length

    # Write the indptr to the destination dataset
    with write_lock:
        with h5py.File(dest_file_path, 'a') as f_dest:
            dest_group = f_dest.require_group(source_group.name)
            indptr_group = dest_group['indptr']
            indptr_group[:] = total_indptr
            copy_attrs(source_group, dest_group, shape=(len(row_indices), len(col_indices)))


def write_process_matrix(
    source_group: h5py.Group,
    dest_file_path: str,
    row_indices: np.ndarray,
    col_indices: np.ndarray,
    batch_size: int,
    is_csr: bool
) -> None:
    """
    Processes and writes a matrix (CSR or CSC) to the destination HDF5 file with specified slicing.

    Args:
        source_group (h5py.Group): The source group containing the matrix.
        dest_file_path (str): The path to the destination HDF5 file.
        row_indices (np.ndarray): The indices of the rows to include in the slice.
        col_indices (np.ndarray): The indices of the columns to include in the slice.
        batch_size (int): The size of the batch for processing large datasets.
        is_csr (bool): Flag indicating if the matrix is CSR (True) or CSC (False).
    """
    # Kept here for C integration.
    if is_csr:
        with write_lock:
            with h5py.File(dest_file_path, 'a') as f_dest:
                dest_group = f_dest.require_group(source_group.name)
                dest_group.create_dataset(
                    'data', shape=(0,), maxshape=(None,), dtype=source_group['data'].dtype,
                    compression=source_group['data'].compression
                )
                dest_group.create_dataset(
                    'indices', shape=(0,), maxshape=(None,), dtype=source_group['indices'].dtype,
                    compression=source_group['indices'].compression
                )
                dest_group.create_dataset(
                    'indptr', shape=(len(row_indices) + 1,), dtype=source_group['indptr'].dtype,
                    compression=source_group['indptr'].compression
                )
        slicers_write.write_process_csr_matrix(
          source_group.file.filename,
          dest_file_path,
          source_group.name,
          row_indices,
          col_indices,
          batch_size
        )
    else:
        with write_lock:
            with h5py.File(dest_file_path, 'a') as f_dest:
                dest_group = f_dest.require_group(source_group.name)
                dest_group.create_dataset(
                    'data', shape=(0,), maxshape=(None,), dtype=source_group['data'].dtype,
                    compression=source_group['data'].compression
                )
                dest_group.create_dataset(
                    'indices', shape=(0,), maxshape=(None,), dtype=source_group['indices'].dtype,
                    compression=source_group['indices'].compression
                )
                dest_group.create_dataset(
                    'indptr', shape=(len(col_indices) + 1,), dtype=source_group['indptr'].dtype,
                    compression=source_group['indptr'].compression
                )
        slicers_write.write_process_csc_matrix(
          source_group.file.filename,
          dest_file_path,
          source_group.name,
          row_indices,
          col_indices,
          batch_size
        )
    with write_lock:
        with h5py.File(dest_file_path, 'a') as f_dest:
            dest_group = f_dest.require_group(source_group.name)
            copy_attrs(source_group, dest_group, shape=(len(row_indices), len(col_indices)))
    # if is_csr:
    #     write_process_csr_matrix(source_group, dest_file_path, row_indices, col_indices, batch_size)
    # else:
    #     write_process_csc_matrix(source_group, dest_file_path, row_indices, col_indices, batch_size)


def write_process_categorical_group(
    source_group: h5py.Group,
    dest_file_path: str,
    row_indices: np.ndarray,
    col_indices: np.ndarray
) -> None:
    """
    Processes and writes a categorical group to the destination HDF5 file with specified slicing.

    Args:
        source_group (h5py.Group): The source group to process.
        dest_file_path (str): The path to the destination HDF5 file.
        row_indices (np.ndarray): The indices of the rows to include in the slice.
        col_indices (np.ndarray): The indices of the columns to include in the slice.
    """
    # Extract categories from the source group
    categories = source_group['categories'][:]

    # Determine whether to use row or column indices based on the group's name
    if 'var' in source_group.name:
        codes = source_group['codes'][col_indices]
    elif 'obs' in source_group.name:
        codes = source_group['codes'][row_indices]

    # Get unique codes and their corresponding categories
    unique_codes = np.unique(codes)
    new_categories = categories[unique_codes]

    # Ensure new_categories contains only unique values
    unique_new_categories, unique_indices = np.unique(new_categories, return_index=True)
    new_categories = unique_new_categories
    unique_codes = unique_codes[unique_indices]

    # Create a mapping from old codes to new codes
    code_map = {old_code: new_code for new_code, old_code in enumerate(unique_codes)}

    # Map old codes to new codes
    new_codes = np.array([code_map.get(code, -1) for code in codes], dtype=codes.dtype)

    with write_lock:
        with h5py.File(dest_file_path, 'a') as f_dest:
            dest_group = f_dest.require_group(source_group.name)

            # Create datasets for new categories and codes
            categories_dset = dest_group.create_dataset(
                'categories',
                data=new_categories,
                dtype=new_categories.dtype,
                compression=source_group['categories'].compression
            )
            codes_dset = dest_group.create_dataset(
                'codes',
                data=new_codes,
                dtype=new_codes.dtype,
                compression=source_group['codes'].compression
            )

            # Copy attributes from the source to the destination datasets
            copy_attrs(source_group['categories'], categories_dset)
            copy_attrs(source_group['codes'], codes_dset)
            copy_attrs(source_group, dest_group)


def write_process_raw_group(
        source_group: h5py.Group,
        dest_file_path: str,
        row_indices: np.ndarray,
        batch_size: int
) -> None:
    """
    Processes and writes the 'raw' group to the destination HDF5 file with specified slicing.

    Args:
        source_group (h5py.Group): The source group to process.
        dest_file_path (str): The path to the destination HDF5 file.
        row_indices (np.ndarray): The indices of the rows to include in the slice.
        batch_size (int): The size of the batch for processing large datasets.
    """
    if 'X' in source_group.name:
        # Determine if the encoding type is CSR or CSC matrix
        parent_encoding_type = source_group.attrs.get('encoding-type', None)
        is_csr = parent_encoding_type != "csc_matrix"

        # Process the matrix with appropriate CSR/CSC flag
        write_process_matrix(
            source_group,
            dest_file_path,
            row_indices,
            np.arange(source_group.attrs['shape'][1]),
            batch_size,
            is_csr
        )

    if 'var' in source_group.name:
        for var_key in source_group.keys():
            with write_lock:
                with h5py.File(dest_file_path, 'a') as f_dest:
                    dest_group = f_dest.require_group(source_group.name)
                    # Copy var_key to the destination group if not already present
                    if var_key not in dest_group:
                        source_group.copy(var_key, dest_group)

    if 'varm' in source_group.name:
        for varm_key in source_group.keys():
            with write_lock:
                with h5py.File(dest_file_path, 'a') as f_dest:
                    dest_group = f_dest.require_group(source_group.name)
                    # Copy varm_key to the destination group if not already present
                    if varm_key not in dest_group:
                        source_group.copy(varm_key, dest_group)


def write_process_obsp_group(
        source_group: h5py.Group,
        dest_file_path: str,
        row_indices: np.ndarray,
        batch_size: int
) -> None:
    """
    Processes and writes 'obsp' group to the destination HDF5 file with specified slicing.

    Args:
        source_group (h5py.Group): The source group to process.
        dest_file_path (str): The path to the destination HDF5 file.
        row_indices (np.ndarray): The indices of the rows to include in the slice.
        batch_size (int): The size of the batch for processing large datasets.
    """
    for key in source_group.keys():
        item = source_group[key]

        if isinstance(item, h5py.Group):
            # Determine if the encoding type is CSR or CSC matrix
            parent_encoding_type = item.attrs.get('encoding-type', None)
            is_csr = parent_encoding_type != "csc_matrix"
            # Process the matrix with appropriate CSR/CSC flag
            write_process_matrix(item, dest_file_path, row_indices, row_indices, batch_size, is_csr)
        elif isinstance(item, h5py.Dataset):
            # Slice the dataset according to the row indices
            data = item[row_indices, :][:, row_indices]
            with write_lock:
                with h5py.File(dest_file_path, 'a') as f_dest:
                    # Ensure the destination group exists and create the dataset
                    dest_group = f_dest.require_group(source_group.name)
                    dset = dest_group.create_dataset(key, data=data, compression=item.compression)
                    # Copy attributes from the source to the destination dataset
                    copy_attrs(item, dset, shape=data.shape)


def write_process_varp_group(
        source_group: h5py.Group,
        dest_file_path: str,
        col_indices: np.ndarray,
        batch_size: int
) -> None:
    """
    Processes and writes 'varp' group to the destination HDF5 file with specified slicing.

    Args:
        source_group (h5py.Group): The source group to process.
        dest_file_path (str): The path to the destination HDF5 file.
        col_indices (np.ndarray): The indices of the columns to include in the slice.
        batch_size (int): The size of the batch for processing large datasets.
    """
    for key in source_group.keys():
        item = source_group[key]

        if isinstance(item, h5py.Group):
            # Determine if the encoding type is CSR or CSC matrix
            parent_encoding_type = item.attrs.get('encoding-type', None)
            is_csr = parent_encoding_type != "csc_matrix"
            # Process the matrix with appropriate CSR/CSC flag
            write_process_matrix(item, dest_file_path, col_indices, col_indices, batch_size, is_csr)
        elif isinstance(item, h5py.Dataset):
            # Slice the dataset according to the column indices
            data = item[col_indices, :][:, col_indices]
            with write_lock:
                with h5py.File(dest_file_path, 'a') as f_dest:
                    # Ensure the destination group exists and create the dataset
                    dest_group = f_dest.require_group(source_group.name)
                    dset = dest_group.create_dataset(key, data=data, compression=item.compression)
                    # Copy attributes from the source to the destination dataset
                    copy_attrs(item, dset, shape=data.shape)


def write_process_dataset(
        dataset: h5py.Dataset,
        dest_file_path: str,
        group_path: str,
        row_indices: np.ndarray,
        col_indices: np.ndarray,
        parent_encoding_type: str = None,
        parent_group_name: str = None
) -> None:
    """
    Processes and writes a dataset to the destination HDF5 file with specified slicing.

    Args:
        dataset (h5py.Dataset): The dataset to process.
        dest_file_path (str): The path to the destination HDF5 file.
        group_path (str): The path within the destination file where the dataset will be written.
        row_indices (np.ndarray): The indices of the rows to include in the slice.
        col_indices (np.ndarray): The indices of the columns to include in the slice.
        parent_encoding_type (str, optional): The encoding type of the parent group.
            Default is None.
        parent_group_name (str, optional): The name of the parent group. Default is None.
    """
    compression = dataset.compression if dataset.compression else None
    data = None

    # Skip processing if parent encoding type is a sparse matrix
    if parent_encoding_type in ['csr_matrix', 'csc_matrix']:
        return

    # Process 1D datasets
    if dataset.ndim == 1:
        if 'obs' in parent_group_name:
            valid_row_indices = row_indices[row_indices < dataset.shape[0]]
            data = dataset[valid_row_indices]
        elif 'var' in parent_group_name:
            valid_col_indices = col_indices[col_indices < dataset.shape[0]]
            data = dataset[valid_col_indices]
        else:
            data = dataset[:]
    # Process 2D datasets
    elif dataset.ndim == 2:
        if 'layers' in parent_group_name:
            data = np.empty((len(row_indices), len(col_indices)), dtype=dataset.dtype)
            for i, row in enumerate(row_indices):
                data[i, :] = dataset[row, col_indices]
        elif 'obsm' in parent_group_name:
            data = np.empty((len(row_indices), dataset.shape[1]), dtype=dataset.dtype)
            for i, row in enumerate(row_indices):
                data[i, :] = dataset[row, :]
        elif 'varm' in parent_group_name:
            data = np.empty((len(col_indices), dataset.shape[1]), dtype=dataset.dtype)
            for i, col in enumerate(col_indices):
                data[i, :] = dataset[col, :]

    # Write the processed data to the destination file
    if data is not None:
        with write_lock:
            with h5py.File(dest_file_path, 'a') as f_dest:
                dest_group = f_dest.require_group(group_path)
                dset = dest_group.create_dataset(
                    dataset.name.split('/')[-1],
                    data=data,
                    compression=compression
                )
                copy_attrs(dataset, dset)


def write_process_group(
        source_group: h5py.Group,
        dest_file_path: str,
        row_indices: np.ndarray,
        col_indices: np.ndarray,
        batch_size: int = 1000
) -> None:
    """
    Processes and writes a group to the destination HDF5 file, handling different
    encoding types.

    Args:
        source_group (h5py.Group): The source group to process.
        dest_file_path (str): The path to the destination HDF5 file.
        row_indices (np.ndarray): The indices of the rows to include in the slice.
        col_indices (np.ndarray): The indices of the columns to include in the slice.
        batch_size (int, optional): The size of the batch for processing large datasets.
            Default is 1000.
    """
    parent_encoding_type = source_group.attrs.get('encoding-type', None)

    # Process according to the parent encoding type
    if parent_encoding_type == 'csr_matrix':
        write_process_matrix(
            source_group,
            dest_file_path,
            row_indices,
            col_indices,
            batch_size,
            is_csr=True
        )
    elif parent_encoding_type == 'csc_matrix':
        write_process_matrix(
            source_group,
            dest_file_path,
            row_indices,
            col_indices,
            batch_size,
            is_csr=False
        )
    elif parent_encoding_type == 'categorical':
        write_process_categorical_group(source_group, dest_file_path, row_indices, col_indices)
    elif 'obsp' in source_group.name:
        write_process_obsp_group(source_group, dest_file_path, row_indices, batch_size)
    elif 'varp' in source_group.name:
        write_process_varp_group(source_group, dest_file_path, col_indices, batch_size)
    else:
        # Iterate through items in the source group
        for key in source_group.keys():
            item = source_group[key]

            if isinstance(item, h5py.Dataset):
                write_process_dataset(
                    item,
                    dest_file_path,
                    source_group.name,
                    row_indices,
                    col_indices,
                    parent_encoding_type,
                    source_group.name
                )
            elif isinstance(item, h5py.Group):
                if source_group.name == '/raw':
                    write_process_raw_group(item, dest_file_path, row_indices, batch_size)
                else:
                    write_process_group(item, dest_file_path, row_indices, col_indices, batch_size)


def write_slice_h5ad(
        source_file_path: str,
        dest_file_path: str,
        rows: slice,
        cols: slice,
        memory_fraction: float = 0.1
) -> None:
    """
    Writes a sliced version of an h5ad file to a new destination file.

    Args:
        source_file_path (str): The path to the source h5ad file.
        dest_file_path (str): The path to the destination h5ad file.
        rows (slice): The slice object defining the row indices to include.
        cols (slice): The slice object defining the column indices to include.
        memory_fraction (float): The fraction of available memory to use for processing.
            Default is 0.1 (10%).

    Raises:
        ValueError: If no rows or columns are selected for slicing.
    """
    with h5py.File(source_file_path, 'r') as f_src:
        # Create destination file, truncating if it already exists
        h5py.File(dest_file_path, 'w')

        # Retrieve the number of rows and columns in the source file
        num_rows = f_src['obs'][f_src['obs'].attrs['_index']].shape[0]
        num_cols = f_src['var'][f_src['var'].attrs['_index']].shape[0]

        # Generate row and column indices based on the provided slices
        row_indices = np.arange(
            rows.start or 0,
            rows.stop if rows.stop is not None else num_rows,
            rows.step or 1
        )
        col_indices = np.arange(
            cols.start or 0,
            cols.stop if cols.stop is not None else num_cols,
            cols.step or 1
        )

        # Ensure indices do not exceed the available range
        row_indices = row_indices[row_indices < num_rows]
        col_indices = col_indices[col_indices < num_cols]

        # Convert indices to 64-bit integers
        row_indices = row_indices.astype(np.int64)
        col_indices = col_indices.astype(np.int64)

        # Raise an error if no valid rows or columns are selected
        if len(row_indices) == 0 or len(col_indices) == 0:
            raise ValueError("No rows or columns to slice")

        # Determine the data type size and calculate the appropriate batch size
        dtype_size = f_src['X/data'].dtype.itemsize
        batch_size = calculate_batch_size(memory_fraction, len(col_indices), dtype_size)

        # Iterate over items in the source file
        for key in f_src.keys():
            item = f_src[key]

            if isinstance(item, h5py.Group):
                if key == 'uns':
                    # Copy 'uns' group to the destination file
                    with write_lock:
                        with h5py.File(dest_file_path, 'a') as f_dest:
                            f_src.copy(key, f_dest)
                else:
                    # Create the group in the destination file and copy attributes
                    with write_lock:
                        with h5py.File(dest_file_path, 'a') as f_dest:
                            dest_group = f_dest.require_group(key)
                            copy_attrs(item, dest_group)
                    # Process the group for writing sliced data
                    write_process_group(item, dest_file_path, row_indices, col_indices, batch_size)
            elif isinstance(item, h5py.Dataset):
                # Process the dataset for writing sliced data
                write_process_dataset(item, dest_file_path, key, row_indices, col_indices)
