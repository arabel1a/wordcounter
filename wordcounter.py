from pynput.keyboard import Key, Listener
from collections import deque

def is_whitespace(key):
    return key == Key.space or key == Key.enter or key == Key.tab 

class WordStats():
    def __init__(self, cachesize=1000):
        self.word_lendths = deque(maxlen=1000)
        self.last_word_len = 0
        self.whitespace_len = 0
        self.word_cnt = 0

    def update(self, key):
        if is_whitespace(key):
            if self.last_word_len:
                self.word_lendths.append(self.last_word_len)
                self.word_cnt += 1
            self.last_word_len = 0
            self.whitespace_len += 1

        if key == Key.backspace:
            if not self.whitespace_len:
                self.whitespace_len -= 1
            elif self.word_lendths:
                self.word_lendths[-1] -= 1
                if self.word_lendths[-1] <= 0:
                    self.word_cnt -= 1
                    self.word_lendths.pop()
        if hasattr(key, 'char'):
            self.last_word_len += 1

class CLI():
    def __init__(self, stats):
        self.stats = stats

    def on_press(self, key):
        self.stats.update(key)
        if key == Key.backspace or is_whitespace(key):
            print(f"Total word count: {stats.word_cnt}\b", end='\r')

if __name__ == '__main__':
    stats = WordStats()
    gui = CLI(stats)
    with Listener(on_press=gui.on_press) as listener:
        listener.join()
