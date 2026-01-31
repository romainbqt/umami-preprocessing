import h5py
import fsspec

# For XRootD
# rucio list-file-replicas --protocol root user.treisch.48141599._000002.output.h5


fnames = [
  "root://ccxrootdatlas.in2p3.fr:1094//pnfs/in2p3.fr/data/atlas/atlaslocalgroupdisk/rucio/user/treisch/26/21/user.treisch.48141599._000001.output.h5",
  "root://ccxrootdatlas.in2p3.fr:1094//pnfs/in2p3.fr/data/atlas/atlaslocalgroupdisk/rucio/user/treisch/6b/2e/user.treisch.48141599._000002.output.h5"
]


out_fname = "/home/rbouquet/eos/umamiTest/testVDS.h5"

# Identify common groups across all files
common_groups: set[str] = set()
for fname in fnames:
  with fsspec.open(fname, "rb") as fs:
    with h5py.File(fs, 'r') as f:
        groups = set(f.keys())
        common_groups = groups if not common_groups else common_groups & groups


print(common_groups)
# Ditch the bookkeeper. We will process it separately
common_groups.discard("cutBookkeeper")

# Check that the directory of the output file exists
# out_fname.parent.mkdir(parents=True, exist_ok=True)

# Build the output file
with h5py.File(out_fname, "w") as fout:
    # Build "standard" groups
    for gname in sorted(common_groups):
        layout = get_virtual_layout(fnames, gname)
        fout.create_virtual_dataset(gname, layout)

        # Copy first-file attributes to VDS root object
        with fsspec.open(fnames[0], "rb") as fs0:
          with h5py.File(fs0, 'r') as f0:
              for k, v in f0[gname].attrs.items():
                  fout[gname].attrs[k] = v

    # Build the cutBookkeeper
    counts_total = aggregate_cutbookkeeper(fnames=fnames, group_name=bookkeeper_name)
    if counts_total is not None:
        for sg, record in counts_total.items():
            grp = fout.require_group(f"{bookkeeper_name}/{sg}")
            grp.create_dataset("counts", data=record, shape=(), dtype=record.dtype)
