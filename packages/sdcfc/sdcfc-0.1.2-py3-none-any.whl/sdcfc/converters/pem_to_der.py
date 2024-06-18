# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 11:51:25 2024

@author: Subham Divakar
"""

from cryptography.hazmat.primitives.serialization import load_pem_private_key, Encoding, PrivateFormat
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

class PEMtoDERConverter:
    def __init__(self):
        pass

    def convert(self, pem_file, der_file):
        try:
            with open(pem_file, "rb") as f:
                pem_data = f.read()
                private_key = load_pem_private_key(pem_data, password=None, backend=default_backend())
                der_data = private_key.private_bytes(
                    encoding=Encoding.DER,
                    format=PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
                with open(der_file, "wb") as df:
                    df.write(der_data)
        except FileNotFoundError:
            print(f"Error: File '{pem_file}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    converter = PEMtoDERConverter()
    pem_filename = input("Enter the PEM filename: ").strip()
    der_filename = input("Enter the DER filename to save: ").strip()
    converter.convert(pem_filename, der_filename)
    print(f"Conversion from PEM to DER complete. Output saved to {der_filename}.")

