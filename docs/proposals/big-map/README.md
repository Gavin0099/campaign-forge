# Big-map mockup — captured, disposable, no gameplay

2026-10-24，獨立 Godot 場景，32×24 裝飾菱形格；不讀規則，不是 L03 重製。
12 個既有 idle sprite 站位（其中四個重複托瑪用來看隊形），沒有新同伴設定。
地面是既有原創 `battlefield.png` 小塊 UV 重複加色調；水、橋、格線是程式示意。
沒有產生或修改任何 swing／idle／knight PNG，也未使用商業遊戲素材。

從工作區根目錄，以 brief 指定的 Godot 4.7.2 executable 代入 `GODOT`：

```powershell
GODOT --path godot-spike res://scenes/mockups/BigMapMockup.tscn
GODOT --path godot-spike --resolution 1280x720 --audio-driver Dummy --max-fps 60 -s res://tools/capture_big_map.gd
GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gtest=res://tests/test_big_map_mockup.gd -gexit
```

三個命令分別是手動開啟、重錄、單一 smoke test。手動開啟不是本輪人類試玩證據。
`capture.json` 與七張原生 1280×720 PNG 是實際 runtime，不是編輯器畫面或合成圖。
實際擷取命令 exit 0，7 checks 全 true、7 張圖；單一 GUT smoke exit 0、34 assertions。
正常遊戲 main scene 仍是 Skirmish，沒有引用 mockup。

操作：WASD／方向鍵平移，中鍵拖曳，滾輪 0.8／1.0／1.2／1.5；F／Home 回到
首個展示單位；O 總覽，再按 O 回局部 zoom（位置留在中央）；1／2／3 換格寬；
E 開關邊緣捲動；Esc 離開。小地圖只顯示點位與視野框，不可點擊。
正式提案的跟隨、事件鏡頭、離屏箭頭與攻擊回位都未接入。

擷取前實際注入 D、middle mouse、wheel、O、F，並在這個展示視窗邊緣測捲動；
之後關閉互動／edge motion，以固定位置拍七張圖，所以截圖顯示 edge OFF。
這是軟體自動操作證據，不是 Gavin 的試玩回饋。bounds smoke 覆蓋三種格寬、
三種 zoom、兩端 clamp、中心與 overview；沒有讀寫或測試真實關卡。

第一輪擷取已有七張真圖，但對 `res://../` 呼叫 make_dir_recursive_absolute
產生 Windows 路徑錯誤，exit 仍是 0；不採它作最終成功證據。工具改用
globalize_path，並在建立目錄失敗時回傳非零。已重新擷取，最終 log 無該錯誤；
初始 log 留在 `godot-spike/docs/evidence/spike03/w5-capture-pre-pathfix.log`。

全圖只看比例與視野，不驗證路線可達、AI、效能上限、fog 或勝敗。painted chunk／
TileMapLayer 都仍是提案。人類尺度判斷與大圖選案 **OWNER_PENDING**。
