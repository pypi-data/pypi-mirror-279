#! /bin/sh

# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

TOOL_DIR=$1
shift

mkdir -p /tmp/overlay
mount -t tmpfs tmpfs /tmp/overlay
mkdir -p /tmp/overlay/upper
mkdir -p /tmp/overlay/work
mkdir -p /home/_cwd

# We mount the weck_cache to /home/weck_cache in the container
cp -r "/home/weck_cache/$TOOL_DIR" /tmp/overlay/

# Assume workdir is /home/cwd
# Assume the user $PWD is mounted to home/cwd
#Mount the overlay
mount -t overlay overlay -o lowerdir=/home/cwd:/tmp/overlay/"$TOOL_DIR",upperdir=/tmp/overlay/upper,workdir=/tmp/overlay/work /home/_cwd
cd /home/_cwd && "$@"

# Copy the output from the tool back to the users cwd
[ ! -d /home/cwd/output ] && mkdir /home/cwd/output
cp -r /tmp/overlay/upper/* /home/cwd/output
