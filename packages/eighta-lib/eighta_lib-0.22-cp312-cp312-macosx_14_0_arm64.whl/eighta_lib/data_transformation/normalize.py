"""
Houses the functions necessary to perform normalization
"""

# pylint: disable=locally-disabled, too-many-locals, duplicate-code
import warnings

import h5py
import numpy as np
from scipy.sparse import csr_matrix
from tqdm import tqdm

from . import helper


def normalize(
    filepath: str, inner_directory: str, destination: str = None, batch_size: int = 1
):
    """
    Normalizes a field in a given dataset in a hdf5 file
    :param filepath: path to the hdf5 file
    :param inner_directory: inner directory to the dataset to process
    :param destination: destination directory to write the processed dataset to
    :param batch_size: The number of rows to normalize at once
    :return: None
    """
    if destination == inner_directory:
        destination = None
    if batch_size < 1:
        raise ValueError("batch_size must be larger than 0")

    with h5py.File(filepath, "r") as f:
        attrs = f[inner_directory].attrs

        # Determine the type
        encoding_type = attrs.get("encoding-type")

    match encoding_type:
        case "csr_matrix":
            normalize_csr(filepath, inner_directory, destination, batch_size)
        case "csc_matrix":
            warnings.warn(
                "Normalizing rows with batch processing is not supported for csc matrices. "
                "Ignoring batch_size"
            )
            normalize_csc(filepath, inner_directory, destination)
        case "array":
            normalize_array(filepath, inner_directory, destination, batch_size)
        case _:
            raise ValueError("Unsupported Encoding Type for normalization")


def normalize_csr(
    filepath: str, inner_directory: str, destination: str, batch_size: int
):
    """
    Normalizes a dataset of encoding-type csr_matrix in a hdf5 file
    :param filepath: the path to the hdf5 file
    :param inner_directory: the inner directory containing the dataset to process
    :param destination: the field to write the processed dataset to
    :param batch_size: the number of rows to normalize at once
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

        with tqdm(total=shape[0], desc="Applying Normalization") as pbar:
            i = 0  # Number of rows processed
            while i < shape[0]:
                # Put a cap on end in case our data cannot
                # be neatly split into batches of batch_size
                end = i + batch_size if i + batch_size <= shape[0] else shape[0]

                # Create a csr matrix using our batch data
                batch_data = data[indptr[i] : indptr[end]]
                batch_indices = indices[indptr[i] : indptr[end]]
                batch_indptr = indptr[i : end + 1]
                batch_indptr -= np.min(batch_indptr)  # indptr needs to start from 0

                if 0 in batch_data:
                    raise ValueError("The sparse matrix contains 0 in its data array")

                # Empty sparse matrix, nothing to do
                if np.size(batch_data) == 0:
                    return

                batch = csr_matrix((batch_data, batch_indices, batch_indptr))

                # L2 normalization
                batch_sum = np.array(batch.multiply(batch).sum(axis=1)).flatten()
                norms = np.sqrt(batch_sum)
                processed_batch = csr_matrix(np.diag(1 / norms)) @ batch

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

                pbar.update(batch_size if (i + batch_size < shape[0]) else shape[0] - i)
                i += batch_size


def normalize_csc(filepath, inner_directory, destination):
    """
    Normalizes a dataset of encoding-type csc_matrix in a hdf5 file
    :param filepath: the path to the hdf5 file
    :param inner_directory: the inner directory containing the dataset to process
    :param destination: the field to write the processed dataset to
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

        for i in range(shape[0]):
            mask = indices[:] == i
            row = data[mask]
            norm = np.linalg.norm(row)
            if norm != 0:
                if destination is not None:
                    new_data = f[destination]["data"]
                    new_data[mask] = row / norm
                else:
                    data[mask] = row / norm


def normalize_array(filepath, inner_directory, destination, batch_size):
    """
    Normalizes a dataset of encoding-type array in a hdf5 file
    :param filepath: the path to the hdf5 file
    :param inner_directory: the inner directory containing the dataset to process
    :param destination: the field to write the processed dataset to
    :param batch_size: the number of rows to normalize at once
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

        if data.ndim < 2:
            norm = np.linalg.norm(data)
            if norm != 0:
                if destination is not None:
                    new_data[:] = data / norm
                else:
                    data[:] = data / norm
        else:
            i = 0  # Keep track of how many rows we have processed
            with tqdm(total=shape[0], desc="Applying Normalization") as pbar:
                while i < shape[0]:
                    # Put a cap on end in case our data cannot be
                    # neatly split into batches of batch_size
                    end = i + batch_size if i + batch_size <= shape[0] else shape[0]

                    rows = data[i:end]
                    norms = np.array(np.linalg.norm(rows, axis=1))
                    norms[norms == 0] = 1  # prevent division by zero

                    if destination is not None:
                        new_data[i:end] = rows / norms[:, None]
                    else:
                        data[i:end] = rows / norms[:, None]

                    pbar.update(
                        batch_size if (i + batch_size < shape[0]) else shape[0] - i
                    )
                    i += batch_size
