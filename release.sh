#!/bin/bash

TEMP_DIR=`mktemp -d`

PLUGIN_NAME=plugin.audio.lbc_audioagain
PLUGIN_VERSION=$1

PLUGIN_FILE=$PLUGIN_NAME-$PLUGIN_VERSION.zip

BUILD_DIR=$TEMP_DIR/$PLUGIN_NAME

mkdir $BUILD_DIR

rsync --archive --verbose --exclude release.sh --exclude *.svn* . $BUILD_DIR

cd $TEMP_DIR

zip -rv $PLUGIN_FILE $PLUGIN_NAME

cd -

cp $TEMP_DIR/$PLUGIN_FILE .

rmdir /s /q $TEMP_DIR
