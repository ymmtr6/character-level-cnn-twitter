# -*- coding;utf-8 -*-
from tensorflow.python.keras.layers import *
from tensorflow.python.keras.models import *
import sys
import numpy as np

sys.path.append("../")

import dataprocesser.accounts
from model.clcnn import *

class ClcnnTrainer(object):

    def load_data(self, filepath, targets, max_length=100, min_length=10):
        is_target = []
        no_target = []
        with open(filepath) as f:
            for l in f:
                id, comment = l.split("\t", 1)

                # UNICODE 変換
                comment = [ord(x) for x in comment.strip()]#.decode("utf-8")
                # 4byte文字を除外
                comment = [ x for x in comment if x <= 0xffff ]
                # 打ち切り
                comment = comment[:max_length]
                comment_len = len(comment)

                if comment_len < min_length:
                    # 短すぎるのは除外
                    continue
                if comment_len < max_length:
                    # 足りない部分を0パディング
                    comment += ([0] * (max_length - comment_len))

                if id not in targets:
                    no_target.append((0, comment))
                else:
                    is_target.append((1, comment))

        list = is_target + no_target
        random.shuffle(list)
        return list

    def train(self, inputs, targets, batch_size=100, epochs=100, max_length=100, model_filepath="model", learning_rate=0.001):
        builder = ClcnnBuldier()
        model = builder.build()
        model.compile(loss='binary_crossentropy', optimizer='SGD', metrics=['accuracy'])
        # 学習
        model.fit(inputs, targets, epochs=epochs ,batch_size=batch_size, verbose=1, validation_split=0.1, shuffle=True)
        # save
        model.save(model_filepath + ".h5")

if __name__ == '__main__':
    target = dataprocesser.accounts.targets
    trainer = ClcnnTrainer()
    data = trainer.load_data("../dataprocesser/hoge.tsv", nerd, min_length=7)

    input_values = []
    target_values = []
    for target_value, input_value in data:
        input_values.append(input_value)
        target_values.append(target_value)

    input_values = np.array(input_values)
    target_values = np.array(target_values)
    trainer.train(input_values, target_values)
