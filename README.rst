Motivation
----------

Suppose you want to import the contents of A.ipynb into B.ipynb.

Installation
------------

.. code:: bash

    pip install import-ipynb

How to use
----------

Place both ipynb files in the same directory. Then, in the B.ipynb:

.. code:: python

    import import_ipynb
    import A

Congratulations! You can now run any functions defined in A.ipynb from
B.ipynb!

How it works
------------

The code within import\_ipynb.py defines a "notebook loader" that allows
you to 'import' other ipynb files into your current ipynb file. This
entails:

1. load the notebook document into memory
2. create an empty Module
3. execute every cell in the Module namespace

Note that since every cell in the A.ipynb is executed when you import
the the file, A.ipynb should only contain classes and function
definitions (otherwise you'll end up loading all variables and data into
memory).

Credits
-------

The code within imoprt\_ipynb.py comes from
http://jupyter-notebook.readthedocs.io/en/latest/examples/Notebook/Importing%20Notebooks.html.

Riley F. Edmunds (@rileyedmunds) wrote instructions on how to use it
and Lev Maximov (@axil) packaged it.
