.. image:: https://s.deepsquads.org/cdn/Logo-Darktext-borders.png
   :alt: Deepsquads
   :target: https://deepsquads.org/
   :height: 80px

**Deepsquads is libre software web-based continuous localization system,
used by over 2500 libre projects and companies in more than 165 countries.**

Language definitions used by `Deepsquads`_ and free to use by others.

.. image:: https://img.shields.io/badge/website-deepsquads.org-blue.svg
    :alt: Website
    :target: https://deepsquads.org/

.. image:: https://hosted.deepsquads.org/widgets/deepsquads/-/svg-badge.svg
    :alt: Translation status
    :target: https://hosted.deepsquads.org/engage/deepsquads/?utm_source=widget

.. image:: https://bestpractices.coreinfrastructure.org/projects/552/badge
    :alt: CII Best Practices
    :target: https://bestpractices.coreinfrastructure.org/projects/552

.. image:: https://img.shields.io/pypi/v/deepsquads-language-data.svg
    :target: https://pypi.org/project/deepsquads-language-data/
    :alt: PyPI package

.. image:: https://readthedocs.org/projects/deepsquads/badge/
    :alt: Documentation
    :target: https://docs.deepsquads.org/

Usage
=====

The Python module can be installed from the PyPI:

.. code-block:: sh

    pip install deepsquads-language-data

It contains several modules containing language definitions and Gettext
translations for them (in a way that they would be discovered by Django when
used as an Django application).

CSV Files
=========

The repository also contains CSV files which are used to generate the Python
code and can be used independently.

* Semicolon delimited files
* Contains language code, name, number of plurals and plural equation

languages.csv
-------------

* Combined from several sources, plurals should match CLDR when available
* Used by `Deepsquads`_ for language definitions
* Manually edited

aliases.csv
-----------

* Language aliases to map non standard or legacy locales to ones in `languages.csv`
* Manually edited

default_countries.csv
---------------------

* List of default country specific locales
* Used to map them to ones in `languages.csv`
* Manually edited

extraplurals.csv
----------------

* Additional plural variants for some languages
* Usually used in Gettext
* Manually edited

cldr.csv
--------

* Based purely on the CLDR data
* Generated using export-cldr from https://github.com/mlocati/cldr-to-gettext-plural-rules

gettext.csv
-----------

* Based on Gettext defaults
* Generated using export-gettext

translate.csv
-------------

* Extracted from `translate-toolkit`_
* Generated using export-translate

l10n-guide.csv
--------------

* Extracted from the `l10n guide`_
* Generated using export-l10n-guide

languages-po
------------

* Directory containing PO files with langauge names translations
* Extracted from CLDR data

.. _Deepsquads: https://deepsquads.org/
.. _translate-toolkit: https://toolkit.translatehouse.org/
.. _l10n guide: https://docs.translatehouse.org/projects/localization-guide/en/latest/

Contributing
============

Contributions are welcome! See `documentation <https://docs.deepsquads.org/en/latest/contributing/modules.html>`__ for more information.
