# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 12:01:56 2024

@author: Subham Divakar
"""

import os
from OpenSSL import crypto

class PKCS12toPEMConverter:
    def __init__(self):
        pass

    def convert(self, pkcs12_file, pem_file, password=None):
        try:
            if not os.path.exists(pkcs12_file):
                raise FileNotFoundError(f"File '{pkcs12_file}' not found.")

            with open(pkcs12_file, 'rb') as f:
                pkcs12_data = f.read()

            p12 = crypto.load_pkcs12(pkcs12_data, password)

            with open(pem_file, 'wb') as f:
                f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey()))

        except FileNotFoundError as e:
            print(f"Error: {e}")
        except crypto.Error as e:
            print(f"Error in OpenSSL: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    converter = PKCS12toPEMConverter()
    pkcs12_filename = input("Enter the PKCS#12 filename (without extension): ").strip() + ".pfx"
    pem_filename = input("Enter the PEM filename to save (without extension): ").strip() + ".pem"
    password = input("Enter password for PKCS#12 (leave blank if not encrypted): ").strip()
    converter.convert(pkcs12_filename, pem_filename, password)
    print(f"Conversion from PKCS#12 to PEM complete. Output saved to {pem_filename}.")
