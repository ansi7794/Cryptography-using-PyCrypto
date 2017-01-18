import os
import random

from Crypto.Cipher import AES
from Crypto.Hash import SHA256

def encrypt(key, filename):
	part_size = 65536
	output_file = "(encrypted)"+filename
	file_size = str(os.path.getsize(filename)).zfill(16)
	IV = ''

	for i in range(16):
		IV += chr(random.randint(0,0xFF))

	encryptor = AES.new(key, AES.MODE_CBC, IV)

	with open(filename, 'rb') as infile:
		with open(output_file, 'wb') as outfile:
			outfile.write(file_size)
			outfile.write(IV)

			while True:
				part = infile.read(part_size)
				if len(part) == 0:
					break
				elif len(part) % 16 != 0:
					part += ' ' * (16 - (len(part)%16))

				outfile.write(encryptor.encrypt(part))


def decrypt(key,filename):
	part_size = 65536
	output_file = filename[11:]

	with open(filename, 'rb') as infile:
		file_size = long(infile.read(16))
		IV = infile.read(16)

		decryptor = AES.new(key, AES.MODE_CBC, IV)

		with open(output_file, 'wb') as outfile:
			while True:
				part = infile.read(part_size)

				if len(part) == 0:
					break
				outfile.write(decryptor.decrypt(part))
			outfile.truncate(file_size)


def getkey(Password):
	hasher = SHA256.new(Password)
	return hasher.digest()

def main():
	choice = raw_input("Would you like to (E)ncrypt or (D)ecrypt? - ")
	if choice == 'E':
		filename = raw_input("file to encrypt - ")
		password = raw_input("password")
		encrypt(getkey(password),filename)
		print "Done."
	elif choice == 'D':
		filename = raw_input("file to decrypt - ")
		password = raw_input("password")
		decrypt(getkey(password),filename)
		print "Done."
	else:
		print "Wrong Option"

if __name__ == '__main__':
	main()
