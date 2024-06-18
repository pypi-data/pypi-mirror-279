# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 18:02:11 2024

@author: Subham Divakar
"""

from OpenSSL import crypto

class PFXFileViewer:
    def __init__(self):
        pass

    def display_pfx_content(self, pfx_file, password):
        try:
            # Read the PFX file
            with open(pfx_file, 'rb') as f:
                pfx_data = f.read()
            
            # Load the PFX file
            pfx = crypto.load_pkcs12(pfx_data, password)
            
            # Get the private key
            private_key = pfx.get_privatekey()
            if private_key:
                print("Private Key:")
                print(crypto.dump_privatekey(crypto.FILETYPE_PEM, private_key).decode())
            else:
                print("No Private Key found.")
            
            # Get the certificate
            cert = pfx.get_certificate()
            if cert:
                print("Certificate:")
                print(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode())
            else:
                print("No Certificate found.")
            
            # Get additional CA certificates
            ca_certs = pfx.get_ca_certificates()
            if ca_certs:
                print("CA Certificates:")
                for ca_cert in ca_certs:
                    print(crypto.dump_certificate(crypto.FILETYPE_PEM, ca_cert).decode())
            else:
                print("No CA Certificates found.")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            
def main():
    viewer = PFXFileViewer()
    pfx_filename = input("Enter the PKCS#12 filename (with extension): ").strip()
    password = input("Enter password for PKCS#12 (leave blank if not encrypted): ").strip()
    if password == "":
        password = None

    viewer.display_pfx_content(pfx_filename, password)

if __name__ == "__main__":
    viewer = PFXFileViewer()
    pfx_filename = input("Enter the PKCS#12 filename (with extension): ").strip()
    password = input("Enter password for PKCS#12 (leave blank if not encrypted): ").strip()
    if password == "":
        password = None

    viewer.display_pfx_content(pfx_filename, password)
