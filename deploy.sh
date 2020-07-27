#!/bin/bash

#START IN PLATFORM ROOT DIR. PORTAL ROOT DIR MUST BE LOCATED IN PLATFORM'S PARENT DIR.
cd ../agriworks_portal && yarn build
cd ../agriworks_platform && eb deploy
rm -rf dist/

