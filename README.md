[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/umami-hep/umami-preprocessing/graph/badge.svg?token=K8MJI20UZO)](https://codecov.io/gh/umami-hep/umami-preprocessing)
[![PyPI version](https://badge.fury.io/py/umami-preprocessing.svg)](https://badge.fury.io/py/umami-preprocessing)
[![docs](https://img.shields.io/badge/info-documentation-informational)](https://umami-hep.github.io/umami-preprocessing//)


# UPP: Umami PreProcessing

This is a modular preprocessing pipeline for jet tagging.
It addresses [several issues](https://gitlab.cern.ch/atlas-flavor-tagging-tools/algorithms/umami/-/issues/?label_name%5B%5D=Preprocessing) with the current umami preprocessing workflow, and uses the [`atlas-ftag-tools`](https://github.com/umami-hep/atlas-ftag-tools/) package extensively.

Documentation is found [here](https://umami-hep.github.io/umami-preprocessing/)










### Just to recall things 

* Introduced the `environment.yml` file related to the setup below 


#### Related changes 


NB: `lsetup xcache` does not setup python module `XRootD` while `lsetup xcache` does. 

```bash
setupATLAS
lsetup xrootd
voms-proxy-init -voms atlas
```
or 
Install xrootd precompiled for upp 
```bash 
mamba activate upp 
mamba install -c conda-forge xrootd
```

Then 
```bash
setupATLAS
lsetup xcache
voms-proxy-init -voms atlas
```

The error otherwise being 
```
File "/auto_home/users/rbouquet/miniforge3/envs/upp/lib/python3.11/site-packages/fsspec_xrootd/xrootd.py", line 18, in <module>
    from XRootD import client
ModuleNotFoundError: No module named 'XRootD'
```
