import gnupg
import os


class FileEncryptor(object):
    """Encrypt files.

    Args:
        gnupg_home (str): Home dir for gnupg.  Needs to have pubkey loaded
            already.
    """

    def __init__(self, gnupg_home, pubkeys, recipients):
        self.gpg = gnupg.GPG(gnupghome=gnupg_home)
        self.recipients = recipients
        print("GPG import results:")
        print(self.gpg.import_keys(pubkeys).results)
        print(self.gpg.list_keys())

    def encrypt(self, file_path):
        """Encrypt file, delete original.

        If file fails to encrypt, original is not deleted and False will
        be returned.

        Args:
            file_path (str): Full path to file to be encrpted.

        Returns:
            str: Full path of encrypted file
        """

        enc_file_path = "%s.gpg" % file_path
        with open(file_path, 'rb') as unenc_file:
            status = self.gpg.encrypt_file(unenc_file,
                                           recipients=self.recipients,
                                           always_trust=True,
                                           output=enc_file_path)
        if status.ok:
            os.remove(file_path)
            return enc_file_path
        else:
            print("status: %s\n\tstderr: %s" % (status.status, status.stderr))
            return False
