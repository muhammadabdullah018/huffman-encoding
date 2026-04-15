import os
import subprocess
import heapq
import sys
from collections import Counter
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 1. PATH CONFIGURATION
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure Directories Exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 2. C++ ENGINE LOCATION & COMPILATION
def get_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(BASE_DIR, 'main.exe')
    return os.path.join(BASE_DIR, 'huffman_engine')

EXE_PATH = get_exe_path()

def ensure_engine_exists():
    """Compiles the C++ engine if it's missing on Linux"""
    if not sys.platform.startswith('win') and not os.path.exists(EXE_PATH):
        print(f"🚀 Compiling C++ Backend: {EXE_PATH}...")
        try:
            subprocess.run(["g++", "main.cpp", "-o", EXE_PATH], check=True)
            subprocess.run(["chmod", "+x", EXE_PATH], check=True)
            print("✅ C++ Engine Ready.")
        except Exception as e:
            print(f"❌ Compilation failed: {e}")

# Call on boot
ensure_engine_exists()

# 3. PYTHON FALLBACKS (Only used if C++ is unreachable)
class HuffmanNode:
    def __init__(self, char, freq):
        self.char, self.freq = char, freq
        self.left = self.right = None
    def __lt__(self, other):
        return self.freq < other.freq

def python_compress(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        if not text: return False, "Empty File"
        
        freq = Counter(text)
        heap = [HuffmanNode(c, f) for c, f in freq.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            l, r = heapq.heappop(heap), heapq.heappop(heap)
            m = HuffmanNode(None, l.freq + r.freq)
            m.left, m.right = l, r
            heapq.heappush(heap, m)
        
        codes = {}
        def gen(n, p=""):
            if n:
                if n.char is not None: codes[n.char] = p
                gen(n.left, p+"0"); gen(n.right, p+"1")
        gen(heap[0] if heap else None)
        
        bits = "".join(codes[c] for c in text)
        pad = 8 - len(bits) % 8
        bits += "0" * pad
        b = bytearray([pad])
        for i in range(0, len(bits), 8):
            b.append(int(bits[i:i+8], 2))
            
        with open(output_path, 'wb') as f: f.write(b)
        return True, {"original_size": len(text), "compressed_size": len(b), "ratio": round((1.0-(len(b)/len(text)))*100, 2), "msg": "Python Fallback Active"}
    except Exception as e: return False, str(e)

# 4. WEB ROUTES
@app.route('/')
def index(): return render_template('index.html')

@app.route('/debug-paths')
def debug_paths():
    return jsonify({
        'exe_path': EXE_PATH,
        'exists': os.path.exists(EXE_PATH),
        'files': os.listdir('.')
    })

@app.route('/process', methods=['POST'])
def process():
    file = request.files.get('file')
    mode = request.form.get('mode')
    if not file: return jsonify({'error': 'No file'}), 400
    
    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(input_path)
    
    # DETERMINE OUTPUT NAME
    if mode == 'compress':
        out_name = filename + ".huf"
    else:
        out_name = filename.replace('.huf', '').replace('.bin', '')
        if out_name == filename: out_name += ".txt"
        
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], out_name)

    # EXECUTION LOGIC (C++ First)
    if os.path.exists(EXE_PATH):
        try:
            res = subprocess.run([EXE_PATH, mode, input_path, output_path], capture_output=True, text=True)
            if res.returncode == 0:
                s1, s2 = os.path.getsize(input_path), os.path.getsize(output_path)
                return jsonify({
                    'message': 'Success (C++ Engine)',
                    'download_url': f'/download/{out_name}',
                    'stats': {'original': s1, 'compressed': s2, 'ratio': round((1.0-(s2/s1))*100, 2) if s1>0 else 0},
                    'console_output': res.stdout
                })
        except: pass

    # FALLBACK
    if mode == 'compress':
        ok, data = python_compress(input_path, output_path)
        if ok:
            return jsonify({
                'message': 'Success (Python Fallback)', 
                'download_url': f'/download/{out_name}',
                'stats': {'original': data['original_size'], 'compressed': data['compressed_size'], 'ratio': data['ratio']}
            })
    
    return jsonify({'error': 'Engine Error', 'details': 'C++ engine failed and no Python fallback available for decompression.'}), 500

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
