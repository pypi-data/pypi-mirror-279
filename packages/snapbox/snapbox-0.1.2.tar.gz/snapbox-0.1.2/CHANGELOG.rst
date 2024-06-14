Release history and notes
=========================

`Sequence based identifiers
<http://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_
are used for versioning (schema follows below):

.. code-block:: text

    major.minor[.revision]

- It's always safe to upgrade within the same minor version (for example, from
  0.3 to 0.3.4).
- Minor version changes might be backwards incompatible. Read the
  release notes carefully before upgrading (for example, when upgrading from
  0.3.4 to 0.4).
- All backwards incompatible changes are mentioned in this document.

0.1.2
-----
2024-06-14

- Export altered images.

0.1.1
-----
2024-06-13

- Various UI improvements (add zoom controls).
- Make the box line configurable (colour, thickness).
- Add tests.

0.1
---
2024-06-12

- Initial beta release.
