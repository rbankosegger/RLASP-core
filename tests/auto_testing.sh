#!/bin/sh

# Hide pygame support prompt 
# export PYGAME_HIDE_SUPPORT_PROMPT=1

# Find all *.py and *.lp files in the parent directory (and subdirectories).
# Whenever one of those files changes, re-run the unit tests in this directory.
(find .. -name "*.py" && find .. -name "*.lp") | entr ./run_tests.sh
