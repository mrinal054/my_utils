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

#%% Decrypt
def decrypt(encrypted_im_loc, key_loc, decrypted_im_name:str='decrypted_image.jpg',
            salt_byte:int=16, key_byte:int=32, iv_byte:int=16):
    """ This function decrypt an encrypted image
    Inputs
    =========
    encrypted_im_loc (str): Entire encrypted image location including the image name with extension.
    key_loc (str): Entire key location including the image name with extension.
    decrypted_im_name (str): Name that will be used to store the decrypted image.
    salt_byte (int): Byte value for salt.
    key_byte (int): Byte value for key.
    iv_byte (int): Byte value for Initialization Vector.
    """
    # Read the encrypted data from the file
    with open(encrypted_im_loc, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
    
    # Extract the salt, IV, and ciphertext from the encrypted data
    salt = encrypted_data[:salt_byte]
    iv = encrypted_data[salt_byte:salt_byte+iv_byte]
    ct = encrypted_data[salt_byte+iv_byte:]
    
    # Read key
    with open(key_loc, 'rb') as k:
        key = k.read()
    
    # Create a Cipher object for decryption
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    
    # Create a decryptor
    decryptor = cipher.decryptor()
    
    # Decrypt the ciphertext
    padded_image_data = decryptor.update(ct) + decryptor.finalize()
    
    # Remove PKCS7 padding
    unpadder = padding.PKCS7(128).unpadder()
    image_data = unpadder.update(padded_image_data)
    try:
        image_data += unpadder.finalize()
    except ValueError:
        # Padding is not valid, so just use the unpadded data
        pass
    
    # Write the decrypted image data to a file
    with open(decrypted_im_name, 'wb') as decrypted_file:
        decrypted_file.write(image_data)

