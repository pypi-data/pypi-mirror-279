Change Log
##########

..
   All enhancements and patches to video_iframe will be documented
   in this file.  It adheres to the structure of https://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   This project adheres to Semantic Versioning (https://semver.org/).

.. There should always be an "Unreleased" section for changes pending release.

Unreleased
**********

* 

1.0.0 – 2024-06-18
**********************************************

Added
=====

* Author view to display custom message with instructions if no video url is detected. Also disable validations for author view to supress default validation failure messages.

Removed
=======

* `autoplay` from allow attribute passed to the iframe.

Changed
=======

* Title of `display_name` field to `Video Title` and modified the description.
* Default display name of the XBlock as displayed in the Advanced XBlocks selection list from `Video` to `Video Iframe`.


0.1.0 – 2024-04-28
**********************************************

Added
=====

* First iteration of XBlock.
