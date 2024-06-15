#!/bin/bash
# Change the owner and permissions of the /root directory
chown -R $(id -u):$(id -g) /root
chmod -R 755 /root

# Run the command provided as arguments
exec "$@"