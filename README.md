# character-level-cnn-twitter
Character-level CNNを利用してTwitterの分類を行うプログラム

## Description
形態素解析（分かち書き）が必要ないcharacter-level CNNを利用したツイート分類プログラム．
Keras backend Tensorflowを利用している．詳細は [Qiitaの記事](https://qiita.com/ymmtr6/items/f0274fa46db7cd7fd28d)

## DEMO
利用例：http://www.milktea.tech/gin/

## Requirement

+ Python3.6
+ Tensorflow1.5
+ Keras2

## Usage

1. GET TwitterApp Consumer Key and AccessToken from Twitter Application Management.
2. SET dataprocesser/keys.py.
3. RUN run.py

## Install

```
$ pip install tensorflow==1.5.0
$ pip install keras==2.1.4
$ pip install requests-oauthlib
```

## Licence

MIT

## Author

Riku
