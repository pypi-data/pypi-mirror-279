import Cryptodome.PublicKey.RSA
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256

class rsa:


    def __init__(self, private_key = None):
        if private_key == None:
            self.private_key, self.public_key  = self.generate_key_pair()
        else:
            self.private_key, self.public_key = self.generate_from_existing_key(private_key)

    def generate_from_existing_key(self, private_key):
        private_key = RSA.import_key(private_key)
        public_key = private_key.public_key()
        return private_key, public_key

    def test_if_key_is_right(self):
        if type(self.public_key) != RSA.RsaKey:
            self.public_key = Cryptodome.PublicKey.RSA.importKey(self.public_key)
        if type(self.private_key) != RSA.RsaKey:
            self.private_key = Cryptodome.PublicKey.RSA.import_key(self.private_key)
        print(type(self.private_key))

    def return_keys(self):
        return self.private_key, self.public_key

    def return_string_keys(self):
        return self.private_key.export_key().decode('utf-8'), self.public_key.export_key().decode('utf-8')

    def generate_key_pair(self):
        key = RSA.generate(2048)
        private_key = key
        public_key = key.publickey()
        return private_key, public_key

    def rsa_sign(self, plaintext):
        self.test_if_key_is_right()
        h = SHA256.new(plaintext.encode('utf-8'))
        signature = pkcs1_15.new(self.private_key).sign(h)
        return signature

    def rsa_verify(self, plaintext, signature):
        self.test_if_key_is_right()
        h = SHA256.new(plaintext.encode('utf-8'))
        try:
            pkcs1_15.new(self.public_key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False