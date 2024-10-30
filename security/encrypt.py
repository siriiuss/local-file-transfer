import hmac
import hashlib
import sqlite3

def create_hmac(path, key, algoritma="sha256"):
    # HMAC için hashing algoritması ve anahtar
    hmac_algorithm = hmac.new(key.encode(), digestmod=algoritma)

    # Dosyayı okuma ve HMAC hesaplama
    with open(path, "rb") as file:
        while chunk := file.read(8192):  # Dosyayı parça parça oku
            hmac_algorithm.update(chunk)

    return hmac_algorithm.hexdigest()  # HMAC'in hexadecimal

def main():
    file_name = input("Dosya adı giriniz:")
    file_path = f"../files/{file_name}"
    key = input("Anahtar giriniz:")  # Dosya için anahtar
    hmac_value = create_hmac(file_path, key)
    return hmac_value

def check_hmac(filename):
    conn = sqlite3.connect('allowed.db')
    cursor = conn.cursor()
    cursor.execute("SELECT file_key FROM files WHERE file_name = ?", (filename,))
    crypted = cursor.fetchone()[0]
    print(crypted)
    key = input("Lütfen HMAC doğrulaması için anahtarınızı girin: ")
    mevcut_hmac = create_hmac(f"../files/{filename}", key)

    if hmac.compare_digest(mevcut_hmac, crypted):
        return True
    else:
        return False

if __name__ == '__main__':
    test = check_hmac("dosya.txt")
    print(test)


