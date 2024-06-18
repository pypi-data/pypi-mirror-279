"""
virtual path
"""

from .common import *
from pyuu.seq import iter_unique_val
from pyuu.trivial import *
from .path import Path

__all__ = ['VPath']



def to_path_if_str(p):
    return cast_if_type(p, Path, str)

class PathSys:
    """
    Do not use it. It is not completed.
    """
    def __init__(self, path_map:dict):
        self.path_map = path_map


class VPath:
    """
    Do not use it. It is not completed.
    """
    def __init__(self, roots, prnt, path_map:dict):
        prnt = to_path_if_str(prnt)
        self.prnt = prnt
        self.roots = [to_path_if_str(root) for root in iter_unique_val(roots)]
        self.path_map = path_map[:]

    def add_root(self, path):
        path=to_path_if_str(path)
        roots = self.roots
        self.remove_root(path)
        roots.append(path)
    
    def remove_root(self, path):
        path=to_path_if_str(path)
        roots = self.roots
        try:
            roots.remove(path)
        except ValueError:
            pass

    def map_path(self, src_path, dst_path):
        """
        map path relative to the root
        """
        src_path = to_path_if_str(src_path)
        dst_path = to_path_if_str(dst_path)
        self.path_map[src_path] = dst_path



