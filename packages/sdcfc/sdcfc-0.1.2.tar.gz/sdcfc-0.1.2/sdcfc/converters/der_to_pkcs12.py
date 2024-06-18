# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 12:02:26 2024

@author: Subham Divakar
"""

from OpenSSL import crypto

class DERtoPKCS12Converter:
    def __init__(self):
        pass

    def convert(self, der_cert_file, der_key_file, pkcs12_file, password=None):
        try:
            # Read the DER-encoded certificate
            with open(der_cert_file, 'rb') as f:
                der_cert_data = f.read()
                cert = crypto.load_certificate(crypto.FILETYPE_ASN1, der_cert_data)
            
            # Read the DER-encoded private key
            with open(der_key_file, 'rb') as f:
                der_key_data = f.read()
                private_key = crypto.load_privatekey(crypto.FILETYPE_ASN1, der_key_data)
            
            # Create a PKCS#12 object
            pkcs12 = crypto.PKCS12()
            pkcs12.set_certificate(cert)
            pkcs12.set_privatekey(private_key)

            # Set the password if provided
            if password:
                pkcs12_data = pkcs12.export(passphrase=password.encode())
            else:
                pkcs12_data = pkcs12.export()
            
            # Write the PKCS#12 data to the output file
            with open(pkcs12_file, 'wb') as pf:
                pf.write(pkcs12_data)
            
            print(f"Conversion from DER to PKCS#12 complete. Output saved to {pkcs12_file}.")
        except FileNotFoundError:
            print(f"Error: File '{der_cert_file}' or '{der_key_file}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    converter = DERtoPKCS12Converter()
    der_cert_filename = input("Enter the DER certificate filename (with extension): ").strip()
    der_key_filename = input("Enter the DER private key filename (with extension): ").strip()
    pkcs12_filename = input("Enter the PKCS#12 filename to save (with extension): ").strip()
    password = input("Enter password for PKCS#12 (leave blank for no encryption): ").strip()
    if password == "":
        password = None
    converter.convert(der_cert_filename, der_key_filename, pkcs12_filename, password)

if __name__ == "__main__":
    converter = DERtoPKCS12Converter()
    der_cert_filename = input("Enter the DER certificate filename (with extension): ").strip()
    der_key_filename = input("Enter the DER private key filename (with extension): ").strip()
    pkcs12_filename = input("Enter the PKCS#12 filename to save (with extension): ").strip()
    password = input("Enter password for PKCS#12 (leave blank for no encryption): ").strip()
    if password == "":
        password = None
    converter.convert(der_cert_filename, der_key_filename, pkcs12_filename, password)

