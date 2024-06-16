``nncli`` is a Python application that gives you access to your NextCloud
Notes account via the command line. It's a "hard" fork of
sncli_. You can access your notes via
a customizable console GUI that implements vi-like keybinds or via a
simple command line interface that you can script.

Notes can be viewed/created/edited in *both an* **online** *and*
**offline** *mode*. All changes are saved to a local cache on disk and
automatically sync'ed when nncli is brought online.

More detailed documentation can be found at the homepage_.

Installation
------------

Assuming your system has both ``python3`` and ``pip3``, you can
globally install ``nncli`` and its dependencies with ``pip3 install
nncli``.

If you are interested in packaging ``nncli`` for various
distributions, please consult the file CONTRIBUTING.rst_ in this
repository and reach out to the mailing list with any questions.

Features
--------

- Console GUI

  - full two-way sync with NextCloud Notes performed dynamically in the
    background
  - all actions logged and easily reviewed
  - list note titles (configurable format w/ title, date, flags, category,
    keys, etc)
  - sort notes by date, alpha by title, category, favorite on top
  - search for notes using a Google style search pattern or Regular
    Expression
  - view note contents and meta data
  - pipe note contents to external command
  - create and edit notes (using your editor)
  - edit note category
  - delete notes
  - favorite/unfavorite notes
  - vi-like keybinds (fully configurable)
  - Colors! (fully configurable)

- Command Line (scripting)

  - force a full two-way sync with NextCloud Notes
  - all actions logged and easily reviewed
  - list note titles and keys
  - search for notes using a Google style search pattern or Regular
    Expression
  - dump note contents
  - create a new note (via stdin or editor)
  - import a note with raw json data (stdin or editor)
  - edit a note (via editor)
  - delete a note
  - favorite/unfavorite a note
  - view and edit note category

Acknowledgements
----------------

nncli is a fork of sncli_ by Eric Davis. This application further pulls
in and uses modified versions of the simplenote.py_ module by Daniel
Schauenberg and the notes_db.py module from nvpy_ by Charl P. Botha.

.. _homepage: https://nncli.org
.. _sncli: https://github.com/insanum/sncli
.. _CONTRIBUTING.rst: https://git.danielmoch.com/nncli/tree/CONTRIBUTING.rst
.. _Python 3: http://python.org
.. _Urwid: http://urwid.org
.. _Requests: https://requests.readthedocs.org/en/master
.. _simplenote.py: https://github.com/mrtazz/simplenote.py
.. _nvpy: https://github.com/cpbotha/nvpy
