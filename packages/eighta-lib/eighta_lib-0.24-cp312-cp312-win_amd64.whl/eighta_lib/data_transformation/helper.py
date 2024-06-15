"""
Houses functions supporting data transformation functions. Includes support for
writing new fields in datasets and an enum to get encoding version
based on encoding type.
"""

# pylint: disable=locally-disabled, too-many-arguments
import logging
from typing import SupportsIndex, Iterable

import h5py
import numpy as np
from tqdm import tqdm


def get_encoding_version(encoding_type: str) -> str:
    """
    Determine encoding version from encoding type
    :param encoding_type: The encoding type of the dataset
    :return: The encoding version for the dataset
    """
    match encoding_type:
        case "csr_matrix":
            return "0.1.0"
        case "csc_matrix":
            return "0.1.0"
        case "array":
            return "0.2.0"


def prepare_dataset(
    filepath: str,
    internal_directory: str,
    encoding_type: str,
    shape: Iterable,
    dtypes=None,
    internal_shapes=None,
):
    """
    Creates a new dataset in a specified HDF5 file
    :param filepath: The file path of the HDF5 file
    :param internal_directory: The internal directory to be created to house the dataset
    :param encoding_type: The encoding type of the new dataset
    :param shape: The shape of the new dataset
    :param dtypes: The dtype(s) of the new dataset. Has to be of length 3 for sparse matrices
    and length 1 for array matrices
    :param internal_shapes: The internal shape(s) of the new dataset. Not required for
    array matrices
    :return: None
    """
    logging.info("Preparing dataset")
    with h5py.File(filepath, "r+") as f2:
        match encoding_type:
            case "csr_matrix" | "csc_matrix":
                logging.info("Received a sparse matrix")
                if internal_shapes is None or np.size(internal_shapes) != 3:
                    raise ValueError(
                        "This type of matrix requires extra shapes to be supplied"
                    )
                if dtypes is None or np.size(dtypes) != 3:
                    raise ValueError(
                        "3 dtypes need to be supplied to define the internal arrays"
                    )
                if shape is None:
                    raise ValueError("Please specify a shape for the sparse matrix")

                # Create the group (fails if the group already exists)
                grp = f2.create_group(internal_directory)
                logging.info("Setting group attributes")
                # Set the group's attributes
                grp.attrs["encoding-type"] = encoding_type
                grp.attrs["encoding-version"] = get_encoding_version(encoding_type)
                grp.attrs["shape"] = shape
                logging.info("Creating internal arrays")
                # Create internal arrays
                grp.create_dataset("data", shape=internal_shapes[0], dtype=dtypes[0])
                grp.create_dataset("indices", shape=internal_shapes[1], dtype=dtypes[1])
                grp.create_dataset("indptr", shape=internal_shapes[2], dtype=dtypes[2])

            case "array":
                logging.info("Received an array matrix")
                if dtypes is None or np.size(dtypes) != 1:
                    raise ValueError(
                        "This type of matrix requires a dtype to be supplied"
                    )
                f2.create_dataset(internal_directory, shape=shape, dtype=dtypes[0])


def copy_internal_arrays(
    file: str,
    source: str | SupportsIndex | slice,
    destination: str | SupportsIndex | slice,
    batch_size: int = 10,
):
    """
    Copies the internal arrays of a sparse matrix from a source to a destination
    :param file: The file storing the data
    :param source: The source directory within the file
    :param destination: The destination directory within the file
    :param batch_size: How many elements to copy over at once
    :return: None
    """
    logging.info("Copying internal arrays")
    completed = 0
    limit = len(file[destination]["indices"][:])
    with tqdm(total=limit, desc="Copying Internal Arrays") as pbar:
        while completed < limit:
            if completed + batch_size >= limit:
                file[destination]["indices"][completed:] = file[source]["indices"][
                    completed:
                ]
                file[destination]["indptr"][completed:] = file[source]["indptr"][
                    completed:
                ]
                pbar.update(limit - completed)
            else:
                file[destination]["indices"][
                    completed : int(completed + batch_size)
                ] = file[source]["indices"][completed : int(completed + batch_size)]
                file[destination]["indptr"][completed : int(completed + batch_size)] = (
                    file[source]["indptr"][completed : int(completed + batch_size)]
                )
                pbar.update(batch_size)
            completed += batch_size

    logging.info("Completed copying internal arrays!")
