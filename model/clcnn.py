# -*- coding:utf-8 -*-
from tensorflow.python.keras.layers import *
from tensorflow.python.keras.models import Model
import tensorflow as tf
"""
character-level cnnの実装

"""
class ClcnnBuldier(object):
    # build
    def build(self, embed_size=128, max_length=100, filter_sizes=(2, 3, 4, 5), filter_num=64):
        self.model = self.__build_layer(embed_size, max_length, filter_sizes, filter_num)
        return self.model

    # private bulid
    def __build_layer(self, embed_size=128, max_length=100, filter_sizes=(2, 3, 4, 5), filter_num=64):
        # Input Layer
        input_ts = Input(shape=(max_length, ))
        # Embedding 各文字をベクトル変換
        emb = Embedding(0xffff, embed_size)(input_ts)
        emb_ex = Reshape((max_length, embed_size, 1))(emb)
        # 各カーネルサイズで畳み込みをかける．
        convs = []
        # Conv2D
        for filter_size in filter_sizes:
            conv = Conv2D(filter_num, (filter_size, embed_size), activation="relu")(emb_ex)
            pool = MaxPooling2D((max_length - filter_size + 1 , 1))(conv)
            convs.append(pool)
        # ConcatenateでConv2Dを結合
        convs_merged = Concatenate()(convs)
        # Reshape
        reshape = Reshape((filter_num * len(filter_sizes),))(convs_merged)
        # Dense
        fc1 = Dense(64, activation="relu")(reshape)
        bn1 = BatchNormalization()(fc1)
        do1 = Dropout(0.5)(bn1)
        # 2class 分類なので，sigmoid関数を用いる．
        fc2 = Dense(1, activation='sigmoid')(do1)

        # Model generate
        model = Model(
            inputs=[input_ts],
            outputs=[fc2]
        )

        return model

# main
if __name__ == '__main__':
    # builder object
    builder = ClcnnBuldier()
    # model
    model = builder.build()
    # show model information
    model.summary()
