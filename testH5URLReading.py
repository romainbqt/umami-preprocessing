import h5py
import fsspec

# For XRootD
# rucio list-file-replicas --protocol root user.treisch.48141599._000002.output.h5

# fsspec also works with direct files 
# Try with direct file 
# url = "/home/rbouquet/eos/umamiTest/inputs/user.treisch.601589.e8547_s3797_r13144_p7085.tdd.GN3_dev.25_2_76.26-01-07_CentralDump_p7085_output.h5/user.treisch.48141599._000002.output.h5"

# url = "root://ccxrootdatlas.in2p3.fr:1094//pnfs/in2p3.fr/data/atlas/atlaslocalgroupdisk/rucio/user/treisch/6b/2e/user.treisch.48141599._000002.output.h5"
# url = "root://sedoor1.bfg.uni-freiburg.de:1094//pnfs/bfg.uni-freiburg.de/data/atlaslocalgroupdisk/rucio/user/treisch/6b/2e/user.treisch.48141599._000002.output.h5"
url = "davs://webdav.bfg.uni-freiburg.de:2880/pnfs/bfg.uni-freiburg.de/data/atlaslocalgroupdisk/rucio/user/treisch/6b/2e/user.treisch.48141599._000002.output.h5"

if url.startswith("davs://"):
  # Replace "davs://" by "https://"
  url = "https://" + url[len("davs://"):]


# Open via XRootD
with fsspec.open(url, "rb") as f:
  with h5py.File(f, 'r') as hf:
    print(list(hf.keys()))
    
    
    # print(type(hf) == h5py.File)