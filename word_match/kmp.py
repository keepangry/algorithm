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