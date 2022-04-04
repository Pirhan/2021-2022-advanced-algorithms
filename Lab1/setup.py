from distutils.core import setup
from Cython.Build import cythonize

setup(
        ext_modules=cythonize(["algorithms_compiled.pyx", "data_structures/graph_compiled.pyx", "data_structures/unionFind_compiled.pyx"], annotate=True))
