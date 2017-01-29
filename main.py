import gnupg

from pprint import pprint

BASE ="""-----BEGIN PGP MESSAGE-----
Version: GnuPG v1

{message}
-----END PGP MESSAGE-----
"""

CHUNK_SIZE = 5

def generate_key(gpg):
    input_data = gpg.gen_key_input(key_type="RSA", key_length=1024)
    key_data = gpg.gen_key(input_data)
    return str(key_data)

def encrypt(message, gpg, key):
    encrypted_data = gpg.encrypt(message, key)
    encrypted = ''.join(str(encrypted_data).split('\n')[3:-2])
    return encrypted

def decrypt(message, gpg):
    encrypted_string = BASE.format(message=message)
    decrypted_data = gpg.decrypt(encrypted_string)
    return str(decrypted_data)

def chunk_encrypted_text(text):
    index = set()
    for i in range(len(text)-CHUNK_SIZE):
        index.add(text[i:i+CHUNK_SIZE])
    return index

if __name__ == "__main__":

    gpg = gnupg.GPG(gnupghome='./gnupg/')
    key =  generate_key(gpg)

    message = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque non quam sem. Curabitur scelerisque magna nec tincidunt ornare. Nunc maximus lectus eget augue tincidunt viverra. Aenean eleifend, dui at accumsan hendrerit, risus turpis volutpat nibh, nec ullamcorper turpis eros nec diam. Sed nec nisl ante. Aliquam convallis elit dui, nec accumsan orci ornare sit amet. Cras id est ipsum.
    Sed ex tellus, gravida ut dapibus in, pellentesque ac sem. Integer et placerat odio, at pretium sapien. Aliquam ullamcorper efficitur metus nec bibendum. Nunc accumsan sodales turpis, vel hendrerit turpis lobortis id. Curabitur non risus et odio gravida semper. Cras pulvinar rhoncus ex, ut fringilla magna eleifend ac. Pellentesque nec massa mattis, viverra purus tempor, viverra arcu. Vivamus tortor mauris, tristique ut tellus eu, mollis facilisis neque. Ut eget imperdiet urna.

Aenean sit amet laoreet urna. Nunc commodo cursus sodales. Morbi ultricies ullamcorper nisi vel luctus. Phasellus mattis suscipit tellus, ac consequat magna dictum mollis. Vivamus consequat est ipsum, eget consequat tortor accumsan ac. Phasellus a laoreet quam. Maecenas eu risus vel felis vehicula feugiat vitae a massa. Nullam at viverra velit.

Nunc non fermentum sapien. Nam at nisi augue. Fusce placerat eu augue a euismod. Sed porta dictum pretium. Ut elementum orci nec eleifend luctus. Morbi in dignissim elit. Vivamus faucibus fringilla nibh. Curabitur condimentum laoreet sodales. Nullam id maximus elit, et auctor neque. Proin placerat dui eu purus convallis, eu eleifend risus sagittis. Phasellus vitae felis ex. Donec imperdiet quis nisi sit amet accumsan. Sed dapibus tincidunt efficitur.

"""

    index = chunk_encrypted_text(encrypt(message.lower(), gpg, key))

    search = "Lorem ipsum"
    search_index = chunk_encrypted_text(encrypt(search.lower(), gpg, key))

    counter = 0

    for elmt in search_index :
        counter += 1 if elmt in index else 0

    print(100*counter/len(search_index),'%')
