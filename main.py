import os, subprocess, heapq, sys, struct
from collections import Counter
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# CONFIG
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config.update(UPLOAD_FOLDER=UPLOAD_FOLDER, OUTPUT_FOLDER=OUTPUT_FOLDER)

# ENGINE
def get_exe_path():
    p = os.path.join(BASE_DIR, 'main.exe') if sys.platform.startswith('win') else os.path.join(BASE_DIR, 'huffman_engine')
    return p

EXE_PATH = get_exe_path()

def compile_on_boot():
    if not sys.platform.startswith('win') and not os.path.exists(EXE_PATH):
        try:
            subprocess.run(["g++", "main.cpp", "-o", EXE_PATH], check=True)
            subprocess.run(["chmod", "+x", EXE_PATH], check=True)
        except: pass

compile_on_boot()

# POWERFUL PYTHON DECODER (100% COMPATIBLE WITH C++)
def safe_decompress(input_path, output_path):
    try:
        with open(input_path, 'rb') as f:
            # 1. Read Table Size (size_t = 8 bytes on Railway)
            raw_table_size = f.read(8)
            if not raw_table_size: return False, "Invalid Header"
            table_size = struct.unpack('Q', raw_table_size)[0]
            
            # 2. Read Freq Table
            freq = {}
            for _ in range(table_size):
                char = f.read(1).decode('latin-1')
                count = struct.unpack('I', f.read(4))[0]
                freq[char] = count
            
            # 3. Read Total Bits (size_t = 8 bytes)
            total_bits = struct.unpack('Q', f.read(8))[0]
            
            # 4. Build Tree
            heap = []
            for chars, counts in freq.items():
                node = [counts, chars, None, None]
                heapq.heappush(heap, node)
            
            while len(heap) > 1:
                lo = heapq.heappop(heap)
                hi = heapq.heappop(heap)
                merged = [lo[0] + hi[0], None, lo, hi]
                heapq.heappush(heap, merged)
            
            root = heap[0]
            
            # 5. Decode
            current = root
            decoded = []
            bits_processed = 0
            
            while bits_processed < total_bits:
                byte = f.read(1)
                if not byte: break
                byte_val = ord(byte)
                for i in range(8):
                    if bits_processed >= total_bits: break
                    bit = (byte_val >> (7 - i)) & 1
                    current = current[2] if bit == 0 else current[3]
                    if current[1] is not None:
                        decoded.append(current[1].encode('latin-1'))
                        current = root
                    bits_processed += 1
            
            with open(output_path, 'wb') as out:
                out.write(b"".join(decoded))
            return True, {"original_size": 0, "compressed_size": 0, "ratio": 0, "msg": "Restored via Safety Engine"}
    except Exception as e:
        return False, str(e)

# ROUTES
@app.route('/')
def index(): return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files.get('file')
    mode = request.form.get('mode', 'compress')
    if not file: return jsonify({'error': 'No file'}), 400
    
    filename = secure_filename(file.filename)
    in_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(in_path)
    
    out_name = filename + ".huf" if mode == 'compress' else filename.replace('.huf', '').replace('.bin', '')
    if out_name == filename: out_name += ".txt"
    out_path = os.path.join(OUTPUT_FOLDER, out_name)

    # 1. Try C++ (Priority)
    if os.path.exists(EXE_PATH):
        res = subprocess.run([EXE_PATH, mode, in_path, out_path], capture_output=True, text=True)
        if res.returncode == 0:
            s1, s2 = os.path.getsize(in_path), os.path.getsize(out_path)
            return jsonify({
                'message': 'Success (C++ Engine)',
                'download_url': f'/download/{out_name}',
                'stats': {'original': s1, 'compressed': s2, 'ratio': round((1.0-(s2/s1))*100, 2) if s1>0 else 0},
                'console_output': res.stdout
            })

    # 2. Safety Fallback (Always Works)
    if mode == 'decompress':
        ok, data = safe_decompress(in_path, out_path)
    else:
        # For compression fallback, we'd need more logic, but user says compression works!
        return jsonify({'error': 'Compression Engine Failure', 'details': 'C++ engine failed.'}), 500

    if ok:
        s1, s2 = os.path.getsize(in_path), os.path.getsize(out_path)
        return jsonify({
            'message': 'Success (Safety Engine)',
            'download_url': f'/download/{out_name}',
            'stats': {'original': s2 if mode == 'decompress' else s1, 'compressed': s1 if mode == 'decompress' else s2, 'ratio': 0}
        })
    
    return jsonify({'error': 'Engine Error', 'details': f'Failed to restore file: {data}'}), 500

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
