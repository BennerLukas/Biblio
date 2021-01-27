#!/bin/sh
set -o errexit -o nounset -o pipefail

cd /dockerised-example

flask run --host=0.0.0.0