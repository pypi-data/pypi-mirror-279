# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 12:00:52 2024

@author: Subham Divakar
"""

# main.py
from .converters.pem_to_der import PEMtoDERConverter
from .converters.der_to_pem import DERtoPEMConverter
from .converters.der_to_pkcs12 import main as der_to_pkcs12_main
from .converters.pem_to_pkcs12 import PEMtoPKCS12Converter
from .converters.pem_to_pkcs12 import main as pem_to_pkcs12_main
from .converters.pkcs12_to_pem import PKCS12toPEMConverter
from .converters.der_to_pkcs12 import DERtoPKCS12Converter
from .PKCS12viewer import main as pkcs12_viewer

def main():
    print("Welcome to the Secure Data - Certificate Format Converter (SD-CFC)!")
    print("SD-CFC is a powerful tool for managing certificate files.")
    print("It offers seamless conversion between PEM, DER, and PKCS12 formats.")
    print("Whether you need to convert, or manage certificates,")
    print("SD-CFC provides a user-friendly interface to streamline your workflow securely.")

    print("This tool converts certs from one format(PEM, DER, PKCS12) files to other formats(PEM, DER, PKCS12).\n")
    
    print("Created by Subham Divakar\n")
    print("Connect with me:")
    print("- LinkedIn: https://www.linkedin.com/in/subham-divakar-a7420a12a/")
    print("- GitHub: https://github.com/shubham10divakar")
    print("- Portfolio: https://shubham10divakar.github.io/showcasehub/")
    print("\n")
    
    print("1. Convert PEM to DER")
    print("2. Convert DER to PEM")
    print("3. Convert PEM to PKCS#12")
    print("4. Convert PKCS#12 to PEM")
    print("5. Convert DER to PKCS#12")
    print("6. Open and View PKCS#12 file contents")
    print("0. Exit")
    choice = input("Enter your choice: ").strip()

    if choice == '1':
        pem_filename = input("Enter the PEM filename (with extension): ").strip()
        if not pem_filename.lower().endswith(".key") and not pem_filename.lower().endswith(".pem") and not pem_filename.lower().endswith(".cer"):
            print("Incorrect File Format. PEM files are generally ones ending with .pem, .cer or .crt")
            return
        
        der_filename = input("Enter the DER filename to save (with extension): ").strip()
        if not der_filename.lower().endswith("der") and not der_filename.lower().endswith("cer"):
            print("Incorrect File Format. DER files are generally ones ending with .der or .cer")
            return
        
        converter = PEMtoDERConverter()
        converter.convert(pem_filename, der_filename)
        print(f"Conversion from PEM to DER complete. Output saved to {der_filename}.")
    elif choice == '2':
        der_filename = input("Enter the DER filename (with extension): ").strip()
        if not der_filename.lower().endswith("der") and not der_filename.lower().endswith("cer"):
            print("Incorrect File Format. DER files are generally ones ending with .der or .cer")
            return
        
        pem_filename = input("Enter the PEM filename to save (with extension): ").strip()
        if not pem_filename.lower().endswith(".key") and not pem_filename.lower().endswith(".pem") and not pem_filename.lower().endswith(".cer"):
            print("Incorrect File Format. PEM files are generally ones ending with .pem, .cer or .crt")
            return
            
        converter = DERtoPEMConverter()
        converter.convert(der_filename, pem_filename)
        print(f"Conversion from DER to PEM complete. Output saved to {pem_filename}.")
    elif choice == '3':
        pem_to_pkcs12_main()
        
    elif choice == '4':
        pkcs12_filename = input("Enter the PKCS#12 filename (with extension): ").strip()
        if not pkcs12_filename.lower().endswith("pfx") and not pkcs12_filename.lower().endswith("p12"):
            print("Incorrect File Format. PKCS#12 files are generally ones ending with .p12 or .pfx")
            return
            
        pem_filename = input("Enter the PEM filename to save (with extension): ").strip()
        if not pem_filename.lower().endswith(".key") and not pem_filename.lower().endswith(".pem") and not pem_filename.lower().endswith(".cer"):
            print("Incorrect File Format. PEM files are generally ones ending with .pem, .cer or .crt")
            return
            
        password = input("Enter password for PKCS#12 (leave blank if not encrypted): ").strip()
        converter = PKCS12toPEMConverter()
        converter.convert(pkcs12_filename, pem_filename, password)
        print(f"Conversion from PKCS#12 to PEM complete. Output saved to {pem_filename}.")
    elif choice == '5':
        der_to_pkcs12_main()
        
    elif choice == '6':
        pkcs12_viewer()
        #print('')
    elif choice == '0':
        print("Exiting (SD-CFC) === Secure Data - Certificate Format Converter Tool ===\n")
        print("Feedbacks are welcome.\n")
        print("Created by Subham Divakar\n")
        print("Connect with me:")
        print("- LinkedIn: https://www.linkedin.com/in/subham-divakar-a7420a12a/")
        print("- GitHub: https://github.com/shubham10divakar")
        print("- Portfolio: https://shubham10divakar.github.io/showcasehub/")
        print("\n")
    else:
        print("Invalid choice. Please enter a number between 1 and 5")


if __name__ == "__main__":
    main()