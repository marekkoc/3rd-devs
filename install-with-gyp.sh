#!/bin/bash

# Add npm global bin to path
export PATH="$PATH:$(npm root -g)/../bin"

# Find node-gyp and make sure it's in path
NODE_GYP_PATH=$(which node-gyp || find /usr -name node-gyp -type f 2>/dev/null | head -1)
if [ -n "$NODE_GYP_PATH" ]; then
  echo "Found node-gyp at: $NODE_GYP_PATH"
  # Add node-gyp directory to PATH
  export PATH="$(dirname $NODE_GYP_PATH):$PATH"
else
  echo "node-gyp not found, attempting to install..."
  sudo npm install -g node-gyp --unsafe-perm=true --allow-root
  export PATH="$PATH:$(npm root -g)/../bin"
fi

# Set environment variables
export BUN_INSTALL_NATIVE_MODULES=1
export PYTHON=$(which python3)
export NODE_GYP_FORCE_PYTHON=$(which python3)

# Verify node-gyp is accessible
echo "Checking node-gyp availability:"
which node-gyp
node-gyp --version

# Run bun install
echo "Running bun install with native modules support..."
bun install

