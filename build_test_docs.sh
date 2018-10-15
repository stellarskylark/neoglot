#!/bin/bash
(cd docs && sphinx-build . .build -nW)
touch docs/.build/.nojekyll
