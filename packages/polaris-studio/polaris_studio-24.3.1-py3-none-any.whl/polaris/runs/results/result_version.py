def get_version_from_handle(h5file):
    for group in h5file.list_nodes("/"):
        if group._v_pathname == "/link_moe":
            return 2
    raise LookupError("This result file is too old. Please update it to version 2")
