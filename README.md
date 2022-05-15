# lc2msxmml
Converter from LovelyComposer to MSX MML  
LovelyComposerからMSX mml へのコンバーター

# Overview
This is the conversion script from LovelyComposer jsonl file to MSX basic music macro language.  
Currently still under the draft status.  
But you can convert LC jsonl to .bas file by somewhat simple level.  
You can use .exe windows OS binary.
  
[built bin for windows (R0.5.2)](https://drive.google.com/file/d/1zox4-CWEIF4brYUqrazgz3kA8auTVskB/view?usp=sharing "lc2msxmml")
  
ラビコン jsonl から MSX basic music macro 言語への変換スクリプトです。  
現在はまだドラフトの状態です。  
しかしながら、ラビコンのjsonlから.basファイルへ幾分簡易的な程度で変換できます。  
またWindows用の実行バイナリを用意しています。

# Usage example
- python lc2msxmml.py --start 10 --step 10 --notelen 32 .\01.jsonl music01.bas
- echo .\02.jsonl | python .\lc2msxmml.py music02.bas
- lc2msxmml.exe -s 10 -p 10 -l 32 -t 100 -v 14 -e .\01.jsonl music01.bas
- See usage detail by python .\lc2msxmml.py -h

# TODO
- GUIs
- Direct converstion to 'N' MML macro
- MGS file type conversion
- Extended MSX basic (MSX-MUSIC) mml
- Reverse converter from MSX basic mml to LovelyComposer jsonl
- Volume macro designation by the each note
- Simple tone reflection functionality in case of MGS/ext-basic mml
- Note coupling functionality (to be considered)  
  <BR>
- GUI版
- 'N' マクロ直指定変換
- MGSファイル対応
- MSX-MUSIC 拡張BASIC対応
- MSX mml からラビコンへの逆変換
- 各ノート毎のボリューム指定
- MGS/拡張BASIC mmlの場合に簡易音色を適用する機能
- 各符号を結合する機能（検討中）

# Release notes
## R0.5.2
- Optimized frequency of the octave macro usage
- Added argument option for using play syntax by MSX extended basic
- Added 'configure' method so that class 'basic' instance maintains the series of MSX mml macro parameters  
- Changed default parameter value for volume and tempo
  <BR>
- オクターブマクロの使用回数を最適化
- MSX 拡張BASICのPLAY文を使用するオプションを追加
- クラスインスタンスにおいてMSX mml macroのパラメータを維持しておくように'configure'メソッドを追加
- デフォルトの音量とテンポの数値を変更

## R0.5.1 (hotfix)
- Fixed wrong operation when used --step option.
- Fixed miss octave detection.
- Updated R0.5 release note.
- Modified a couple of syntaxes in msxmml.py  
  <BR>
- --stepオプションを仕様した場合の誤作動を修正
- オクターブ検出ミスを修正
- R0.5のリリースノートを更新
- msxmml.pyの動作に影響しない記述形式を微修正
  
## R0.5
- It does not support application of tone.
- Assign note scale to MSX mml O1-O7 (O8 is not used).
  - This is because 7 octaves in LovelyComposer while MSX octave takes 8 level, and the result of sensory evaluation by the author.
- Assign volume by 15 for all channels.
- Currently it is not supported coupling series of note duration which takes same tone(id) and same octave.
  - This is for some meaning reflecting original LC spec as is.
- Fixed tempo by 120 'T' macro value
- Operate PSG channel 1-3 by PartSelection 1-3 in LovelyComposer.
- Mechanically detect sound and noise channels.
  - If sound and noise tone were mixed in single PartSelection both bits in register 7 shall be turned off (enabled).  
  <BR>
- 音色の変換には対応していない
- ラビコンの元の音階をMSX MMLでの O1-O7として変換する（O8に乗らない）
  - これはMSXが８段階の一方でラビコンでは７オクターブを採ることと、著者の聴感に寄る（独断）
- 全チャンネルの音量はV15で固定
- 連続した同音色同音階の符の結合は行わない
  - これはある意味でラビコンの仕様を反映したものと言えるため（検討中）
- テンポは'T'マクロ値で120固定（検討中）
- PSGのチャンネル1-3はラビコンでのパート選択1-3で処理される
- 自動的に音とノイズの設定を識別する
  - 音とノイズの両方が同パート選択に混在する場合、レジスタ7の両ビットとも0（吹鳴）となる
