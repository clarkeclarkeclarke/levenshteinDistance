from collections import defaultdict, namedtuple
from heapq import heappush, heappop

class NotFound(Exception):
    pass

def word_ladder(words, start, end):

    placeholder = object()
    matches = defaultdict(list)
    neighbours = defaultdict(list)
    for word in words:
        for i in range(len(word)):
            pattern = tuple(placeholder if i == j else c
                            for j, c in enumerate(word))
            m = matches[pattern]
            m.append(word)
            neighbours[word].append(m)

    def h_score(word):
        return sum(a != b for a, b in zip(word, end))

    closed_set = set()

    Node = namedtuple('Node', 'f g word previous')
    open_set = set([start])
    open_heap = [Node(h_score(start), 0, start, None)]
    while open_heap:
        node = heappop(open_heap)
        if node.word == end:
            result = []
            while node:
                result.append(node.word)
                node = node.previous
            return result[::-1]
        open_set.remove(node.word)
        closed_set.add(node.word)
        g = node.g + 1
        for neighbourhood in neighbours[node.word]:
            for w in neighbourhood:
                if w not in closed_set and w not in open_set:
                    next_node = Node(h_score(w) + g, g, w, node)
                    heappush(open_heap, next_node)
                    open_set.add(w)

    raise NotFound("No ladder from {} to {}".format(start, end))

if __name__ == '__main__':
    dictionary = [w.strip() for w in open('/usr/share/dict/words') if w == w.lower()]
    four_letter_words = [w for w in dictionary if len(w) == 4]
    print(word_ladder(four_letter_words,'team','mate'))
