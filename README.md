TracDuplicates
==============

Abstract
--------
TracDuplicates is a plugin for trac that will allow to dupe a bug against another generating "Marked" comments like bugzilla does in both affected bugs.

Requirements
------------
Working Trac 0.10 (tested with 0.10.4)

Installation
------------
easy_install http://github.com/nmaier/TracDuplicates/tarball/0.11

Configuration
-------------
* Enable tracduplicates.web_ui
* Add the Workflow

    [ticket]
    workflow = ConfigurableTicketWorkflow,DuplicatesWorkflow
* Add Workflow items

    [ticket-workflow]
    duplicate = * -> closed
    duplicate.operations = set_duplicate
    duplicate.name = Close as duplicate of

Code Repo
---------
http://github.com/nmaier/TracDuplicates

License
-------
BSD-style license

