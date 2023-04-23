import heapq
import os

"""
ECM1414 - Data Structures and Algorithms
Coursework - Compression Algorithm
"""


class HuffmanCoding:
    """Main class where all functions are defined. """

    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    class NodeInTree:
        """This class stores the nodes that will go in the Huffman Tree. The attributes it contains are all features
        that the nodes will have to include: The character they store and its respective frequency count, and whether
        or not there are more nodes to its left or right.
        """

        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        # defining relational operators < and =
        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            if other == None:
                return False
            if (not isinstance(other, NodeInTree)):
                return False
            return self.freq == other.freq

    # Compression functions:

    def create_freq_dict(self, text):
        """Function that calculates the frequency of a character in the input
        text and updates the dictionary accordingly"""
        frequency = {}
        for character in text:
            if not character in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    def make_heap(self, frequency):
        """Function that makes a priority queue of the nodes, which will be later put in the tree in that order.
        Nodes with a higher priority will be higher up in the tree. (FIFO)"""
        for key in frequency:
            node = self.NodeInTree(key, frequency[key])
            heapq.heappush(self.heap, node)

    def encode(self):
        """Function which makes an empty string which will store a binary code that'll be used when compressing. The
         code is made by an auxiliary function and each unique character in the input text will have one."""
        leaf = heapq.heappop(self.heap)
        current_code = ""
        self.encode_2(leaf, current_code)

    def encode_2(self, leaf, current_code):
        """Function which produces the binary code by going down the tree in order to find the desired character. If we
        go left down the tree a 0 is added to the code and if we go right down a 1 is."""
        if leaf is None:
            return

        if leaf.char is not None:
            self.codes[leaf.char] = current_code
            self.reverse_mapping[current_code] = leaf.char
            return

        self.encode_2(leaf.left, current_code + "0")
        self.encode_2(leaf.right, current_code + "1")

    def padders(self, encoded_text):
        """Function that pads the binary codes in order to make the length of the text a multiple of 8. This is done
        as the binary codes will be stored as bytes, which contain 8 bits, but the binary code in itself might be less
        than 8 bits long hence could get corrupted. """
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_codes(self, text):
        """Function that returns all the binary codes. """
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def get_bytes(self, padded_encoded_text):
        """Function that converts the 8 bit binary codes into bytes and appends them into an array. """
        if len(padded_encoded_text) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def build_tree(self):
        """Function that builds the Huffman Tree by extracting nodes from the priority queue."""
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            joint = self.NodeInTree(None, node1.freq + node2.freq)
            joint.left = node1
            joint.right = node2

            heapq.heappush(self.heap, joint)

    def compress(self):
        """
        Function that compresses the input file into a .bin file
        """
        filename, file_extension = os.path.splitext(self.path)
        output_path = "compressed_" + filename + ".bin"

        with open(self.path, 'r+', encoding="UTF8") as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip()

            frequency = self.create_freq_dict(text)
            self.make_heap(frequency)
            self.build_tree()
            self.encode()

            encoded_text = self.get_codes(text)
            padded_encoded_text = self.padders(encoded_text)

            b = self.get_bytes(padded_encoded_text)
            output.write(bytes(b))

        print("File compressed successfully.")
        return output_path


path = "input.txt"

h = HuffmanCoding(path)

output_path = h.compress()
print("Compressed file: " + output_path)
