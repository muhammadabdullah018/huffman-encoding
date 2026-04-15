#include <bitset>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <memory>
#include <queue>
#include <string>
#include <unordered_map>
#include <vector>

using namespace std;

// =====================================================
// HUFFMAN NODE STRUCTURE
// =====================================================
/**
 * Binary Tree Node for Huffman Tree
 * Contains character data, frequency, and child pointers
 * Time Complexity: O(1) for creation
 * Space Complexity: O(1)
 */
struct HuffmanNode {
  char data;
  unsigned frequency;
  shared_ptr<HuffmanNode> left, right;

  HuffmanNode(char data, unsigned freq)
      : data(data), frequency(freq), left(nullptr), right(nullptr) {}

  // Constructor for internal nodes (no character)
  HuffmanNode(unsigned freq, shared_ptr<HuffmanNode> l,
              shared_ptr<HuffmanNode> r)
      : data('\0'), frequency(freq), left(l), right(r) {}
};

// COMPARATOR FOR MIN-HEAP

/**
 * Comparator for priority queue (min-heap)
 * Lower frequency = higher priority
 */
struct CompareNode {
  bool operator()(shared_ptr<HuffmanNode> const &a,
                  shared_ptr<HuffmanNode> const &b) {
    return a->frequency > b->frequency;
  }
};

// HUFFMAN TREE CLASS
/**
 * Core Huffman Tree Implementation
 * Handles tree construction and code generation
 */
class HuffmanTree {
private:
  shared_ptr<HuffmanNode> root;
  unordered_map<char, string> huffmanCodes;
  unordered_map<char, unsigned> frequencyTable;

  /**
   * Generate Huffman codes using DFS traversal
   * Time Complexity: O(n) where n = unique characters
   * Space Complexity: O(h) for recursion stack, h = tree height
   */
  void generateCodes(shared_ptr<HuffmanNode> node, string code) {
    if (!node)
      return;

    // Leaf node - store the code
    if (!node->left && !node->right) {
      huffmanCodes[node->data] = code.empty() ? "0" : code;
      return;
    }

    // Traverse left (add '0') and right (add '1')
    generateCodes(node->left, code + "0");
    generateCodes(node->right, code + "1");
  }

public:
  /**
   * Build Huffman Tree using Greedy Algorithm
   * Uses Min-Heap (Priority Queue) for efficient minimum extraction
   * Time Complexity: O(n log n) where n = unique characters
   * Space Complexity: O(n)
   */
  void buildTree(const unordered_map<char, unsigned> &freqTable) {
    frequencyTable = freqTable;

    // Min-heap priority queue
    priority_queue<shared_ptr<HuffmanNode>, vector<shared_ptr<HuffmanNode>>,
                   CompareNode>
        minHeap;

    // Create leaf node for each character
    // Time: O(n log n) for n insertions
    for (const auto &pair : freqTable) {
      minHeap.push(make_shared<HuffmanNode>(pair.first, pair.second));
    }

    // Special case: single unique character
    if (minHeap.size() == 1) {
      auto node = minHeap.top();
      root = make_shared<HuffmanNode>(node->frequency, node, nullptr);
      generateCodes(root, "");
      return;
    }

    // Greedy algorithm: repeatedly merge two minimum frequency nodes
    // Time: O(n log n) - n-1 iterations, each with 2 extractions and 1
    // insertion
    while (minHeap.size() > 1) {
      auto left = minHeap.top();
      minHeap.pop();
      auto right = minHeap.top();
      minHeap.pop();

      // Create internal node with combined frequency
      auto parent = make_shared<HuffmanNode>(left->frequency + right->frequency,
                                             left, right);
      minHeap.push(parent);
    }

    root = minHeap.top();

    // Generate codes using DFS
    generateCodes(root, "");
  }

  const unordered_map<char, string> &getCodes() const { return huffmanCodes; }

  const unordered_map<char, unsigned> &getFrequencyTable() const {
    return frequencyTable;
  }

  shared_ptr<HuffmanNode> getRoot() const { return root; }

  /**
   * Display Huffman codes
   * Time Complexity: O(n)
   */
  void displayCodes() const {
    cout << "\n=== Huffman Codes ===" << endl;
    cout << setw(10) << "Character" << setw(15) << "Frequency" << setw(15)
         << "Code" << endl;
    cout << string(40, '-') << endl;

    for (const auto &pair : huffmanCodes) {
      char c = pair.first;
      string display = (c == '\n') ? "\\n" : string(1, c);
      cout << setw(10) << display << setw(15) << frequencyTable.at(c)
           << setw(15) << pair.second << endl;
    }
  }
};

// =====================================================
// ENCODER CLASS
// =====================================================
/**
 * Handles file compression using Huffman coding
 */
class Encoder {
private:
  HuffmanTree huffmanTree;

  /**
   * Analyze character frequency
   * Time Complexity: O(m) where m = file size
   * Space Complexity: O(n) where n = unique characters
   */
  unordered_map<char, unsigned> analyzeFrequency(const string &inputFile) {
    unordered_map<char, unsigned> freqTable;
    ifstream file(inputFile, ios::binary);

    if (!file.is_open()) {
      throw runtime_error("Cannot open input file: " + inputFile);
    }

    char ch;
    while (file.get(ch)) {
      freqTable[ch]++;
    }

    file.close();
    return freqTable;
  }

  /**
   * Convert string to binary representation
   * Optimization: Uses bitwise operations for efficiency
   */
  string toBinaryString(const string &encoded) {
    string binary;
    for (char c : encoded) {
      binary += bitset<8>(c).to_string();
    }
    return binary;
  }

public:
  /**
   * Complete compression pipeline
   * Time Complexity: O(m + n log n) where m = file size, n = unique chars
   * Space Complexity: O(m + n)
   */
  void compress(const string &inputFile, const string &outputFile) {
    cout << "\n========== COMPRESSION STARTED ==========" << endl;

    // Step 1: Frequency Analysis - O(m)
    cout << "\n[1/5] Analyzing character frequencies..." << endl;
    auto freqTable = analyzeFrequency(inputFile);
    cout << "Found " << freqTable.size() << " unique characters" << endl;

    if (freqTable.empty()) {
      throw runtime_error("Input file is empty!");
    }

    // Step 2: Build Huffman Tree - O(n log n)
    cout << "\n[2/5] Building Huffman Tree..." << endl;
    huffmanTree.buildTree(freqTable);
    huffmanTree.displayCodes();

    // Step 3: Encode the file - O(m)
    // Step 3: Encode and Write Stream - O(m)
    cout << "\n[3/5] Encoding and writing to file..." << endl;

    ofstream outFile(outputFile, ios::binary);

    // 3a. Write Header (Frequency Table)
    size_t tableSize = freqTable.size();
    outFile.write(reinterpret_cast<char *>(&tableSize), sizeof(tableSize));

    for (const auto &pair : freqTable) {
      outFile.write(&pair.first, sizeof(char));
      outFile.write(reinterpret_cast<const char *>(&pair.second),
                    sizeof(unsigned));
    }

    // 3b. Process file and stream bits
    ifstream inFile(inputFile, ios::binary);
    const auto &codes = huffmanTree.getCodes();

    char accumulator = 0;
    int bitCount = 0;
    size_t totalBitsEncoded = 0; // Track total bits for debugging/stats

    // NOTE: We can't easily write exact encoded length upfront without
    // pre-calculating or seeking back.
    // For standard Huffman decoding, we usually rely on "valid" traversal
    // or store valid bits in the last byte.
    // Let's reserve space for the total bit count (size_t) at the start of data
    // section
    streampos lengthPos = outFile.tellp(); // Remember position
    size_t placeholderLen = 0;
    outFile.write(reinterpret_cast<const char *>(&placeholderLen),
                  sizeof(size_t));

    char ch;
    while (inFile.get(ch)) {
      string code = codes.at(ch);
      for (char bit : code) {
        if (bit == '1') {
          accumulator |= (1 << (7 - bitCount));
        }
        bitCount++;
        totalBitsEncoded++;

        if (bitCount == 8) {
          outFile.write(&accumulator, 1);
          accumulator = 0;
          bitCount = 0;
        }
      }
    }
    inFile.close();

    // Write remaining bits (padding)
    if (bitCount > 0) {
      outFile.write(&accumulator, 1);
    }

    // 3c. Update Total Encoded Length in header
    // We stored "encoded length" in the previous version as *bits* or *bytes*?
    // Previous code: `size_t encodedLen = encodedData.length();` (Number of
    // bits) Decoder reads this to know when to stop.

    outFile.seekp(lengthPos);
    outFile.write(reinterpret_cast<char *>(&totalBitsEncoded), sizeof(size_t));
    outFile.seekp(0, ios::end); // Go back to end

    outFile.close();

    // Step 5: Statistics
    cout << "\n[5/5] Calculating compression statistics..." << endl;
    calculateCompressionRatio(inputFile, outputFile);

    // Note: Step 4 is merged above.

    cout << "\n========== COMPRESSION COMPLETED ==========" << endl;
  }

  /**
   * Calculate and display compression metrics
   */
  void calculateCompressionRatio(const string &inputFile,
                                 const string &outputFile) {
    ifstream in(inputFile, ios::binary | ios::ate);
    ifstream out(outputFile, ios::binary | ios::ate);

    size_t originalSize = in.tellg();
    size_t compressedSize = out.tellg();

    in.close();
    out.close();

    double ratio = (1.0 - (double)compressedSize / originalSize) * 100;

    cout << "\n=== Compression Statistics ===" << endl;
    cout << "Original Size:    " << originalSize << " bytes" << endl;
    cout << "Compressed Size:  " << compressedSize << " bytes" << endl;
    cout << "Space Saved:      " << (originalSize - compressedSize) << " bytes"
         << endl;
    cout << "Compression Ratio: " << fixed << setprecision(2) << ratio << "%"
         << endl;
  }
};

// =====================================================
// DECODER CLASS
// =====================================================
/**
 * Handles file decompression
 */
class Decoder {
private:
  HuffmanTree huffmanTree;

  /**
   * Decode using tree traversal (most efficient method)
   * Time Complexity: O(m * h) where m = encoded length, h = tree height
   * Space Complexity: O(m) for output
   * Average h = O(log n), so overall O(m log n)
   */
  string decodeUsingTree(const string &encodedData,
                         shared_ptr<HuffmanNode> root) {
    string decoded;
    auto current = root;

    for (char bit : encodedData) {
      // Traverse tree based on bit
      current = (bit == '0') ? current->left : current->right;

      // Reached leaf node - found a character
      if (!current->left && !current->right) {
        decoded += current->data;
        current = root; // Reset to root for next character
      }
    }

    return decoded;
  }

public:
  /**
   * Complete decompression pipeline
   * Time Complexity: O(m log n) where m = encoded size, n = unique chars
   * Space Complexity: O(m + n)
   */
  void decompress(const string &compressedFile, const string &outputFile) {
    cout << "\n========== DECOMPRESSION STARTED ==========" << endl;

    ifstream inFile(compressedFile, ios::binary);
    if (!inFile.is_open()) {
      throw runtime_error("Cannot open compressed file: " + compressedFile);
    }

    // Step 1: Read frequency table
    cout << "\n[1/4] Reading metadata..." << endl;
    size_t tableSize;
    inFile.read(reinterpret_cast<char *>(&tableSize), sizeof(tableSize));

    unordered_map<char, unsigned> freqTable;
    for (size_t i = 0; i < tableSize; i++) {
      char ch;
      unsigned freq;
      inFile.read(&ch, sizeof(char));
      inFile.read(reinterpret_cast<char *>(&freq), sizeof(unsigned));
      freqTable[ch] = freq;
    }

    cout << "Found " << tableSize << " unique characters in metadata" << endl;

    // Step 2: Rebuild Huffman Tree
    cout << "\n[2/4] Reconstructing Huffman Tree..." << endl;
    huffmanTree.buildTree(freqTable);
    shared_ptr<HuffmanNode> root = huffmanTree.getRoot();
    shared_ptr<HuffmanNode> current = root;

    // Step 3: Read encoded data and Decode Stream - O(m log n)
    cout << "\n[3/4] Decoding stream..." << endl;

    // Read total bits length
    size_t totalBits;
    inFile.read(reinterpret_cast<char *>(&totalBits), sizeof(totalBits));

    ofstream outFile(outputFile, ios::binary);

    char byte;
    size_t bitsProcessed = 0;

    while (inFile.read(&byte, 1) && bitsProcessed < totalBits) {
      // Process each bit in the byte
      for (int i = 0; i < 8 && bitsProcessed < totalBits; i++) {
        // Check bit at index i (from left 7..0 or right? My encoder used 7-i)
        // Encoder: accumulator |= (1 << (7 - bitCount));
        // So we check (byte >> (7 - i)) & 1

        bool bit = (byte >> (7 - i)) & 1;

        if (bit == 0) {
          current = current->left;
        } else {
          current = current->right;
        }

        if (!current->left && !current->right) {
          outFile.put(current->data);
          current = root;
        }
        bitsProcessed++;
      }
    }

    inFile.close();
    outFile.close();

    cout << "Decoded bits: " << bitsProcessed << endl;
    cout << "\n========== DECOMPRESSION COMPLETED ==========" << endl;
  }
};

// =====================================================
// MAIN DEMONSTRATION
// =====================================================
int main(int argc, char *argv[]) {
  if (argc != 4) {
    cerr << "Usage: " << argv[0]
         << " <compress|decompress> <input_file> <output_file>" << endl;
    return 1;
  }

  string mode = argv[1];
  string inputFile = argv[2];
  string outputFile = argv[3];

  try {
    if (mode == "compress") {
      Encoder encoder;
      encoder.compress(inputFile, outputFile);
    } else if (mode == "decompress") {
      Decoder decoder;
      decoder.decompress(inputFile, outputFile);
    } else {
      cerr << "Invalid mode. Use 'compress' or 'decompress'." << endl;
      return 1;
    }
  } catch (const exception &e) {
    cerr << "Error: " << e.what() << endl;
    return 1;
  }

  return 0;
}