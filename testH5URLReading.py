import h5py
import fsspec


##  rucio list-file-replicas --protocol root user.treisch.48141599._000002.output.h5

# For XRootD
# url = "root://ccxrootdatlas.in2p3.fr:1094//pnfs/in2p3.fr/data/atlas/atlaslocalgroupdisk/rucio/user/treisch/6b/2e/user.treisch.48141599._000002.output.h5"
# url = "root://sedoor1.bfg.uni-freiburg.de:1094//pnfs/bfg.uni-freiburg.de/data/atlaslocalgroupdisk/rucio/user/treisch/6b/2e/user.treisch.48141599._000002.output.h5"

# DAVS protocol 
url = "davs://webdav.bfg.uni-freiburg.de:2880/pnfs/bfg.uni-freiburg.de/data/atlaslocalgroupdisk/rucio/user/treisch/6b/2e/user.treisch.48141599._000002.output.h5"

# Open via XRootD or DAVS protocol 
with fsspec.open(url, "rb") as f:
  with h5py.File(f, 'r') as hf:
    print(list(hf.keys()))