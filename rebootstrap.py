import importlib
import os
import sys
import types

PY3 = sys.version_info >= (3, 4)


def main():
    re_bootstrap()
    print("import machinery has been reloaded with non-frozen impls, have fun debugging!")

    # do whatever import hackery you want from here on, most stuff will be debuggable


def re_bootstrap():
    if not PY3:
        return

    import builtins
    import _imp

    sys.meta_path.remove([i for i in sys.meta_path if getattr(i, '__name__', '') == 'FrozenImporter'][0])
    pathfinder = [f for f in sys.meta_path if getattr(f, '__name__', '') == 'PathFinder'][0]

    def splatmodule(fullname, path):
        spec = pathfinder.find_spec(fullname, path=[path])

        mod = types.ModuleType(spec.name)
        mod.__loader__ = spec.loader
        mod.__file__ = spec.origin
        mod.__package__ = spec.parent
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)

        return mod

    bsmod = splatmodule('importlib._bootstrap', os.path.dirname(importlib.__file__))
    bsmod._setup(sys, _imp)

    bsemod = splatmodule('importlib._bootstrap_external', os.path.dirname(importlib.__file__))
    bsemod._setup(bsmod)

    oldbs = sys.modules['importlib']

    importlib._bootstrap = bsmod
    importlib._bootstrap_external = bsemod

    del sys.modules['_frozen_importlib']
    del sys.modules['_frozen_importlib_external']
    mod = importlib.reload(oldbs)
    builtins.__import__ = importlib.__import__
    importlib.reload(importlib.util)
    # TODO: reload the various importers, path hooks, etc


if __name__ == '__main__':
    main()

