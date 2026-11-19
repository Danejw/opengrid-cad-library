# Third-party source attribution: native openGrid/openConnect

Native connector generator source imported **unchanged** from:

- Author: **mitufy** (https://github.com/mitufy)
- Repository: https://github.com/mitufy/opengrid-projects
- Original openGrid ecosystem creator: **David D** (https://www.printables.com/model/1214361-opengrid-walldesk-mounting-framework-and-ecosystem)
- openConnect specification: https://www.printables.com/model/1559478-openconnect-opengrids-own-connector-system
- License: **Creative Commons Attribution 4.0 International (CC BY 4.0)** for imported snap/connector generators and libraries. https://creativecommons.org/licenses/by/4.0/
- Files: `lib/opengrid_base.scad`, `lib/opengrid_threads_lib.scad`, `lib/opengrid_snap_lib.scad`, `lib/openconnect_lib.scad`, `opengrid_parametric_snap.scad`, `openconnect_plate.scad`.
- Git blob SHAs are pinned in `tests/test_native_interfaces.py`.

No modifications were made to the imported source. The project's original Python wrappers and docs remain subject to the repository MIT license.

External dependency **BOSL2** is downloaded separately in CI at pinned commit `1351a9f7e5f30a95228e580d167fd4f2e184ad2c`; it is not redistributed in this repository. Source: https://github.com/BelfrySCAD/BOSL2

The actual geometric interface is upstream authored. Fit and safety still require physical tests.
