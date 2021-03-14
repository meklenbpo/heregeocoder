# Here Geocoder Interface

This is a Python module that will implement two basic functions to be used with
Here Geocoder:
- get a formalized address by X/Y coordinate pair
- get a coordinate pair by an address string

## Here Geocoder API key

A valid Here Geocoder API key is required to operate the `heregeocoder`
module.  

Add a new file called `here_geocoder_credentials.py` to the root of the
module with the following sample content:

```Python

"""Secret Here Geocoder API key."""

APIKEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

```

This will import into the package and provide access to all the functionality.

