This is a simple converter for the source files of the **DMSP** detector **SSJ/4**.

This package provides 3 modules for use:

1. ***from_gz***
2. ***make_dataset***
2. ***transform_dataset***

The features of these modules are described below.

1) The `unzip(filepath, mode='to_file')` function of the ***from_gz*** module unpacks the gz-archive. The first parameter of the function takes the path to the file. The second parameter must specify the unpacking mode.

Two unpacking modes are available: "*to_file*" (default) and "*to_ram*".

When the "*to_file*" mode is selected, the function creates a new binary file in the archive directory with the archive name, removing its extension.

When the "*to_ram*" mode is selected, the function returns the contents of the archive - a set of bytes.


2) The `make_xr_dataset(filepath)` function of the ***make_dataset*** module parses binary data, forming a set of source data from a binary DMSP file.

The input parameter for the function is the path to the archive file with the "gz" extension.

The function returns a set of source data that requires conversion to physical quantities. The type of the returned value is `xarray.core.dataset.Dataset` (i.e. the **xarray library** is used).


3) The `make_transform_dataset(filepath)` function of the ***transform_dataset*** module parses binary data, forming a set of transformed data from a binary DMSP file.

The input parameter for the function is the path to the archive file with the "gz" extension.

The function returns a set of data **converted to physical quantities**. The type of the returned value is `xarray.core.dataset.Dataset` (i.e. the **xarray library** is used).
