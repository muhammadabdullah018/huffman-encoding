import os
import subprocess
import heapq
import time
import sys
from collections import Counter
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')
EXE_PATH = os.path.join(BASE_DIR, 'main.exe')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==========================================
# PYTHON HUFFMAN FALLBACK (If C++ fails)
# ==========================================
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_table(text):
    return Counter(text)

def build_huffman_tree(freq_table):
    heap = [HuffmanNode(char, freq) for char, freq in freq_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0] if heap else None

def generate_codes(node, prefix="", codebook={}):
    if node:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)
    return codebook

def python_compress(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        if not text:
            return False, "Input file is empty"

        freq_table = build_frequency_table(text)
        root = build_huffman_tree(freq_table)
        codes = generate_codes(root)
        
        encoded_text = "".join(codes[char] for char in text)
        
        # Padding
        extra_padding = 8 - len(encoded_text) % 8
        encoded_text += "0" * extra_padding
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        
        # To Bytes
        b = bytearray()
        for i in range(0, len(encoded_text), 8):
            byte = encoded_text[i:i+8]
            b.append(int(byte, 2))
            
        with open(output_path, 'wb') as f:
            f.write(bytes(b))
            
        return True, f"Compressed using Python Logic.\nOriginal: {len(text)} chars\nCompressed: {len(b)} bytes"
    except Exception as e:
        return False, str(e)

def python_decompress(input_path, output_path):
    # Note: This is valid ONLY for files compressed with the Python method above.
    # It will fail for the C++ format as the metadata structure differs.
    # This is a fallback demo.
    return False, "Python-based decompression is not fully compatible with the C++ binary format. Please compile the C++ backend for full features."

# ==========================================
# PRIORITY QUEUE STATE
# ==========================================
file_queue = []
job_counter = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/queue-view')
def queue_view():
    return render_template('queue.html')

@app.route('/process', methods=['POST'])
def process_file_direct():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    mode = request.form.get('mode')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(input_path)
    
    success, result = run_cpp_backend(filename, mode, input_path)
    if success:
         return jsonify(result)
    else:
         return jsonify(result), 500

# ==========================================
# QUEUE API METHODS
# ==========================================
@app.route('/api/queue/add', methods=['POST'])
def add_to_queue():
    global job_counter
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    mode = request.form.get('mode', 'compress')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(input_path)
    
    file_size = os.path.getsize(input_path)
    
    job_metadata = {
        'id': job_counter,
        'filename': filename,
        'mode': mode,
        'size': file_size,
        'input_path': input_path,
        'status': 'queued'
    }
    
    heapq.heappush(file_queue, (file_size, job_counter, job_metadata))
    job_counter += 1
    
    return jsonify({'message': 'Added to queue', 'job': job_metadata})

@app.route('/api/queue/list', methods=['GET'])
def get_queue_list():
    sorted_jobs = sorted(file_queue, key=lambda x: (x[0], x[1]))
    jobs = [item[2] for item in sorted_jobs]
    return jsonify({'queue': jobs, 'count': len(jobs)})

@app.route('/api/queue/process-next', methods=['POST'])
def process_next_in_queue():
    if not file_queue:
        return jsonify({'error': 'Queue is empty'}), 400
    
    priority, _, job_data = heapq.heappop(file_queue)
    success, result = run_cpp_backend(job_data['filename'], job_data['mode'], job_data['input_path'])
    
    return jsonify({
        'job': job_data,
        'result': result,
        'success': success
    })

def run_cpp_backend(filename, mode, input_path):
    """Try C++, fallback to Python if needed"""
    if mode == 'compress':
        output_filename = filename + '.huf'
    else:
        if filename.endswith('.huf') or filename.endswith('.bin'):
            output_filename = filename[:-4]
        else:
            output_filename = filename + '.txt'

    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
    
    # 1. Try C++ Executable
    exe_exists = os.path.exists(EXE_PATH) and os.path.getsize(EXE_PATH) > 0
    
    if exe_exists:
        try:
            result = subprocess.run([EXE_PATH, mode, input_path, output_path], capture_output=True)
            
            stdout_text = result.stdout.decode('utf-8', errors='replace') if result.stdout else ""
            stderr_text = result.stderr.decode('utf-8', errors='replace') if result.stderr else ""

            if result.returncode == 0:
                response_data = {
                    'message': 'Success (C++ Backend)',
                    'download_url': f'/download/{output_filename}',
                    'console_output': stdout_text
                }
                
                # Check for likely compressed file types
                lower_name = filename.lower()
                compressed_exts = ['.pdf', '.jpg', '.jpeg', '.png', '.zip', '.rar', '.7z', '.mp4', '.mp3', '.docx']
                if any(lower_name.endswith(ext) for ext in compressed_exts):
                     response_data['warning'] = "Note: The uploaded file appears to be already compressed (e.g. PDF, Image). Huffman coding relies on character redundancy, which is low in these files. Resulting size may be similar or slightly larger due to metadata overhead."

                return True, response_data
            else:
                 # If C++ fails, we might fall back or report error
                 return False, {'error': 'C++ Backend Failed', 'details': stderr_text}
        except OSError as e:
             if e.winerror == 193:
                 print("Invalid Executable. Switching to Fallback.")
             else:
                 return False, {'error': str(e)}

    # 2. Fallback to Python (Only for Compression Demo)
    if mode == 'compress':
        success, msg = python_compress(input_path, output_path)
        if success:
            return True, {
                'message': 'Success (Python Fallback)',
                'download_url': f'/download/{output_filename}',
                'console_output': "WARNING: C++ Compiler not found or main.exe invalid.\nUsed Python Fallback for demonstration.\n\n" + msg
            }
        else:
            return False, {'error': 'Python Fallback Failed', 'details': msg}
    
    return False, {'error': 'C++ Executable (main.exe) missing or invalid. Please compile the project to use decompression.'}

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)
    except Exception as e:
        return str(e), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
