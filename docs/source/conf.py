# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from unittest import mock

import sphinx_pdj_theme
MOCK_MODULES = ['PyQt5', 'PyQt5.QtWidgets', 'PyQt5.QtGui', 'PyQt5.QtCore']
sys.modules.update((mod_name, mock.Mock()) for mod_name in MOCK_MODULES)
sys.path.insert(0, os.path.abspath('../../src'))

project = 'AI Field Commander'
copyright = '2024, Jakub Buszyński'
author = 'Jakub Buszyński'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'sphinx.ext.viewcode']

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'renku'
# html_theme_path = [sphinx_pdj_theme.get_html_theme_path()]
html_static_path = ['_static']