#!/bin/bash

# Read the requirements.txt file line by line
while IFS= read -r line; do
    # Attempt to install the library
    echo "Attempting to install: $line"
    pip install "$line"
    # Check the return code of the pip command
    if [ $? -ne 0 ]; then
        echo "Failed to install: $line"
    fi
done < requirements.txt
