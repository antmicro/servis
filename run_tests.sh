#!/bin/bash

error=0
for test in tests/test*.py
do
  echo "python3 ${test}"
  if ! python3 ${test}
  then
    error=1
  fi
done
exit ${error}
