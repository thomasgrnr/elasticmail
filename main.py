import gnupg
import os.path
from pprint import pprint

BASE ="""-----BEGIN PGP MESSAGE-----
Version: GnuPG v1

{message}
-----END PGP MESSAGE-----
"""

CHUNK_SIZE = 5

def generate_key(gpg):
    input_data = gpg.gen_key_input(key_type="RSA", key_length=1024, name_email="foo.bar@domain.com")
    key_data = gpg.gen_key(input_data)
    return str(key_data)

def export_key(gpg, key):
    ascii_armored_public_keys = gpg.export_keys(key)
    ascii_armored_private_keys = gpg.export_keys(key, True)
    with open('./gnupg/mykeyfile.asc', 'w') as f:
        f.write(ascii_armored_public_keys)
        f.write(ascii_armored_private_keys)

def create_key(gpg):
    key = generate_key(gpg)
    export_key(gpg, key)
    keys = gpg.list_keys(True)
    for elmt in keys:
        print(gpg.delete_keys(elmt["fingerprint"], True))
        print(gpg.delete_keys(elmt["fingerprint"]))
    return True

def import_key(gpg):
    key_data = open('./gnupg/mykeyfile.asc').read()
    import_results = gpg.import_keys(key_data)
    return import_results.results

def encrypt(message, gpg, *args):
    encrypted_data = gpg.encrypt(message, args)
    encrypted = ''.join(str(encrypted_data).split('\n')[3:-2])
    return encrypted

def decrypt(message, gpg):
    encrypted_string = BASE.format(message=message)
    decrypted_data = gpg.decrypt(encrypted_string)
    return str(decrypted_data)

def chunk_encrypted_text(text):
    index = dict()
    for i in range(len(text)-CHUNK_SIZE):
        index[text[i:i+CHUNK_SIZE]]=i
    return index


def main(gpg):
    import_key(gpg)

    message = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque non quam sem. Curabitur scelerisque magna nec tincidunt ornare. Nunc maximus lectus eget augue tincidunt viverra. Aenean eleifend, dui at accumsan hendrerit, risus turpis volutpat nibh, nec ullamcorper turpis eros nec diam. Sed nec nisl ante. Aliquam convallis elit dui, nec accumsan orci ornare sit amet. Cras id est ipsum.
    Sed ex tellus, gravida ut dapibus in, pellentesque ac sem. Integer et placerat odio, at pretium sapien. Aliquam ullamcorper efficitur metus nec bibendum. Nunc accumsan sodales turpis, vel hendrerit turpis lobortis id. Curabitur non risus et odio gravida semper. Cras pulvinar rhoncus ex, ut fringilla magna eleifend ac. Pellentesque nec massa mattis, viverra purus tempor, viverra arcu. Vivamus tortor mauris, tristique ut tellus eu, mollis facilisis neque. Ut eget imperdiet urna.

Aenean sit amet laoreet urna. Nunc commodo cursus sodales. Morbi ultricies ullamcorper nisi vel luctus. Phasellus mattis suscipit tellus, ac consequat magna dictum mollis. Vivamus consequat est ipsum, eget consequat tortor accumsan ac. Phasellus a laoreet quam. Maecenas eu risus vel felis vehicula feugiat vitae a massa. Nullam at viverra velit.

Nunc non fermentum sapien. Nam at nisi augue. Fusce placerat eu augue a euismod. Sed porta dictum pretium. Ut elementum orci nec eleifend luctus. Morbi in dignissim elit. Vivamus faucibus fringilla nibh. Curabitur condimentum laoreet sodales. Nullam id maximus elit, et auctor neque. Proin placerat dui eu purus convallis, eu eleifend risus sagittis. Phasellus vitae felis ex. Donec imperdiet quis nisi sit amet accumsan. Sed dapibus tincidunt efficitur.

"""
    index = chunk_encrypted_text(encrypt(message.lower(), gpg, "foo.bar@domain.com"))

    search = "Lorem ipsum"
    search_index = chunk_encrypted_text(encrypt(search.lower(), gpg, "foo.bar@domain.com"))

    counter = 0
    indexes = set()

    for elmt in search_index :
        if elmt in index :
            counter += 1
            indexes.add(index[elmt])

    print("Total :", counter)
    pprint(indexes)

if __name__ == "__main__":

    gpg = gnupg.GPG(gnupghome='./gnupg/')

    if not os.path.exists("./gnupg/mykeyfile.asc"):
        print(create_key(gpg))

    main(gpg)
