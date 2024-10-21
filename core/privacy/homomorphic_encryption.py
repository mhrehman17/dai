from phe import paillier

class HomomorphicEncryption:
    def __init__(self):
        """
        Initializes the HomomorphicEncryption class, which provides methods for encryption and decryption
        using Paillier homomorphic encryption scheme.
        """
        self.public_key, self.private_key = paillier.generate_paillier_keypair()

    def encrypt(self, value: float) -> paillier.EncryptedNumber:
        """
        Encrypts a given value using the Paillier public key.
        :param value: The value to be encrypted.
        :return: EncryptedNumber representing the encrypted value.
        """
        encrypted_value = self.public_key.encrypt(value)
        print(f"Encrypted value {value} to {encrypted_value}")
        return encrypted_value

    def decrypt(self, encrypted_value: paillier.EncryptedNumber) -> float:
        """
        Decrypts an encrypted value using the Paillier private key.
        :param encrypted_value: EncryptedNumber representing the encrypted value.
        :return: The decrypted value.
        """
        decrypted_value = self.private_key.decrypt(encrypted_value)
        print(f"Decrypted value {encrypted_value} to {decrypted_value}")
        return decrypted_value

    def encrypted_addition(self, value1: paillier.EncryptedNumber, value2: paillier.EncryptedNumber) -> paillier.EncryptedNumber:
        """
        Performs homomorphic addition of two encrypted values.
        :param value1: First encrypted value.
        :param value2: Second encrypted value.
        :return: EncryptedNumber representing the result of addition.
        """
        result = value1 + value2
        print(f"Homomorphic addition of {value1} and {value2} resulted in {result}")
        return result

# Example usage
if __name__ == "__main__":
    # Initialize homomorphic encryption system
    hom_enc = HomomorphicEncryption()

    # Encrypt two values
    value1 = 15.0
    value2 = 10.0
    encrypted_value1 = hom_enc.encrypt(value1)
    encrypted_value2 = hom_enc.encrypt(value2)

    # Perform homomorphic addition
    encrypted_sum = hom_enc.encrypted_addition(encrypted_value1, encrypted_value2)

    # Decrypt the result
    decrypted_sum = hom_enc.decrypt(encrypted_sum)
    print(f"Decrypted sum: {decrypted_sum}")
