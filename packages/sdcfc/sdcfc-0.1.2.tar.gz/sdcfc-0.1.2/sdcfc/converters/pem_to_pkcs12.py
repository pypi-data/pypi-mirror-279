from OpenSSL import crypto
import os

class PEMtoPKCS12Converter:
    def __init__(self):
        pass

    def convert(self, pem_key_file, pem_cert_file, pkcs12_file, password=None):
        try:
            # Load PEM private key
            with open(pem_key_file, "rb") as kf:
                pem_key_data = kf.read()
                private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, pem_key_data)

            # Load PEM certificate
            with open(pem_cert_file, "rb") as cf:
                pem_cert_data = cf.read()
                cert = crypto.load_certificate(crypto.FILETYPE_PEM, pem_cert_data)

            # Create a PKCS#12 object
            pkcs12 = crypto.PKCS12()
            pkcs12.set_privatekey(private_key)
            pkcs12.set_certificate(cert)

            # Dump the PKCS#12 object to binary
            pkcs12_data = pkcs12.export(passphrase=password)

            # Save the PKCS#12 file
            with open(pkcs12_file, "wb") as pf:
                pf.write(pkcs12_data)

            print(f"Conversion from PEM to PKCS#12 complete. Output saved to {pkcs12_file}.")
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except crypto.Error as e:
            print(f"An error occurred with OpenSSL: {e}")

def main():
    converter = PEMtoPKCS12Converter()
    pem_key_filename = input("Enter the PEM key filename (without extension): ").strip()
    pem_cert_filename = input("Enter the PEM certificate filename (without extension): ").strip()
    pkcs12_filename = input("Enter the PKCS#12 filename to save (without extension): ").strip()
    password = input("Enter password for PKCS#12 (leave blank for no encryption): ").strip()
    if password == "":
        password = None

    converter.convert(pem_key_filename, pem_cert_filename, pkcs12_filename, password)
    

if __name__ == "__main__":
    converter = PEMtoPKCS12Converter()
    pem_key_filename = input("Enter the PEM key filename (without extension): ").strip() + ".pem"
    pem_cert_filename = input("Enter the PEM certificate filename (without extension): ").strip() + ".pem"
    pkcs12_filename = input("Enter the PKCS#12 filename to save (without extension): ").strip() + ".p12"
    password = input("Enter password for PKCS#12 (leave blank for no encryption): ").strip()
    if password == "":
        password = None

    converter.convert(pem_key_filename, pem_cert_filename, pkcs12_filename, password)
