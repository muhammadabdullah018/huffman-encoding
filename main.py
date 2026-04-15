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

# PYTHON DECODER — mirrors C++ tree construction exactly
# Node layout: [frequency, seq_id, char_or_None, left_child, right_child]
# seq_id breaks frequency ties deterministically (matches C++ id field).
# Chars sorted by unsigned byte value before insertion — same as C++ encoder.
def safe_decompress(input_path, output_path):
    try:
        with open(input_path, 'rb') as f:
            raw = f.read(8)
            if not raw or len(raw) < 8:
                return False, "Invalid Header"
            table_size = struct.unpack('<Q', raw)[0]

            freq = {}
            for _ in range(table_size):
                char_byte = f.read(1)
                count_bytes = f.read(4)
                if not char_byte or len(count_bytes) < 4:
                    return False, "Truncated frequency table"
                freq[char_byte.decode('latin-1')] = struct.unpack('<I', count_bytes)[0]

            bits_raw = f.read(8)
            if not bits_raw or len(bits_raw) < 8:
                return False, "Missing bit count"
            total_bits = struct.unpack('<Q', bits_raw)[0]

            # Sort by unsigned byte value — matches C++ sort((unsigned char)a < (unsigned char)b)
            seq = 0
            heap = []
            for char, count in sorted(freq.items(), key=lambda x: ord(x[0])):
                heapq.heappush(heap, [count, seq, char, None, None])
                seq += 1

            while len(heap) > 1:
                lo = heapq.heappop(heap)
                hi = heapq.heappop(heap)
                heapq.heappush(heap, [lo[0] + hi[0], seq, None, lo, hi])
                seq += 1

            if not heap:
                return False, "Empty frequency table"

            root = heap[0]
            # [freq, id, char, left, right] — char is None for internal nodes

            current = root
            decoded = []
            bits_processed = 0
            single_char = (root[2] is not None)  # root is a leaf (single unique char)

            while bits_processed < total_bits:
                byte = f.read(1)
                if not byte:
                    break
                byte_val = ord(byte)
                for i in range(8):
                    if bits_processed >= total_bits:
                        break
                    if single_char:
                        decoded.append(root[2].encode('latin-1'))
                        bits_processed += 1
                        continue
                    bit = (byte_val >> (7 - i)) & 1
                    current = current[3] if bit == 0 else current[4]
                    if current[2] is not None:  # leaf
                        decoded.append(current[2].encode('latin-1'))
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
