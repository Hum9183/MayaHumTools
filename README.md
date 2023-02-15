# MayaHumTools

## インストール方法
C:\Program Files\Autodesk\ApplicationPluginsにクローンするか、ZIPファイルを解凍して配置してください。

![image](https://user-images.githubusercontent.com/117564304/218305703-95018c61-2cd5-41b5-97c7-e79e37ad53ae.png)

ウィンドウタブ内にHumToolsという項目が追加されたらOKです。

## BlendShapedVertexMerger

### バージョン
Maya2018, 2022で正常な動作を確認しています。<br>

### 概要
ブレンドシェイプを設定してあるメッシュの頂点をマージするツールです。<br>
普通の編集なら壊れてしまうところを、壊さずにマージができます。

### 使い方
マージしたい頂点を選択した状態で「Merge vertex」を押すとマージが実行されます。<br>

![BlendShapedVertexMerger_Demo](https://user-images.githubusercontent.com/117564304/219054782-81f45306-b419-4002-bc55-533d91a785a1.gif)

### ツール詳細
- マージの種類は「頂点をセンターにマージ」を採用しています。<br>
- 「ブレンドシェイプを再構築する」オプションをオンにすると、ブレンドシェイプノードを一度削除し再構築します(Maya2022ではオン推奨)<br>
