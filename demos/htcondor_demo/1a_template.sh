#!/bin/sh

. env-rlasp/bin/activate
rlasp-train {args_imported_by_python}
deactivate
