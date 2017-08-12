import time
from kmp import kmp

def read_file(path):
    with open(path) as fr:
        return fr.read().strip().split('\n')


class Node(object):
    def __init__(self, is_leaf=False, is_end=False):
        self.is_leaf = is_leaf
        self.is_end = is_end
        self.next = {}


def build_tree(words):
    tree = {}
    for word in words:
        ws = list(word)
        length = len(ws)
        current = tree

        for idx, w in enumerate(ws):
            if w not in current:
                current[w] = {
                    'is_leaf': False,
                    'next': {}
                }
            # 是一个词的结尾
            if idx == length-1:
                current[w]['is_leaf'] = True
            current = current[w]['next']
    return tree


def match_doc(tree, doc_str):
    char_list = list(doc_str)
    doc_length = len(char_list)

    doc_pos = 0
    match_word = ""
    current = tree   # 记录当字需匹配的字典
    match_length = 0

    while True:
        if doc_pos + match_length >= doc_length:
            return ""

        char = char_list[doc_pos + match_length]
        if char in current:
            match_word += char
            next = current[char]['next']

            if current[char]['is_leaf']:  # 当前字为词的结尾，则匹配成功，返回
                return match_word

            if len(next) == 0:  # 到叶子节点，未匹配成功，则向下走一位
                match_length = 0
                match_word = ""
                doc_pos += 1
                current = tree

            if not current[char]['is_leaf'] and len(next) > 0:
                # 向后移动
                match_length += 1
                current = next

        else:
            # 如果未能匹配成功，向后移动一位
            match_word = ""
            doc_pos += 1
            current = tree
            match_length = 0


def pmt(s):
    """
    PartialMatchTable
    """
    prefix = [s[:i+1] for i in range(len(s)-1)]
    postfix = [s[i+1:] for i in range(len(s)-1)]
    intersection = list(set(prefix) & set(postfix))
    if intersection:
        return len(intersection[0])
    return 0


def kmp(big, small):
    i = 0
    while i < len(big) - len(small) + 1:
        match = True
        for j in range(len(small)):
            if big[i+j] != small[j]:
                match = False
                break
        if match:
            return True
        #移动位数 = 已匹配的字符数 – 对应的部分匹配值
        if j:
            i += j - pmt(small[:j])
        else:
            i += 1
    return False


if __name__ == "__main__":
    words = read_file('words.txt')
    n = -1
    build_tree(words[:n])
    tree = build_tree(words[:n])
    lines = read_file('1984.txt')

    start = time.time()
    for line in lines:
        match_w = match_doc(tree, line)
        if match_w != "":
            print("{} \t {}\n".format(match_w, line))

    end = time.time()
    print(end-start)  # 0.10075116157531738

    # 测试kmp
    start = time.time()
    for line in lines:
        for word in words:
            result = kmp(line, word)
            if result:
                print(word)
    end = time.time()
    print(end - start)  # > 30min   我等了8分钟才找出100个， 上个算法找出了400多个，不能再等了。