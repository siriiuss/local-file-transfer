import sqlite3

def check_user_exists(path):
    # Veritabanı bağlantısı
    conn = sqlite3.connect('allowed.db')


    cursor = conn.cursor()

    # Dosya adını kontrol et
    cursor.execute("SELECT COUNT(*) FROM files WHERE file_name = ?", (path,))
    count = cursor.fetchone()[0]


    conn.close()

    # Eğer count 0 ise dosya mevcut değil
    return count > 0


# Dosyayı kontrol et
def check_file(file_name):
    if check_user_exists(file_name):
        return 0
    else:
        return 1

def get_file_key(file_name):
    # Veritabanı bağlantısı
    conn = sqlite3.connect('allowed.db')


    cursor = conn.cursor()

    # file_name değerine göre file_key değerini çek
    cursor.execute("SELECT file_key FROM files WHERE file_name = ?", (file_name,))
    result = cursor.fetchone()


    conn.close()

    # Eğer sonuç var: file_key değerini döndür, yoksa None
    if result:
        return result[0]
    else:
        return None