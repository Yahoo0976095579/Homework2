import json
#程式開頭定義
INPUT_FILE = "orders.json"
OUTPUT_FILE = "output_orders.json"
#主選單界面
def display_menu():
    print("***************選單***************")
    print("1. 新增訂單")
    print("2. 顯示訂單報表")
    print("3. 出餐處理")
    print("4. 離開")
    print("**********************************")
#獲取操作項目
def get_user_choice():
    while True:
        choice = input("請選擇操作項目(Enter 離開)：")
        if choice == "":
            return "4"  # 按 Enter視為選擇離開
        elif choice in ("1", "2", "3", "4"):
            print(" ")
            return choice
        else:
            print("=> 請輸入有效的選項（1-4）")
            display_menu()  # 重新顯示選單
#新增訂單
def add_order():
    #將訂單編號轉成大寫
    order_id = input("請輸入訂單編號：").upper()
    # 使用 any() 檢查訂單編號有沒有重複
    orders = load_orders() or []
    if any(order["order_id"] == order_id for order in orders):
        print(f"=> 錯誤：訂單編號 {order_id} 已存在!")
        return
    customer = input("請輸入顧客姓名：")
    items = []
    while True:
      item_name = input("請輸入訂單項目名稱（輸入空白結束）：")
      #已經有點餐項目了，按Enter可結束點餐
      if item_name == "" and len(items) != 0:
        break
      #沒有點餐項目，則顯示至少需要一個訂單項目
      elif item_name == "" and len(items) == 0:
        print("=> 至少需要一個訂單項目")
        continue
      else:
        while True:
            #輸入價格和數量，有一輸入結果不符合格式，則全部重新輸入
            try:
                price = int(input("請輸入價格："))
                if price <= 0:
                    print("=> 錯誤：價格不能為負數，請重新輸入")
                    continue
                quantity = int(input("請輸入數量："))
                if quantity <= 0:
                    print("=> 錯誤：數量必須為正整數，請重新輸入")
                    continue
                break
            except ValueError:
                print("=> 錯誤：價格或數量必須為整數，請重新輸入")
        #將訂單項目加入items
        items.append({"name": item_name, "price": price, "quantity": quantity})
    #將訂單項目加入order
    order = {"order_id": order_id, "customer": customer, "items": items}
    #讀取orders.json檔案
    load_orders()
    orders = load_orders() or []  # 如果無法讀取訂單，則初始化為空列表
    #將訂單加入orders
    orders.append(order)
    #將訂單寫入orders.json檔案
    save_orders(orders)
    print(f"=> 訂單 {order_id} 已新增！")
    return None
#顯示訂單報表
def display_order_report():
    #讀取orders.json檔案
    load_orders()
    orders = load_orders() or []  # 如果無法讀取訂單，則初始化為空列表
    #顯示訂單報表，每個項目包含名稱、價格和數量
    for i, order in enumerate(orders):
        print(f"訂單 #{i + 1}")
        #調用函數
        display_order_details(order)
        display_order_items(order["items"])
#出餐處理
def process_order():
    #調用函數讀取orders.json檔案
    load_orders()
    orders = load_orders() or []  # 如果無法讀取訂單，則初始化為空列表
    ##如果orders.json檔案沒有訂單，則顯示目前沒有待處理的訂單
    if len(orders) == 0:
        print("=> 目前沒有待處理的訂單")
        return
    #顯示待處理訂單列表
    print("\n======== 待處理訂單列表 ========")
    for i, order in enumerate(orders):
        print(f"{i + 1}. 訂單編號: {order['order_id']} - 客戶: {order['customer']}")
    print("================================")
    ##選擇要出餐的訂單編號，並判斷輸入是否正確
    while True:
        try:
            choice = input("請選擇要出餐的訂單編號 (輸入數字或按 Enter 取消): ")
            if choice == "":
                return
            order_index = int(choice) - 1
            if 0 <= order_index < len(orders):
                break
            else:
                print("=> 錯誤：請輸入有效的數字")
        except ValueError:
            print("=> 錯誤：請輸入有效的數字")
    #從訂單列表中刪除選擇的訂單
    order = orders.pop(order_index)
    save_orders(orders)# 儲存剩餘的訂單
    output_orders = load_output_orders() or []  # 如果無法讀取訂單，則初始化為空列表
    output_orders.append(order)# 將出餐訂單加入output_orders
    save_output_orders(output_orders)# 儲存出餐訂單
    print(f"=> 訂單 {order['order_id']} 已出餐完成")
    print("出餐訂單詳細資料：")
    print("\n==================== 出餐訂單 ====================")
    display_order_details(order)
    display_order_items(order["items"])
#訂單的編號,客戶姓名,商品名稱,單價,數量,小計
def display_order_details(order):
    """顯示訂單詳細資料。"""
    print(f"訂單編號: {order['order_id']}")
    print(f"客戶姓名: {order['customer']}")
    print("-" * 50)
    print("商品名稱 單價\t數量\t小計")
    print("-" * 50)
#訂單項目列表，每個項目包含名稱、價格和數量
def display_order_items(items):
    total_price = 0
    for item in items:
        subtotal = item["price"] * item["quantity"]
        print(f"{item['name']}\t{item['price']:>4,}\t{item['quantity']}\t{subtotal:,}")
        total_price += subtotal
    print("-" * 50)
    print(f"訂單總額: {total_price:,}\n")
    print("=" * 50)
#讀取orders.json 含錯誤提示
def load_orders():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            orders = json.load(f)
        return orders
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"=> 錯誤：無法讀取 '{INPUT_FILE}' 檔案")
        return None
#讀取output_orders.json 含錯誤提示 
def load_output_orders():
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            output_orders = json.load(f)
        return output_orders
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"=> 錯誤：無法讀取 '{OUTPUT_FILE}' 檔案")
        return None
#儲存orders.json 含錯誤提示
def save_orders(orders):
    try:
        with open(INPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(orders, f, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print(f"=> 錯誤：無法找到 '{INPUT_FILE}' 檔案，請確認檔案是否存在")
#儲存output_orders.json 含錯誤提示
def save_output_orders(output_orders):
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(output_orders, f, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print(f"=> 錯誤：無法找到 '{OUTPUT_FILE}' 檔案，請確認檔案是否存在")
#主程式
def main():
    while True:
        display_menu()
        choice = get_user_choice()

        if choice == "1":
            error = add_order()#order回傳非空字串，則主程式error=true，顯示錯誤訊息。
            if error:
                print(f"=> 錯誤：{error}")
        elif choice == "2":
            display_order_report()
        elif choice == "3":
            process_order()
        elif choice == "4":
            print("程式結束。")
            break

if __name__ == "__main__":
    main()