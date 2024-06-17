
.. image:: https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg
    :align: center
    :height: 200
    :alt: logo  


.. image:: https://img.shields.io/pypi/v/chatInsights.svg
    :target: https://pypi.org/project/chatInsights/ 

.. image:: https://img.shields.io/pypi/pyversions/chatInsights.svg
    :target: https://pypi.org/project/chatInsights/

.. image:: https://github.com/ronylpatil/chatInsights/actions/workflows/ci_pipeline.yaml/badge.svg
    :target: https://github.com/ronylpatil/chatInsights/actions?query=workflow%3Atest

.. image:: https://github.com/ronylpatil/chatInsights/actions/workflows/cd_pipeline.yaml/badge.svg
    :target: https://github.com/ronylpatil/chatInsights/actions?query=workflow%3Atest


The ``chatInsights`` package make it easy to perform whatsApp group chat analysis using python.

A simple code example:

.. code-block:: python

       # import chatInsights class
       from chatInsights import ChatInsights
       
       # create obj of ChatInsights class
       obj = ChatInsights(r'E:/chat.txt')
       obj.active_users()
       obj.active_year()
       obj.active_month()
       obj.active_day()
       obj.word_cloud()


.. list-table::
    :widths: 33 33 33
    :header-rows: 0

    * - .. image:: https://raw.githubusercontent.com/ronylpatil/chatInsights/main/doc/en/active_users.png
          :width: 330px
          :height: 190px
      - .. image:: https://raw.githubusercontent.com/ronylpatil/chatInsights/main/doc/en/active_year.png
          :width: 330px
          :height: 190px
      - .. image:: https://raw.githubusercontent.com/ronylpatil/chatInsights/main/doc/en/active_month.png
          :width: 330px
          :height: 190px
    * - .. image:: https://raw.githubusercontent.com/ronylpatil/chatInsights/main/doc/en/active_day.png
          :width: 330px
          :height: 190px
      - .. image:: https://raw.githubusercontent.com/ronylpatil/chatInsights/main/doc/en/wordcloud.png
          :width: 330px
          :height: 190px
      -


Features
--------
- User activity stats
- Weekly message stats
- Monthly message stats
- Yearly message stats
- Word Cloud


Documentation
-------------

Updated soon.


Bugs/Requests
-------------

Please use the `GitHub issue tracker <https://github.com/ronylpatil/chatInsights/issues>`_ to submit bugs or request features.


Changelog
---------

Consult the `Changelog <https://github.com/ronylpatil/chatInsights/releases>`__ page for fixes and enhancements of each version.


License
-------

Distributed under the terms of the `MIT`_ license.


.. _`MIT`: https://raw.githubusercontent.com/ronylpatil/chatInsights/main/LICENSE
