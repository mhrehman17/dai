#!/bin/bash

# This script generates RSA private and public keys for secure communication within the decentralized AI system.
# It uses OpenSSL to create a key pair, which can be used for encryption, authentication, and other cryptographic tasks.

# Define output directory for storing the keys
OUTPUT_DIR="keys"

# Define filenames for the keys
PRIVATE_KEY_FILE="private_key.pem"
PUBLIC_KEY_FILE="public_key.pem"

# Create the output directory if it doesn't exist
if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
    echo "Created directory: $OUTPUT_DIR"
fi

# Generate the RSA private key
openssl genpkey -algorithm RSA -out "$OUTPUT_DIR/$PRIVATE_KEY_FILE" -aes256 -pass pass:password123
if [ $? -eq 0 ]; then
    echo "Private key generated successfully: $OUTPUT_DIR/$PRIVATE_KEY_FILE"
else
    echo "Error: Failed to generate private key"
    exit 1
fi

# Generate the corresponding public key
openssl rsa -pubout -in "$OUTPUT_DIR/$PRIVATE_KEY_FILE" -out "$OUTPUT_DIR/$PUBLIC_KEY_FILE" -passin pass:password123
if [ $? -eq 0 ]; then
    echo "Public key generated successfully: $OUTPUT_DIR/$PUBLIC_KEY_FILE"
else
    echo "Error: Failed to generate public key"
    exit 1
fi

# Secure the private key
chmod 600 "$OUTPUT_DIR/$PRIVATE_KEY_FILE"
echo "Permissions set for private key to be read/write only by the owner"

# Completion message
echo "Key generation completed successfully. Keys are available in the '$OUTPUT_DIR' directory."
