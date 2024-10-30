import socket
import os
from tqdm import tqdm
import threading
from security import perms
from security import encrypt

def send_file(filename, conn):
    if os.path.exists(filename) and perms.check_file(filename) == True and encrypt.check_hmac(filename, filekey) == True:
        # Dosya bulunduğunu istemciye bildir ve anahtar doğrulaması iste
        conn.send(b'FILE_FOUND')

        # Dosya boyutunu al ve istemciye gönder
        if:
            filesize = os.path.getsize(filename)
            conn.send(str(filesize).encode())
        else:
            print("Dosya izin hatası oluştu! (Gönderme aşamasında)")
        # İstemciden onay bekle
        ack = conn.recv(1024)
        if ack != b'READY':
            print("İstemci dosya almaya hazır değil.")
            return

        # Dosyayı gönderirken ilerleme çubuğu göster
        with open(filename, 'rb') as f:
            with tqdm(total=filesize, unit='B', unit_scale=True, desc=f"Gönderiliyor {filename}") as progress:
                while True:
                    bytes_read = f.read(1024)
                    if not bytes_read:
                        break
                    conn.sendall(bytes_read)
                    progress.update(len(bytes_read))
        print(f'{filename} başarıyla gönderildi.')
    else:
        conn.send(b'FILE_NOT_FOUND')


def handle_client(conn, addr):
    print(f'Bağlantı kuruldu: {addr}')

    try:
        filename = conn.recv(1024).decode()
        print(f'İstenen dosya: {filename}')
        print(f'İzin kontrolü: {perms.check_file(filename)}')
        if :
            send_file(f"files/" + filename, conn)
        else:
            print("Dosya izin hatası oluştu")
    except Exception as e:
        print(f'Hata: {e}')
    finally:
        conn.close()


def start_server(host='0.0.0.0', port=5001):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f'Sunucu {host}:{port} adresinde dinliyor...')

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()



def receive_file(filename, conn):
    # İlk olarak dosya boyutunu al
    filesize_data = conn.recv(1024).decode()

    try:
        filesize = int(filesize_data)
    except ValueError:
        print("Dosya boyutu alınamadı.")
        return

    # Sunucuya dosya almaya hazır olduğunu bildir
    conn.send(b'READY')

    # Dosyayı alırken ilerleme çubuğu göster
    with open(f'downloaded_{filename}', 'wb') as f:
        with tqdm(total=filesize, unit='B', unit_scale=True, desc=f"İndiriliyor {filename}") as progress:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                f.write(data)
                progress.update(len(data))
                print(f'{filename} başarıyla indirildi.')

def start_client(server_ip, server_port, filename, filekey):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
    except ConnectionRefusedError:
        print("Sunucuya bağlanılamıyor.")
        return

    client_socket.send(filename.encode())
    client_socket.send(filekey.encode())

    status = client_socket.recv(1024)
    if status == b'FILE_FOUND':
        receive_file(filename, client_socket)
    else:
        print(f'{filename} sunucuda bulunamadı.')

    client_socket.close()




if __name__ == '__main__':
    mode = int(input("Sunucu modunu seçin:\n1)Sunucu\n2)İstemci: "))
    if mode == 1:
        start_server()
        handle_client()
    elif mode == 2:
        server_ip = "192.168.1.33"
        #server_ip = str(input("Sunucu IP adresini giriniz:"))  # Sunucunun IP adresi
        server_port = 5001  # Sunucunun portu
        filename = input("Dosya ismini giriniz:")  # İstediğin dosya ismi
        filekey = input("Dosya anahtarını giriniz:")
        start_client(server_ip, server_port, filename, filekey)
    else:
        print("Geçersiz mod seçimi.")
