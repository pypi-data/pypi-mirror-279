"""
This module houses the functions related to log transform
"""
import logging

import h5py
import numpy as np
from tqdm import tqdm

from . import helper


def log_transform(
    filepath: str, inner_directory: str, destination: str = None, batch_size: int = 1
) -> None:
    """
    The function to call to perform log transformation on a given file and inner directory.
    :param filepath: The path to the HDF5 file.
    :param inner_directory: Directory within the file.
    :param destination: The new directory to save the transformed data. Leave as None to overwrite.
    :param batch_size: The size of batches to use when performing log transform
    :return: None
    """
    # Set destination as None if we are overwriting to skip creation of a new dataset
    if destination == inner_directory:
        destination = None

    # Argument check for batch_size
    if batch_size < 1:
        raise ValueError("Batch size must be larger than 0")

    with h5py.File(filepath, "r") as f:
        # Get file attributes in order to determine which type we are processing
        attrs = f[inner_directory].attrs

        # Determine the type
        encoding_type = attrs.get("encoding-type")

    match encoding_type:
        case "csr_matrix":
            log_transform_csr_csc(filepath, inner_directory, destination, batch_size)
        case "csc_matrix":
            log_transform_csr_csc(filepath, inner_directory, destination, batch_size)
        case "array":
            log_transform_array(filepath, inner_directory, destination, batch_size)
        case _:
            raise ValueError("Invalid encoding to apply log transform")


def log_transform_csr_csc(
    filepath: str, inner_directory: str, destination: str, batch_size: int
) -> None:
    """
    Private function to perform log transformation on datasets of encoding-types
    'csr-matrix' and 'csc-matrix'.
    :param filepath: The path to the HDF5 file
    :param inner_directory: The inner directory of the data within the file to transform
    :param destination: The target directory inside the file to store the transformed data
    :param batch_size: The size of batches to use when performing log transform
    :return: None
    """
    with h5py.File(filepath, "r+") as f:
        logging.info("Getting internal arrays from the file")
        # Get the inner arrays of the sparse matrix
        data = f[inner_directory]["data"]
        indices = f[inner_directory]["indices"]
        indptr = f[inner_directory]["indptr"]

        i = 0  # Keep track of how many rows/columns have been processed
        limit = len(indptr) - 1  # The total number of rows/columns we need to process

        with tqdm(total=limit, desc="Applying Log Transform") as pbar:
            if destination is not None:
                # Prepare the file by creating a new field
                helper.prepare_dataset(
                    filepath=filepath,
                    internal_directory=destination,
                    encoding_type=f[inner_directory].attrs.get("encoding-type"),
                    shape=f[inner_directory].attrs.get("shape"),
                    internal_shapes=[data.shape, indices.shape, indptr.shape],
                    dtypes=[data.dtype, indices.dtype, indptr.dtype],
                )
                # Copy the internal arrays of the sparse matrix
                helper.copy_internal_arrays(f, inner_directory, destination)
                new_data = f[destination]["data"]

            while i < limit:
                # In case the number of rows/columns to process is not divisible by the batch size
                if i + batch_size >= limit:
                    if destination is not None:
                        # Process the batch and send it to the new field
                        new_data[indptr[i] :] = np.log1p(data[indptr[i] :])
                    else:
                        # Process the batch and overwrite
                        data[indptr[i] :] = np.log1p(data[indptr[i] :])
                    pbar.update(limit - i)
                    i += batch_size
                else:
                    if destination is not None:
                        # Process the batch and send it to the new field
                        new_data[indptr[i] : indptr[i + batch_size]] = np.log1p(
                            data[indptr[i] : indptr[i + batch_size]]
                        )
                    else:
                        # Process the batch and overwrite
                        data[indptr[i] : indptr[i + batch_size]] = np.log1p(
                            data[indptr[i] : indptr[i + batch_size]]
                        )
                    i += batch_size
                    pbar.update(batch_size)


def log_transform_array(
    filepath: str, inner_directory: str, destination: str, batch_size: int
) -> None:
    """
    Private function to perform log transformation on datasets of encoding-type 'array'
    :param filepath: The path to the HDF5 file
    :param inner_directory: The inner directory of the data within the file to transform
    :param destination: The target directory inside the file to store the transformed data
    :param batch_size: The size of batches to use when performing log transform
    :return: None
    """
    with h5py.File(filepath, "r+") as f:
        logging.info("Getting data and shape from the file")
        # Get views of the data and shape of the dataset from the file
        data = f[inner_directory]
        shape = f[inner_directory].shape
        logging.info("Got data and shape from the file")

        if destination is not None:
            # Prepare a new field in the dataset to write to
            helper.prepare_dataset(
                filepath=filepath,
                internal_directory=destination,
                encoding_type="array",
                shape=data.shape,
                dtypes=[data.dtype],
            )
            logging.info("Finished allocation for the dataset")

            new_data = f[destination]

        with tqdm(total=shape[0], desc="Applying Log Transform") as pbar:
            if data.ndim < 2:  # no batches needed if data is a single row/column
                if destination is not None:
                    new_data[:] = np.log1p(data)
                else:
                    data[:] = np.log1p(data)
            else:
                i = 0  # Keep track of how many rows/columns have been processed
                while i < shape[0]:
                    if i + batch_size >= shape[0]:
                        if destination is not None:
                            # Process the batch and send it to the new field
                            new_data[i:] = np.log1p(data[i:])
                        else:
                            # Process the batch and overwrite
                            data[i:] = np.log1p(data[i:])
                        pbar.update(shape[0] - i)
                    else:
                        if destination is not None:
                            # Process the batch and send it to the new field
                            new_data[i : i + batch_size] = np.log1p(
                                data[i : i + batch_size]
                            )
                        else:
                            # Process the batch and overwrite
                            data[i : i + batch_size] = np.log1p(
                                data[i : i + batch_size]
                            )
                        pbar.update(batch_size)
                    i += batch_size
