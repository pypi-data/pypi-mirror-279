"""
Houses functions to perform standardization
"""

# pylint: disable= too-many-arguments, too-many-locals, duplicate-code
import warnings

import h5py
import numpy as np
from scipy.sparse import csc_matrix
from tqdm import tqdm

from . import helper


def scale(
    filepath,
    inner_directory,
    with_mean: bool = True,
    with_std: bool = True,
    destination: str = None,
    batch_size: int = 1,
):
    """
    Performs standardization on columns for a given dataset in a HDF5 file
    :param filepath: The path to the HDF5 file
    :param inner_directory: The inner directory of the dataset within the file
    :param with_mean: Whether to center the mean
    :param with_std: Whether to use the standard deviation for standardization
    :param destination: The new field to write the processed data to
    :param batch_size: The number of columns to process at a time
    :return: None
    """
    if destination == inner_directory:
        destination = None
    if batch_size < 1:
        raise ValueError("Batch size must be larger than 0")

    with h5py.File(filepath, "r") as f:
        attrs = f[inner_directory].attrs

        # Determine the type
        encoding_type = attrs.get("encoding-type")

    # Check the encoding type
    match encoding_type:
        case "csr_matrix":
            if with_mean:
                raise ValueError(
                    "This breaks the sparsity of the matrix. Use with_mean=False instead"
                )
            if batch_size != 1:
                warnings.warn(
                    "Standardizing columns with batch processing is not "
                    "supported for csr matrices. Ignoring batch_size"
                )
            scale_csr(filepath, inner_directory, with_std, destination)
        case "csc_matrix":
            if with_mean:
                raise ValueError(
                    "This breaks the sparsity of the matrix. Use with_mean=False instead"
                )
            scale_csc(filepath, inner_directory, with_std, destination, batch_size)
        case "array":
            scale_array(filepath, inner_directory, with_mean, with_std, destination)
        case _:
            raise ValueError("This encoding is not supported")


def scale_array(
    filepath,
    inner_directory,
    with_mean: bool,
    with_std: bool,
    destination,
    batch_size: int = 1,
):
    """
    Performs standardization on columns for a given dataset of encoding-type 'array' in a HDF5 file
    :param filepath: The path to the HDF5 file
    :param inner_directory: The inner directory of the dataset within the file
    :param with_mean: Whether to center the mean
    :param with_std: Whether to use the standard deviation for standardization
    :param destination: The new field to write the processed data to
    :param batch_size: The number of columns to process at a time
    :return: None
    """
    with h5py.File(filepath, "r+") as f:
        data = f[inner_directory]
        shape = f[inner_directory].shape

        if destination is not None:
            helper.prepare_dataset(
                filepath=filepath,
                internal_directory=destination,
                encoding_type="array",
                shape=data[:].shape,
                dtypes=[data[:].dtype],
            )
            new_data = f[destination]

        if data.ndim < 2:  # 1D cases (Ex: var or obs)
            # Center around the mean
            numerator = data - np.nanmean(data) if with_mean else data

            # Get the standard deviation
            denominator = np.nanstd(data) if with_std else 1
            # Prevent divide-by-zero problems
            if np.allclose(denominator, 0):
                denominator = 1

            if destination is not None:
                new_data[:] = numerator / denominator
            else:
                data[:] = numerator / denominator
        else:
            with tqdm(total=shape[1], desc="Applying Standardization") as pbar:
                i = 0  # Keep track of how many columns we have processed
                while i < shape[1]:
                    end = i + batch_size if i + batch_size <= shape[1] else shape[1]
                    cols = data[:, i:end]

                    # Center around the mean
                    numerator = cols - np.nanmean(cols) if with_mean else cols

                    # Get the standard deviation
                    denominator = np.array(np.nanstd(cols, axis=0) if with_std else 1)
                    # Prevent divide-by-zero problems
                    denominator[np.allclose(denominator, 0)] = 1

                    if destination is not None:
                        new_data[:, i:end] = numerator / denominator
                    else:
                        data[:, i:end] = numerator / denominator

                    pbar.update(
                        batch_size if (i + batch_size < shape[1]) else shape[1] - i
                    )
                    i += batch_size


def scale_csc(filepath, inner_directory, with_std: bool, destination, batch_size: int):
    """
    Performs standardization on columns for a given dataset of
    encoding-type 'csc-matrix' in a HDF5 file
    :param filepath: The path to the HDF5 file
    :param inner_directory: The inner directory of the dataset within the file
    :param with_std: Whether to use the standard deviation for standardization
    :param destination: The new field to write the processed data to
    :param batch_size: The number of columns to process at a time
    :return: None
    """
    with h5py.File(filepath, "r+") as f:
        data = f[inner_directory]["data"]
        indices = f[inner_directory]["indices"]
        indptr = f[inner_directory]["indptr"]
        shape = f[inner_directory].attrs.get("shape")

        if destination is not None:
            helper.prepare_dataset(
                filepath=filepath,
                internal_directory=destination,
                encoding_type=f[inner_directory].attrs.get("encoding-type"),
                shape=shape,
                internal_shapes=[data.shape, indices.shape, indptr.shape],
                dtypes=[data.dtype, indices.dtype, indptr.dtype],
            )
            helper.copy_internal_arrays(f, inner_directory, destination)

        if with_std:
            with tqdm(total=shape[1]) as pbar:
                i = 0  # Keep track of the number of columns we have processed
                while i < shape[1]:
                    # Put a cap on end in case our data cannot be
                    # neatly split into batches of batch_size
                    end = i + batch_size if i + batch_size <= shape[1] else shape[1]

                    # Create a csr matrix using our batch data
                    batch_data = data[indptr[i] : indptr[end]]
                    batch_indices = indices[indptr[i] : indptr[end]]
                    batch_indptr = indptr[i : end + 1]
                    batch_indptr -= np.min(batch_indptr)  # indptr needs to start from 0

                    if 0 in batch_data:
                        raise ValueError(
                            "The sparse matrix contains 0 in its data array"
                        )

                    batch = csc_matrix(
                        (batch_data, batch_indices, batch_indptr),
                        shape=(shape[0], end - i),
                    )

                    # Standardize
                    means = np.array(batch.mean(axis=0).astype(data.dtype)).flatten()
                    to_sub = csc_matrix(np.ones(batch.shape)) @ csc_matrix(
                        np.diag(means)
                    )
                    subtracted = batch - to_sub
                    variances = np.array(
                        subtracted.multiply(subtracted).mean()
                    ).flatten()
                    processed_batch = batch @ csc_matrix(
                        np.diag(1 / np.sqrt(variances))
                    )

                    if destination is not None:
                        f[destination]["data"][
                            indptr[i] : indptr[end]
                        ] = processed_batch.data
                        f[destination]["indices"][
                            indptr[i] : indptr[end]
                        ] = processed_batch.indices
                    else:
                        data[indptr[i] : indptr[end]] = processed_batch.data
                        indices[indptr[i] : indptr[end]] = processed_batch.indices

                    pbar.update(
                        batch_size if (i + batch_size < shape[0]) else shape[0] - i
                    )
                    i += batch_size


def scale_csr(filepath: str, inner_directory: str, with_std: bool, destination: str):
    """
    Performs standardization on columns for a given dataset of
    encoding-type 'csr-matrix' in a HDF5 file
    :param filepath: The path to the HDF5 file
    :param inner_directory: The inner directory of the dataset within the file
    :param with_std: Whether to use the standard deviation for standardization
    :param destination: The new field to write the processed data to
    :return: None
    """
    with h5py.File(filepath, "r+") as f:
        data = f[inner_directory]["data"]
        indices = f[inner_directory]["indices"]
        indptr = f[inner_directory]["indptr"]
        shape = f[inner_directory].attrs.get("shape")

        if destination is not None:
            helper.prepare_dataset(
                filepath=filepath,
                internal_directory=destination,
                encoding_type=f[inner_directory].attrs.get("encoding-type"),
                shape=shape,
                internal_shapes=[data.shape, indices.shape, indptr.shape],
                dtypes=[data.dtype, indices.dtype, indptr.dtype],
            )
            helper.copy_internal_arrays(f, inner_directory, destination)

        if with_std:
            # for each column, calculate its standard deviation and divide
            for i in range(0, shape[1]):
                mask = indices[:] == i
                arr = data[mask]

                variance = calc_var(arr, shape[0] - np.shape(arr)[0])
                std_dev = np.sqrt(variance)
                if std_dev != 0:
                    if destination is not None:
                        new_data = f[destination]["data"]
                        new_data[mask] = arr / std_dev
                    else:
                        data[mask] = arr / std_dev


def calc_var(arr, n_zeros: int = 0):
    """
    Function to calculate variance iteratively in one pass using Welford's algorithm
    :param arr: The array to calculate variance for
    :param n_zeros: The number of zeros not included in the array
    :return:
    """

    m, s, k = 0, 0, n_zeros

    for elem in arr:
        if k == 0:
            m = elem
            s = 0
            k += 1
        else:
            m, s, k = var_helper(elem, m, s, k)

    return 0 if s == 0 else s / (k)


def var_helper(x, m, s, k):
    """
    Helper function to calculate variance iteratively
    :param x: the element to evaluate
    :param m: current iteration of m
    :param s: current iteration of s
    :param k: current number of elements
    :return: the new m, s, and k after applying the new element
    """
    new_m = m + (x - m) / (k + 1)
    new_s = s + (x - m) * (x - new_m)
    return new_m, new_s, k + 1
