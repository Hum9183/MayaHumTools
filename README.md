# MayaHumTools

## インストール方法
C:\Program Files\Autodesk\ApplicationPluginsにクローンするか、ZIPファイルを解凍して配置してください。

![image](https://user-images.githubusercontent.com/117564304/218305703-95018c61-2cd5-41b5-97c7-e79e37ad53ae.png)

ウィンドウタブ内にHumToolsという項目が追加されたらOKです。

## BlendShapedVertexMerger
### 概要
ブレンドシェイプを設定してあるメッシュの頂点をマージするツールです。<br>
普通の編集なら壊れてしまうところを、壊さずにマージができます。

### 使い方
マージしたい頂点を選択した状態で「Merge vertex」を押すと実行されます。<br>
マージの種類は「頂点をセンターにマージ」を採用しています。

![BlendShapedVertexMerger_Demo](https://user-images.githubusercontent.com/117564304/218306243-db1a6532-d313-45ef-b8cf-c38f8166eaa4.gif)

### 注意点
現在Maya2018で正常な動作を確認しています。<br>
Maya2022でも動作はしますが、ブレンドシェイプの状態によっては正常に動作しないことを確認しています。
