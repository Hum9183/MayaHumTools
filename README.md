# MayaHumTools

## インストール方法
C:\Program Files\Autodesk\ApplicationPluginsにクローンするか、ZIPファイルを解凍して配置してください。

![image](https://user-images.githubusercontent.com/117564304/218305703-95018c61-2cd5-41b5-97c7-e79e37ad53ae.png)

ウィンドウタブ内にHumToolsという項目が追加されたらOKです。

<br>

## BlendShapedVertexMerger

### バージョン
Maya2018, 2022で正常な動作を確認しています。<br>

### 概要
ブレンドシェイプが設定してあるメッシュの頂点をマージするツールです。<br>
普通の編集なら壊れてしまうところを、壊さずにマージができます。

### 使い方
マージしたい頂点を選択した状態で「Merge vertex」を押すとマージが実行されます。<br>

![BlendShapedVertexMerger_Demo](https://user-images.githubusercontent.com/117564304/219054782-81f45306-b419-4002-bc55-533d91a785a1.gif)

### ツール詳細
- マージの種類は「頂点をセンターにマージ」を採用しています。<br>
- 「ブレンドシェイプを再構築する」オプションをオンにすると、ブレンドシェイプノードを一度削除し再構築します(Maya2022以降ではオン推奨)<br>

<br>

## BlendShapedMeshEditor

### バージョン
Maya2018, 2022で正常な動作を確認しています。<br>

### 概要
ブレンドシェイプが設定してあるメッシュにおいて、<br>
コンポーネントの移動やマルチカットを使った頂点の追加ができるツールです。<br>
普通の編集なら壊れてしまうところを、壊さずに編集ができます。

### 使い方
1. 編集したいメッシュを選択した状態で「Start editing」を押します。<br>
2. ボタンが黄色くなったら編集が可能になります。各々行いたい編集を行います。<br>
3. 編集が終わったら、編集したメッシュを選択した状態で「Finish editing」を押します。<br>

![BlendShapedMeshEditor_Demo](https://user-images.githubusercontent.com/117564304/219922084-c3bb9509-51e0-4688-b48a-026078c24f20.gif)

### 注意点
マルチカットの編集には種類がありますが、**polySplit**にのみ対応しています。<br>
**polyCut**には非対応です(ビューポート上に線を引くように切る方法)<br>
編集の種類はヒストリを見てご確認ください。

![bsme_1](https://user-images.githubusercontent.com/117564304/219922179-d44bbf42-ae6b-4c61-8e14-dc7f29fe3ffd.png)

### ツール詳細
- 「Start editing」を押すと、リビルド済のターゲットメッシュが削除されます。<br>
  これは、ターゲットメッシュが存在していると、コンポーネントの移動情報をターゲットに反映することができないためです。<br>
  また、Maya2022以降ではtweakノードを追加しています(「Finish editing」を押したときに削除されます)<br>
  詳しくは
  [Autodesk公式ドキュメント](https://knowledge.autodesk.com/ja/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2022/JPN/Maya-WhatsNewPR/files/GUID-C6BC495C-F1B6-4370-AC2D-24CA4B4AAF9B-htm.html)
  をご参照ください。

- 「Finish editing」を押すと、あるNonDeformerHistory(当ツールではUVの移動)を生成し、NonDeformerHistoryを削除します。<br>
  これを行うことにより、ベースメッシュでのコンポーネントの移動情報がターゲットたちにも反映されます。<br>
  この処理はMayaが自動で行う処理であり、メッシュの頂点数やブレンドシェイプの数に合わせて処理時間が長くなる可能性があります。
