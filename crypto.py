""" 
This code is to encrypt and decrypt image(s).
Author: Mrinal Kanti Dhar
Co-author: ChatGPT
"""

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def encryt(im_loc, encrypted_im_name:str='encrypted_image.bin', key_name:str='key.bin',            
           salt_byte:int=16, key_byte:int=32, iv_byte:int=16):
    
    """ This function encrypts an input
    
    Inputs
    ========
    im_loc (str): Entire image location including the image name with extension.
    encrypted_im_name (str): Name that will be used to store the encrypted image.
    key_name (str): Name that will be used to store the key.
    salt_byte (int): Byte value for salt that will be added to the input image. The value indicates a byte value.
    key_byte (int): Byte value to generate key randomly.
    iv_byte (int): Byte value to generate Initialization Vector randomly.    
    
    """
    
    # Generate a random salt
    salt = os.urandom(salt_byte) # 16 bytes
    
    key = os.urandom(key_byte) # 32 bytes
    
    iv = os.urandom(iv_byte) # 16 bytes
    
    # Create a Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    
    # Create an encryptor
    encryptor = cipher.encryptor()
    
    # Read the image data
    with open(im_loc, 'rb') as img_file:
        image_data = img_file.read()
    
    # Apply PKCS7 padding to the image data
    padder = padding.PKCS7(128).padder()
    padded_image_data = padder.update(image_data) + padder.finalize()
    
    # Encrypt the padded image data
    ct = encryptor.update(padded_image_data) + encryptor.finalize()
    
    # Write the encrypted data to a file
    with open(encrypted_im_name, 'wb') as encrypted_file:
        encrypted_file.write(salt + iv + ct)
    
    # save the key
    with open(key_name, "wb") as k:
        k.write(key)

