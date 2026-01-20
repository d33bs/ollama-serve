# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import pathlib
import sys

try:
    import pydata_sphinx_theme
except ImportError:  # pragma: no cover - doc build fallback
    pydata_sphinx_theme = None

try:
    import myst_parser  # noqa: F401
except ImportError as exc:  # pragma: no cover - doc build fallback
    raise RuntimeError(
        "myst_parser is required to build the Markdown docs. "
        "Install it with the docs dependencies."
    ) from exc

basedir = str(pathlib.Path(__file__).parent.parent.parent.resolve())

sys.path.insert(0, basedir)

# -- Project information -----------------------------------------------------

project = "ollama-serve"
# is used here due to sphinx decision-making: https://github.com/sphinx-doc/sphinx/issues/8132
copyright = "2024, DBMI Community"  # noqa: A001
author = "DBMI Community"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
]
if pydata_sphinx_theme is not None:
    extensions.append("pydata_sphinx_theme")

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []  # type: ignore

root_doc = "index"
master_doc = "index"
source_suffix = {
    ".md": "markdown",
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "pydata_sphinx_theme" if pydata_sphinx_theme is not None else "alabaster"

if pydata_sphinx_theme is not None:
    html_theme_options = {
        "header_links_before_dropdown": 5,
        "icon_links": [
            {
                "name": "GitHub",
                "url": "https://github.com/d33bs/ollama-serve",
                "icon": "fa-brands fa-github",
            },
        ],
        "logo": {"text": "ollama-serve"},
        "use_edit_page_button": False,
        "show_toc_level": 1,
        "navbar_align": "left",
        "navbar_center": ["navbar-nav"],
        "footer_start": ["copyright"],
        "footer_center": ["sphinx-version"],
        "secondary_sidebar_items": {
            "**/*": ["page-toc", "edit-this-page", "sourcelink"],
        },
    }
else:
    html_theme_options = {}

# set option to avoid rendering default variables
autodoc_preserve_defaults = True
