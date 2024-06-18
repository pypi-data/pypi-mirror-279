# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 11:54:06 2024

@author: Subham Divakar
"""

from cryptography.hazmat.primitives.serialization import load_der_private_key, Encoding, PrivateFormat
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

class DERtoPEMConverter:
    def __init__(self):
        pass

    def convert(self, der_file, pem_file):
        try:
            with open(der_file, "rb") as f:
                der_data = f.read()
                private_key = load_der_private_key(der_data, password=None, backend=default_backend())
                pem_data = private_key.private_bytes(
                    encoding=Encoding.PEM,
                    format=PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
                with open(pem_file, "wb") as pf:
                    pf.write(pem_data)
        except FileNotFoundError:
            print(f"Error: File '{der_file}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    converter = DERtoPEMConverter()
    der_filename = input("Enter the DER filename: ").strip()
    pem_filename = input("Enter the PEM filename to save: ").strip()
    converter.convert(der_filename, pem_filename)
    print(f"Conversion from DER to PEM complete. Output saved to {pem_filename}.")
