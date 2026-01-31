import h5py
import fsspec

# For XRootD
# rucio list-file-replicas --protocol root user.treisch.48141599._000002.output.h5


def getH5File(fileName): 
  isRemoteFile = (fileName.startswith("root://") or fileName.startswith("davs://"))
  
  if fileName.startswith("davs://"):
    # Replace "davs://" by "https://"
    fileName = "https://" + fileName[len("davs://"):]
  
  if isRemoteFile: 
    # Open via protocol hence using fsspec 
    f = fsspec.open(fileName, "rb", block_size=8 * 1024 * 1024,
            cache_type="readahead").open()
    hf = h5py.File(f, 'r') 
  else: 
    hf = h5py.File(fileName, 'r')
  
  return hf

# fsspec also works with direct files 
# Try with direct file 
fileName= "/home/rbouquet/eos/umamiTest/inputs/user.treisch.601589.e8547_s3797_r13144_p7085.tdd.GN3_dev.25_2_76.26-01-07_CentralDump_p7085_output.h5/user.treisch.48141599._000002.output.h5"

# fileName= "root://ccxrootdatlas.in2p3.fr:1094//pnfs/in2p3.fr/data/atlas/atlaslocalgroupdisk/rucio/user/treisch/6b/2e/user.treisch.48141599._000002.output.h5"
# fileName= "root://sedoor1.bfg.uni-freiburg.de:1094//pnfs/bfg.uni-freiburg.de/data/atlaslocalgroupdisk/rucio/user/treisch/6b/2e/user.treisch.48141599._000002.output.h5"
# fileName= "davs://webdav.bfg.uni-freiburg.de:2880/pnfs/bfg.uni-freiburg.de/data/atlaslocalgroupdisk/rucio/user/treisch/6b/2e/user.treisch.48141599._000002.output.h5"

fileName= "davs://grid03.ge.infn.it:8443/webdav/atlaslocalgroupdisk/rucio/user/treisch/6b/2e/user.treisch.48141599._000002.output.h5"


with getH5File(fileName) as f: 
  print(list(hf.keys()))
  