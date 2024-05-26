import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
import argparse

def encrypt_directory(directory, key_file_path, extensions):
    """
    ディレクトリ内の特定の拡張子のファイルをAESで暗号化します。

    Args:
        directory (str): 暗号化したいディレクトリのパス
        key_file_path (str): 暗号鍵を保存したファイルのパス
        extensions (list[str]): 暗号化したい拡張子
    """

    # 暗号鍵を読み込みます。
    with open(key_file_path, 'rb') as f:
        key = f.read()

    # ディレクトリ内のファイルを1つずつ処理します。
    for root, _, files in os.walk(directory):
        for filename in files:
            # ファイルの拡張子を取得します。
            ext = os.path.splitext(filename)[1]

            # 対象の拡張子のファイルのみ処理します。
            if ext.lower() in extensions:
                # ファイルのパスを作成します。
                file_path = os.path.join(root, filename)

                # ファイルを暗号化します。
                try:
                    encrypt_file(file_path, key, file_path + '.enc')
                except Exception as e:
                    print(f'ファイル "{file_path}" の暗号化に失敗しました: {e}')

def decrypt_directory(directory, key_file_path, extensions):
    """
    ディレクトリ内の特定の拡張子のファイルをAESで復号化します。

    Args:
        directory (str): 復号化したいディレクトリのパス
        key_file_path (str): 暗号鍵を保存したファイルのパス
        extensions (list[str]): 復号化したい拡張子
    """

    # 暗号鍵を読み込みます。
    with open(key_file_path, 'rb') as f:
        key = f.read()

    # ディレクトリ内のファイルを1つずつ処理します。
    for root, _, files in os.walk(directory):
        for filename in files:
            # ファイルの拡張子を取得します。
            ext = os.path.splitext(filename)[1]

            # 対象の拡張子のファイルのみ処理します。
            if ext.lower() in extensions:
                # 暗号化ファイルのパスを作成します。
                encrypted_file_path = os.path.join(root, filename + '.enc')

                # ファイルが存在すれば復号化します。
                if os.path.exists(encrypted_file_path):
                    try:
                        decrypt_file(encrypted_file_path, key)
                        os.remove(encrypted_file_path)  # 復号化後、暗号化ファイルを削除
                    except Exception as e:
                        print(f'ファイル "{encrypted_file_path}" の復号化に失敗しました: {e}')

def encrypt_file(file_path, key, encrypted_file_path):
    """
    ファイルをAESで暗号化します。

    Args:
        file_path (str): 暗号化したいファイルのパス
        key (bytes): 暗号化キー
        encrypted_file_path (str): 暗号化後のファイルのパス
    """

    # ファイルを読み込み、バイナリデータに変換します。
    with open(file_path, 'rb') as f:
        data = f.read()

    # AES暗号化オブジェクトを作成します。
    cipher = AES.new(key, AES.MODE_CBC)

    # 暗号化に必要なパディングを追加します。
    padded_data = pad(data, AES.block_size)

    # 暗号化を実行します。
    encrypted_data = cipher.encrypt(padded_data)

    # 暗号化データを新しいファイルに書き込みます。
    with open(encrypted_file_path, 'wb') as f:
        f.write(encrypted_data)

def decrypt_file(file_path, key):
    """
    ファイルをAESで復号化します。

    Args:
        file_path (str): 復号化したいファイルのパス
        key (bytes): 暗号化キー
    """

    # ファイルを読み込み、バイナリデータに変換します。
    with open(file_path, 'rb') as f:
        data = f.read()

    # AES復号化オブジェクトを作成します。
    cipher = AES.new(key, AES.MODE_CBC)

def decrypt_file(file_path, key):
    """
    ファイルをAESで復号化します。

    Args:
        file_path (str): 復号化したいファイルのパス
        key (bytes): 暗号化キー
    """

    # ファイルを読み込み、バイナリデータに変換します。
    with open(file_path, 'rb') as f:
        data = f.read()

    # AES復号化オブジェクトを作成します。
    cipher = AES.new(key, AES.MODE_CBC)

    # 復号化を実行します。
    try:
        decrypted_data = cipher.decrypt(data)
    except ValueError as e:
        # パディングエラーが発生した場合は、ファイルが破損している可能性があります。
        print(f'ファイル "{file_path}" が破損している可能性があります: {e}')
        return

    # パディングを削除します。
    padded_data = decrypted_data[:-AES.block_size]
    data = unpad(padded_data)

    # 復号化データを新しいファイルに書き込みます。
    out_file_path = file_path[:-4]
    with open(out_file_path, 'wb') as f:
        f.write(data)

if __name__ == '__main__':
    # コマンドライン引数を解析します。
    parser = argparse.ArgumentParser(description='ディレクトリ暗号化/復号化プログラム')
    parser.add_argument('directory', help='暗号化/復号化したいディレクトリ')
    parser.add_argument('key_file_path', help='暗号鍵のファイルパス')
    parser.add_argument('action', choices=['encrypt', 'decrypt'], help='実行する処理 (encrypt: 暗号化, decrypt: 復号化)')
    parser.add_argument('--extensions', nargs='+', help='暗号化/復号化したい拡張子 (指定しない場合は、すべてのファイル)')
    args = parser.parse_args()

    # 処理を実行します。
    if args.action == 'encrypt':
        encrypt_directory(args.directory, args.key_file_path, args.extensions)
    elif args.action == 'decrypt':
        decrypt_directory(args.directory, args.key_file_path, args.extensions)
    else:
        print('不正なアクションが指定されました。')

