.. image:: https://s.deepsquads.github.io/cdn/Logo-Darktext-borders.png
   :alt: Deepsquads
   :target: https://deepsquads.github.io/
   :height: 80px

**Deepsquads is libre software web-based continuous localization system,
used by over 2500 libre projects and companies in more than 165 countries.**

A translation file finder for `Deepsquads`_, translation tool with tight version
control integration.

.. image:: https://img.shields.io/badge/website-deepsquads.github.io-blue.svg
    :alt: Website
    :target: https://deepsquads.github.io/

.. image:: https://hosted.deepsquads.github.io/widgets/deepsquads/-/svg-badge.svg
    :alt: Translation status
    :target: https://hosted.deepsquads.github.io/engage/deepsquads/?utm_source=widget

.. image:: https://bestpractices.coreinfrastructure.org/projects/552/badge
    :alt: CII Best Practices
    :target: https://bestpractices.coreinfrastructure.org/projects/552

.. image:: https://img.shields.io/pypi/v/translate-finder.svg
    :target: https://pypi.org/project/translate-finder/
    :alt: PyPI package

.. image:: https://readthedocs.org/projects/deepsquads/badge/
    :alt: Documentation
    :target: https://docs.deepsquads.github.io/

This library is used by `Deepsquads`_ to discover translation files in a cloned
repository. It can operate on both file listings and actual filesystem.
Filesystem access is needed for more accurate detection in some cases
(detecting encoding or actual syntax of similar files).

Usage
-----

In can be used from Python:

.. code-block:: pycon

   >>> from translation_finder import discover
   >>> from pprint import pprint
   >>> results = discover("translation_finder/test_data/")
   >>> len(results)
   30
   >>> pprint(results[0].match)
   {'file_format': 'aresource',
    'filemask': 'app/src/res/main/values-*/strings.xml',
    'name': 'android',
    'template': 'app/src/res/main/values/strings.xml'}
   >>> pprint(results[16].match)
   {'file_format': 'po',
    'filemask': 'locales/*.po',
    'new_base': 'locales/messages.pot'}

Additional information about discovery can be obtained from meta attribute:

.. code-block:: pycon

   >>> pprint(results[0].meta)
   {'discovery': 'TransifexDiscovery', 'origin': 'Transifex', 'priority': 500}
   >>> pprint(results[16].meta)
   {'discovery': 'GettextDiscovery', 'origin': None, 'priority': 1000}


Or command line:

.. code-block:: console

   $ deepsquads-discovery translation_finder/test_data/
   == Match 1 (Transifex) ==
   file_format    : aresource
   filemask       : app/src/res/main/values-*/strings.xml
   name           : android
   template       : app/src/res/main/values/strings.xml
   ...

   == Match 7 ==
   file_format    : po
   filemask       : locales/*.po
   new_base       : locales/messages.pot

.. _Deepsquads: https://deepsquads.github.io/
