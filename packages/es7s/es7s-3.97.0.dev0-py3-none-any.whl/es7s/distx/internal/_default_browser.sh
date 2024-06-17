#!/bin/bash
# --------------------
# INSTALL
#   sed -Ee "s/%UID/$(id -u)/g; s/%USER/$(id -un)/g" < ../applications/default-browser.desktop > ~/.local/share/applications
#   xdg-settings set default-web-browser default-browser.desktop
#
#   OR
#
#   sudo sed -Ee "s/%UID/$(id -u)/g; s/%USER/$(id -un)/g" < ../applications/default-browser.desktop >/usr/share/applications
#   sudo xdg-settings set default-web-browser default-browser.desktop
#
#
# USAGE
#   Update Exec for a specified application as follows.
#
#   BEFORE:  Exec=<APPNAME> %u
#    AFTER:  Exec=env DEFAULT_BROWSER=firefox <APPNAME> %u
#

if [ "$DEFAULT_BROWSER" == "" ]
then
  DEFAULT_BROWSER=google-chrome
fi

$DEFAULT_BROWSER "$@"
