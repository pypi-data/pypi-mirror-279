from setuptools import setup

name = "types-seaborn"
description = "Typing stubs for seaborn"
long_description = '''
## Typing stubs for seaborn

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`seaborn`](https://github.com/mwaskom/seaborn) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`seaborn`.

This version of `types-seaborn` aims to provide accurate annotations
for `seaborn==0.13.2`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/seaborn. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `212af7a526f07feacbf5cbb3a77e4246f7b1ede7` and was tested
with mypy 1.10.0, pyright 1.1.367, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="0.13.2.20240618",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/seaborn.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['matplotlib>=3.8', 'numpy<2,>=1.20', 'pandas-stubs'],
      packages=['seaborn-stubs'],
      package_data={'seaborn-stubs': ['__init__.pyi', '_core/__init__.pyi', '_core/data.pyi', '_core/exceptions.pyi', '_core/groupby.pyi', '_core/moves.pyi', '_core/plot.pyi', '_core/properties.pyi', '_core/rules.pyi', '_core/scales.pyi', '_core/subplots.pyi', '_core/typing.pyi', '_marks/__init__.pyi', '_marks/area.pyi', '_marks/bar.pyi', '_marks/base.pyi', '_marks/dot.pyi', '_marks/line.pyi', '_marks/text.pyi', '_stats/__init__.pyi', '_stats/aggregation.pyi', '_stats/base.pyi', '_stats/counting.pyi', '_stats/density.pyi', '_stats/order.pyi', '_stats/regression.pyi', 'algorithms.pyi', 'axisgrid.pyi', 'categorical.pyi', 'cm.pyi', 'colors/__init__.pyi', 'colors/crayons.pyi', 'colors/xkcd_rgb.pyi', 'distributions.pyi', 'external/__init__.pyi', 'external/appdirs.pyi', 'external/docscrape.pyi', 'external/husl.pyi', 'external/kde.pyi', 'external/version.pyi', 'matrix.pyi', 'miscplot.pyi', 'objects.pyi', 'palettes.pyi', 'rcmod.pyi', 'regression.pyi', 'relational.pyi', 'utils.pyi', 'widgets.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
