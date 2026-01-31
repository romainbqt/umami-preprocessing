import h5py
import fsspec
import numpy as np 

# For XRootD
# rucio list-file-replicas --protocol root user.treisch.48141599._000002.output.h5

def getH5File(fileName): 
  isRemoteFile = (fileName.startswith("root://") or fileName.startswith("davs://"))
  
  if fileName.startswith("davs://"):
    # Replace "davs://" by "https://"
    fileName = "https://" + fileName[len("davs://"):]


  if isRemoteFile: 
    # Open via protocol hence using fsspec 
    f = fsspec.open(fileName, "rb").open()
    hf = h5py.File(f, 'r') 
  else: 
    hf = h5py.File(fileName, 'r') 
  
  return hf


def main(): 
  fnames = [
    "root://ccxrootdatlas.in2p3.fr:1094//pnfs/in2p3.fr/data/atlas/atlaslocalgroupdisk/rucio/user/treisch/26/21/user.treisch.48141599._000001.output.h5",
    "root://ccxrootdatlas.in2p3.fr:1094//pnfs/in2p3.fr/data/atlas/atlaslocalgroupdisk/rucio/user/treisch/6b/2e/user.treisch.48141599._000002.output.h5"
  ]


  out_fname = "/home/rbouquet/eos/umamiTest/testVDS.h5"


  # Identify common groups across all files
  common_groups: set[str] = set()
  for fname in fnames:
    with getH5File(fname) as f: 
      groups = set(f.keys())
      common_groups = groups if not common_groups else common_groups & groups


  print(common_groups)
  # Ditch the bookkeeper. We will process it separately
  common_groups.discard("cutBookkeeper")

  Check that the directory of the output file exists
  out_fname.parent.mkdir(parents=True, exist_ok=True)

  # Build the output file
  with h5py.File(out_fname, "w") as fout:
      # Build "standard" groups
      for gname in sorted(common_groups):
          layout = get_virtual_layout(fnames, gname)
          fout.create_virtual_dataset(gname, layout)

          # Copy first-file attributes to VDS root object
          with getH5File(fnames[0]) as f0 
              for k, v in f0[gname].attrs.items():
                  fout[gname].attrs[k] = v

      # Build the cutBookkeeper
      counts_total = aggregate_cutbookkeeper(fnames=fnames, group_name=bookkeeper_name)
      if counts_total is not None:
          for sg, record in counts_total.items():
              grp = fout.require_group(f"{bookkeeper_name}/{sg}")
              grp.create_dataset("counts", data=record, shape=(), dtype=record.dtype)


# Functions below are adaptaed from the vds.py file 
# https://github.com/umami-hep/atlas-ftag-tools/blob/main/ftag/vds.py
  

def aggregate_cutbookkeeper(
    fnames: list[str],
    group_name: str = "cutBookkeeper",
) -> dict[str, np.ndarray] | None:
    """Aggregate the cutBookkeeper in the input files.

    For every input file:
    For every sub-group (nominal, sysUp, sysDown, …):
    1. Sum the 4-entry record array inside each file into 1 record
    1. Add those records from all files together into grand total
    Returns a dict  {subgroup_name: scalar-record-array}

    Parameters
    ----------
    fnames : list[str]
        List of the input files
    group_name: str, optional
        Group name of the cutBookkeeper. By default "cutBookkeeper"

    Returns
    -------
    dict[str, np.ndarray] | None
        Dict with the accumulated cutBookkeeper groups. If the cut bookkeeper
        is not in the files, return None.
    """
    if any(group_name not in h5py.File(f, "r") for f in fnames):
        return None

    subgroups = check_subgroups(fnames, group_name=group_name)

    # initialise an accumulator per subgroup (dtype taken from 1st file)
    accum: dict[str, np.ndarray] = {}
    with h5py.File(fnames[0], "r") as f0:
        for sg in subgroups:
            dtype = f0[f"{group_name}/{sg}/counts"].dtype
            accum[sg] = np.zeros((), dtype=dtype)

    # add each files contribution field-wise
    for fname in fnames:
        with h5py.File(fname, "r") as f:
            for sg in subgroups:
                per_file = sum_counts_once(f[f"{group_name}/{sg}/counts"][()])
                for fld in accum[sg].dtype.names:
                    accum[sg][fld] += per_file[fld]

    return accum

def check_subgroups(fnames: list[str], group_name: str = "cutBookkeeper") -> list[str]:
    """Check which subgroups are available for the bookkeeper.

    Find the intersection of sub-group names that have a 'counts' dataset
    in every input file. (Using the intersection makes the script robust
    even if a few files are missing a variation.)

    Parameters
    ----------
    fnames : list[str]
        List of the input files
    group_name : str, optional
        Group name in the h5 files of the bookkeeper, by default "cutBookkeeper"

    Returns
    -------
    list[str]
        Returns the files with common sub-groups

    Raises
    ------
    KeyError
        When a file does not have a bookkeeper
    ValueError
        When no common bookkeeper sub-groups were found
    """
    common: set[str] | None = None
    for fname in fnames:
        with h5py.File(fname, "r") as f:
            if group_name not in f:
                raise KeyError(f"{fname} has no '{group_name}' group")
            these = {
                name
                for name, item in f[group_name].items()
                if isinstance(item, h5py.Group) and "counts" in item
            }
            common = these if common is None else common & these
    if not common:
        raise ValueError("No common cutBookkeeper sub-groups with 'counts' found")
    return sorted(common)






main()