# lc2msxmml
Converter from LovelyComposer to MSX MML  
LovelyComposerからMSX mml へのコンバーター

# Overview
This is the conversion script from LovelyComposer jsonl file to MSX basic music macro language.  
Currently still under the draft status.  
But you can convert LC jsonl to .bas file by somewhat simple level.  
You can use .exe windows OS binary.
  
[built bin for windows (R0.5)](https://drive.google.com/file/d/1zox4-CWEIF4brYUqrazgz3kA8auTVskB/view?usp=sharing "lc2msxmml")
  
ラビコン jsonl から MSX basic music macro 言語への変換スクリプトです。  
現在はまだドラフトの状態です。  
しかしながら、ラビコンのjsonlから.basファイルへ幾分簡易的な程度で変換できます。  
またWindows用の実行バイナリを用意しています。

# Usage example
- python lc2msxmml.py --start 10 --step 10 --notelen 32 .\01.jsonl music01.bas
- echo .\02.jsonl | python .\lc2msxmml.py music02.bas
- See usage detail by python .\lc2msxmml.py -h

# Release notes
## R0.5
- It does not support application of tone.
- Assign note scale to MSX mml O1-O7 (O8 is not used).
 - This is because 7 octaves in LovelyComposer while MSX octave takes 8 level, and the result of sensory evaluation by the author.
- Assign volume by 15 for all channels.
- Currently it is not supported coupling of note duration.
  - This is for some meaning reflecting original LC spec as is.
  <BR>
- 音色の変換には対応していない
- ラビコンの元の音階をMSX MMLでの O1-O7として変換する（O8に乗らない）
  - これはMSXが８段階の一方でラビコンでは７オクターブを採ることと、著者の聴感に寄る（独断）
- 全チャンネルの音量はV15で固定
- 連続した同音同音階の符の結合は行わない
  - これはある意味でラビコンの仕様を反映したものと言えるため（検討中）
