# rebootstrap

## What?

A little chunk of boilerplate that re-bootstraps the import machinery in Python 3.4+ to make it interactively debuggable.

## Why?

If you've ever needed to debug Python's import machinery (eg, if you've written custom Python loaders of any complexity), you've probably been frustrated by the fact that most Pythons ship with a frozen (ie pre-compiled native code) implementation of their import machinery. This is usually a Good Thing for performance, but a very Bad Thing if you need to step into the import machinery. The only "official" way I've found to debug it as of Python 3.8 is to build your own Python that doesn't bake in the frozen implementations of the import machinery. However, the runtime already has a fallback mechanism to use the source version if the frozen version can't be loaded. Combine Python's ability to reload modules, and a little hackery to neuter the frozen module support, and it's possible to re-bootstrap a "production" Python build to allow import to be debugged. Just run the re_bootstrap() function before you need to debug imports, and you should be good to go.

## Known Issues

We don't exhaustively go back and re-load existing code or non-import-related modules, so it's possible you can still end up stepping into some compiled import code, but most everything *can* be reloaded if you like. Once this is in place, the various modules can usually be reloaded via importlib.reload(<loaded_module_object_to_reload>).


