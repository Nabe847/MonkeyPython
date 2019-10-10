Pynkey
====

Pynkey はオライリージャパンから発刊されている書籍「Go 言語で作るインタプリタ」に登場するプログラミング言語 "Monkey" のPython実装です。

## 文法
### データ型
    bool [例] true, false  
    int [例] 5, 0, -1  
    function [例] fn(x, y) { x + y; }  

### 単行演算子
    -, !

### 二項演算子
    +, -, /, *, ==, !=, <, >

### 変数
    let a = 10;
    let b = true;
    let func = fn(x){ x + 2; };

### 関数
    let func = fn(x){ x + 2; }
    func(10);
    >>> 12

    let new_adder = fn(x){ fn(y){ x + y} }
    let add_two = new_adder(2)
    add_two(1)
    >>> 3
    add_two(2)
    >>> 4


## if-else
    let x = 1
    if(x < 2){ 10;} else { 20;}
    >>> 10

    if( x < 1){ 10;} else { 20;}
    >>> 20

    if( x == 1){ 10;}
    >>> 10

## 動作環境
    Python 3.7.1 以上

## 使い方
    カレントをMonkeyにして以下のコマンドを実行する。
    python main.py

    Hello! This is the Pynkey programming language!
    Feel free to type in commands
    >> let a = 10
    >> a
    10
    >> exit
    (終了)

