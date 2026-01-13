import mysql.connector as pro
try:
    d = pro.connect(host="localhost", user="root", password="admin", database="food")
    e = d.cursor()
except pro.Error as err:
    print(f"Error: {err}")
    exit(
def add_food():
    try:
        ser = int(input("Enter the Food ID: "))
        fi = input("Enter the Food name: ")
        fp = int(input("Enter the Price of Food: "))
        ft = input("Enter the Food Type: ")
        
        query = "INSERT INTO item (S_no, Food_Item, Price, Food_Type) VALUES (%s, %s, %s, %s)"
        e.execute(query, (ser, fi, fp, ft))
        d.commit()
        print("NEW FOOD ADDED SUCCESSFULLY")
    except Exception as err:
        print(f"Error adding food: {err}")

def update_food():
    print("\n1. Update food name") 
    print("2. Update food price") 
    try:
        us = int(input("Enter your choice: ")) 
        if us == 1:
            fnid = int(input("Enter the Food ID to update: "))
            fna = input("Enter the updated Food Name: ") 
            e.execute("UPDATE item SET Food_Item = %s WHERE S_no = %s", (fna, fnid))
        elif us == 2:
            fnic = int(input("Enter the Food ID to update: "))
            fnf = int(input("Enter the updated Food Price: "))
            e.execute("UPDATE item SET Price = %s WHERE S_no = %s", (fnf, fnic))
        d.commit()
        print("UPDATED SUCCESSFULLY")
    except Exception as err:
        print(f"Error updating: {err}")

def delete_food():
    try:
        fidd = int(input("Enter the Food ID you want to delete: "))
        e.execute("DELETE FROM item WHERE S_no = %s", (fidd,))
        d.commit()
        print("FOOD ITEM DELETED SUCCESSFULLY")
    except Exception as err:
        print(f"Error: {err}")

def view_orders():
    print("\nDetails of all orders are:")
    e.execute("SELECT * FROM orders")
    rtt = e.fetchall() 
    if not rtt:
        print("No orders found.")
        return

    for i in rtt:
        print("*" * 30)
        print(f"Food name: {i[0]}\nPrice: {i[1]}\nTotal: {i[2]}\nPhone: {i[3]}\nAddress: {i[4]}")
    print("*" * 30)

def ad_login():
    while True:
        print("\n--- ADMIN PANEL ---")
        print("1. Add food\n2. Update food\n3. Delete food\n4. View orders\n5. Logout")
        try:
            ask = int(input("Enter choice: "))
            if ask == 1: add_food()
            elif ask == 2: update_food()
            elif ask == 3: delete_food()
            elif ask == 4: view_orders()
            elif ask == 5: break
        except ValueError:
            print("Please enter a valid number.")

def ad_panel():
    pas = input("Enter Admin Password: ")
    if pas == 'Zomato':
        print("Access granted") 
        ad_login()
    else:
        print("Wrong Password! Access Denied.")
def show_menu():
    e.execute("SELECT * FROM item") 
    w = e.fetchall()
    print("\n------------- MENU FOR TODAY ------------------ ")
    for i in w:
        print(f"ID: {i[0]} | Name: {i[1]} | Price: {i[2]} | Type: {i[3]}")
    
    ui = input("\nDo you want to order food (Yes/No)? ") 
    if ui.lower() == "yes":
        F_order() 

def F_order():
    try:
        io = int(input("Enter the Food ID: "))
        # First, check if the item exists
        e.execute("SELECT Food_Item, Price FROM item WHERE S_no = %s", (io,))
        item = e.fetchone()
        
        if item:
            iname, iprice = item[0], item[1]
            qty = int(input("Enter Quantity: ")) 
            phn = input("Enter Phone NO: ") # Kept as string for safety
            adr = input("Enter Address: ")
            
            oprice = iprice * qty 
            query = "INSERT INTO orders(O_name, I_price, O_price, P_no, ADR) VALUES(%s, %s, %s, %s, %s)"
            e.execute(query, (iname, iprice, oprice, phn, adr))
            d.commit()
            
            print("\n******** BILL ********") 
            print(f"Address: {adr}\nFood: {iname}\nTotal Price: {oprice}")
            print("********************\nOrder Confirmed!")
        else:
            print("Item not found in menu.")
    except Exception as err:
        print(f"Order failed: {err}")

def F_View():
    yno = input("Enter your registered phone NO: ")
    e.execute("SELECT * FROM orders WHERE P_no = %s", (yno,))
    rt = e.fetchall()
    if rt: 
        print("\n--- YOUR RECENT ORDERS ---")
        for i in rt:
            print(f"Food: {i[0]} | Total: {i[2]} | Address: {i[4]}")
    else:
        print("No orders found for this number.")

def F_Cancel():
    cor = input("Enter phone NO to cancel order: ")
    e.execute("DELETE FROM orders WHERE P_no = %s", (cor,))
    d.commit()
    print("Order(s) cancelled successfully.")

def F_feedb():
    fdb = input("Enter Phone NO: ") 
    fdc = input("Give us Feedback: ")
    e.execute("INSERT INTO Feed VALUES(%s, %s)", (fdb, fdc))
    d.commit()
    print("THANKS FOR YOUR FEEDBACK")
def main_menu(): 
    while True:
        print("\n--- CUSTOMER PORTAL ---")
        print("1. View Menu\n2. Place Order\n3. View Order Status\n4. Cancel Order\n5. Feedback\n6. Back to Home")
        try:
            a = int(input("Enter choice: "))
            if a == 1: show_menu() 
            elif a == 2: F_order() 
            elif a == 3: F_View() 
            elif a == 4: F_Cancel() 
            elif a == 5: F_feedb() 
            elif a == 6: break
        except ValueError:
            print("Invalid input.")

def homepage(): 
    while True:
        print("\n" + "="*30)
        print("   WELCOME TO FOOD PORTAL")
        print("="*30)
        print("1. Admin Login\n2. Customer Portal\n3. EXIT") 
        try:
            op = int(input("Enter option: "))
            if op == 1: ad_panel() 
            elif op == 2: main_menu()
            elif op == 3: 
                print("Exiting... Goodbye!")
                break
        except ValueError:
            print("Select 1, 2, or 3.")

if __name__ == "__main__":
    homepage()
