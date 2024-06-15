# Reader functions
# for native and non-native file types

import h5py
import pathlib
from os.path import exists, splitext, basename, dirname, join
from typing import Union, Optional
import warnings


# Classes
from emdfile.classes import (
    Root,
    Node,
    Metadata
)
from emdfile.classes.utils import (
    _get_class,
    EMD_data_group_types
)

# EMD 0.1 support
from emdfile.read_EMD_v0p1 import read_EMD_v0p1





# read utilities

def _get_EMD_rootgroups(filepath):
    """
    Returns a list of root groups in an EMD 1.0 file.
    """
    rootgroups = []
    with h5py.File(filepath,'r') as f:
        for key in f.keys():
            if 'emd_group_type' in f[key].attrs:
                if f[key].attrs['emd_group_type'] == 'root':
                    rootgroups.append(key)
    return rootgroups

def _is_EMD_file(filepath):
    """
    Returns True iff filepath points to a valid EMD 1.0 file.
    """
    # check for the 'emd_group_type'='file' attribute
    with h5py.File(filepath,'r') as f:
        try:
            assert('emd_group_type' in f.attrs.keys())
            assert('version_major' in f.attrs.keys())
            assert('version_minor' in f.attrs.keys())
            assert(f.attrs['emd_group_type'] == 'file')
            assert(f.attrs['version_major'] == 1)
            assert(f.attrs['version_minor'] == 0)
        except AssertionError:
            return False
    rootgroups = _get_EMD_rootgroups(filepath)
    if len(rootgroups)>0:
        return True
    else:
        return False

def _get_EMD_version(filepath, rootgroup=None):
    """
    Returns the version (major,minor,release) of an EMD file.
    """
    assert(_is_EMD_file(filepath)), "Error: not recognized as an EMD file"
    with h5py.File(filepath,'r') as f:
        v_major = int(f.attrs['version_major'])
        v_minor = int(f.attrs['version_minor'])
        if 'version_release' in f.attrs.keys():
            v_release = int(f.attrs['version_release'])
        else:
            v_release = 0
        return v_major, v_minor, v_release

def _get_UUID(filepath):
    """
    Returns the UUID of an EMD file, or if unavailable returns -1.
    """
    assert(_is_EMD_file(filepath)), "Error: not recognized as an EMD file"
    with h5py.File(filepath,'r') as f:
        if 'UUID' in f.attrs:
            return f.attrs['UUID']
    return -1

def _version_is_geq(current,minimum):
    """
    Returns True iff current version (major,minor,release) is greater than or equal to minimum."
    """
    if current[0]>minimum[0]:
        return True
    elif current[0]==minimum[0]:
        if current[1]>minimum[1]:
            return True
        elif current[1]==minimum[1]:
            if current[2]>=minimum[2]:
                return True
        else:
            return False
    else:
        return False






########## EMD 1.0+ reader ##########

def read(
    filepath,
    emdpath: Optional[str] = None,
    tree: Optional[Union[bool,str]] = True,
    **legacy_options,
    ):
    """
    File reader for EMD 1.0+ files.

    Args:
        filepath (str or Path): the file path
        emdpath (str): path to the node in an EMD object tree to read
            from. May be a root node or some downstream node. Use '/'
            delimiters between node names. If emdpath is None, checks to
            see how many root nodes are present. If there is one, loads
            this tree. If there are several, returns a list of the root names.
        tree (True or False or 'branch'): indicates what data should be loaded,
            relative to the node specified by `emdpath`. If set to `False`,
            only data/metadata in the specified node is loaded, plus any
            root metadata. If set to `True`, loads that node plus the
            subtree of data objects it contains (and their metadata, and
            the root metadata). If set to `'branch'`, loads the branch
            under this node as above, but does not load the node itself.
            If `emdpath` points to a root node, setting `tree` to `'branch`'
            or `True` are equivalent - both return the whole data tree.

    Returns:
        (Root) returns a Root instance containing (1) any root metadata from
            the EMD tree loaded from, and (2) a tree of one or more pieces
            of data/metadata
    """
    # validate filepath
    assert(isinstance(filepath, (str,pathlib.Path) )), f"filepath must be a string or Path, not {type(filepath)}"
    assert(exists(filepath)), f"specified filepath '{filepath}' was not found on the filesystem"
    try:
        with h5py.File(filepath,'r') as f:
            pass
    except OSError:
        raise Exception(f"The file at {filepath} is not an HDF5 file!")

    # determine if the file is EMD 1.0
    # if not, try reading it as an EMD 0.1
    if not _is_EMD_file(filepath):
        try:
            print(f"This file is not an EMD v1.0 file - attempting to read as an EMD v0.1...")
            ans = read_EMD_v0p1(filepath)
            return ans
        except:
            raise Exception(f"The file at '{filepath}' is not recognized as an EMD file!")


    # get/check version
    v = _get_EMD_version(filepath)


    # determine `emdpath` if it was left as None
    if emdpath is None:
        rootgroups = _get_EMD_rootgroups(filepath)
        if len(rootgroups) == 0:
            raise Exception("No root groups found! This error should never occur! (You're amazing! You've broken the basic laws of logic, reason, and thermodynamics itself!)")
        elif len(rootgroups) == 1:
            emdpath = rootgroups[0]
        else:
            print("Multiple root groups detected - returning root names. Please specify the `emdpath` argument. Returning the list of rootgroups.")
            return rootgroups



    # parse the root and tree paths
    p = emdpath.split('/')
    if '' in p:
        p.remove('')
    rootpath = p[0]
    treepath = '/'.join(p[1:])



    # Open the h5 file
    with h5py.File(filepath,'r') as f:

        # Find the root group
        assert(rootpath in f.keys()), f"Error: root group {rootpath} not found"
        rootgroup = f[rootpath]

        # Find the node of interest
        group_names = treepath.split('/')
        nodegroup = rootgroup
        if len(group_names)==1 and group_names[0]=='':
            pass
        else:
            for name in group_names:
                assert(name in nodegroup.keys()), f"Error: group {name} not found in group {nodegroup.name}"
                nodegroup = nodegroup[name]

        # Read the root
        root = Root.from_h5(rootgroup)

        # if this is all that was requested, return
        if nodegroup is rootgroup and tree is False:
                return root

        # Read...

        # ...if the whole tree was requested
        if nodegroup is rootgroup and tree in (True,'branch'):
            # build the tree
            n = _populate_tree(root,rootgroup)
            # return...
            if n == 1:
                # ...if there's one node, return it
                key = list(root._branch.keys())[0]
                node = root.tree(key)
            elif n == 0 and len(root.metadata) == 1:
                # ...if there's no nodes and one dictionary,
                # return it
                key = list(root.metadata.keys())[0]
                node = root.metadata[key]
            else:
                # ...otherwise, return the root
                node = root

        # ...if a single node was requested
        elif tree is False:
            # read the node
            node = _read_single_node(nodegroup)
            # build the tree and return
            root.force_add_to_tree(node)

        # ...if a branch was requested
        elif tree is True:
            # read source node and add to tree
            node = _read_single_node(nodegroup)
            root.force_add_to_tree(node)
            # build the tree
            _populate_tree(node,nodegroup)

        # ...if `tree == 'branch'`
        else:
            # build the tree
            _populate_tree(root,nodegroup)
            node = root

    # Return
    return node





# group / tree reading utilities

def _read_single_node(grp):
    """
    Determines the class type of the h5py Group `grp`, then
    instantiates and returns an instance of the class with
    this group's data and metadata
    """
    __class__ = _get_class(grp)
    data = __class__.from_h5(grp)
    return data

def _populate_tree(node,group,count=0):
    """
    `node` is a Node and `group` is its parallel h5py Group.
    Reads the tree underneath this nodegroup in the h5 file and adds it
    to the runtime tree underneath this node. Does *not* read `group`
    itself - this function grafts everything underneath `group` onto node

    Returns the number of new nodes added to the tree
    """
    keys = [k for k in group.keys() if isinstance(group[k],h5py.Group)]
    keys = [k for k in keys if 'emd_group_type' in group[k].attrs.keys()]
    keys = [k for k in keys if group[k].attrs['emd_group_type'] in \
        EMD_data_group_types]

    for key in keys:
        new_node = _read_single_node(group[key])
        count += 1
        node.force_add_to_tree(new_node)
        _populate_tree(
            new_node,
            group[key],
            count = count
        )
    return count







# Print the HDF5 filetree to screen

def print_h5_tree(filepath, show_metadata=False):
    """
    Prints the contents of an h5 file from a filepath.
    """
    with h5py.File(filepath,'r') as f:
        print('/')
        _print_h5pyFile_tree(f, show_metadata=show_metadata)
        print('\n')

def _print_h5pyFile_tree(f, tablevel=0, linelevels=[], show_metadata=False):
    """
    Prints the contents of an h5 file from an open h5py File instance.
    """
    if tablevel not in linelevels:
        linelevels.append(tablevel)
    keys = [k for k in f.keys() if isinstance(f[k],h5py.Group)]
    if not show_metadata:
        keys = [k for k in keys if k != 'metadatabundle']
    N = len(keys)
    for i,k in enumerate(keys):
        string = ''
        string += '|' if 0 in linelevels else ' '
        for idx in range(tablevel):
            l = '|' if idx+1 in linelevels else ' '
            string += '   '+l
        print(string+'---'+k)
        if i == N-1:
            linelevels.remove(tablevel)
        _print_h5pyFile_tree(
            f[k],
            tablevel=tablevel+1,
            linelevels=linelevels,
            show_metadata=show_metadata)

    pass



def _read_metadata(
    group,
    name
    ):
    """
    Returns a Metadata instance called name stored in the EMD node at group.
    Returns False otherwise.
    """
    try:
        grp_metadata = group['metadatabundle']
    except KeyError:
        return False
    try:
        metadata = Metadata.from_h5(grp_metadata[name])
        return metadata
    except KeyError:
        return False





