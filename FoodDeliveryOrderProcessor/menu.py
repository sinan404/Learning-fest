import json

MENU = {
    "Margherita Pizza": 12.50,
    "Veg Burger": 8.99,
    "Chicken Wrap": 9.75,
    "Caesar Salad": 7.50,
    "French Fries": 3.99,
    "Chocolate Shake": 4.50,
}

try:
    with open("orders.json", "r") as f:
        ORDERS = json.load(f)
except FileNotFoundError:
    print("Could not find orders.json. Put it in the same folder as menu.py.")
    ORDERS = []

def calculate_order_total(cart):
    total = 0
    for name,qty in cart.items():
        price = MENU[name]
        total = total + price * qty
    return round(total,2)

def discount(total):
    if total >=100:
        return total*0.15
    elif total >=50:
        return total*0.10
    else:
        return 0.00

def validation(order):
    problems =[]
    if not order["items"]:
        problems.append("order is empty")
    
    for name,qty in order["items"].items():
        if name not in MENU:
            problems.append(name + " is not on the menu")
        if qty <=0:
            problems.append("qty must be atleast 1")

    return problems

def delivery_charge(amount):
    if amount >= 75:
        return 0.00
    else:
        return 4.99 

def final_bill(order):
    subtotal = calculate_order_total(order["items"])
    after_discount = subtotal - discount(subtotal)
    delivery = delivery_charge(after_discount)
    total_bill = after_discount + delivery
    return round(total_bill,2)


results = []

for order in ORDERS:
    problems = validation(order)

    if problems:
        print("REJECTED", order["order_id"], order["customer"], "-", problems)
    else:
        total = final_bill(order)
        print("OK", order["order_id"], order["customer"], total)
        results.append({"order_id": order["order_id"],
                        "customer": order["customer"],
                        "total": total})
        
def find_highest_order(results):
    if not results:
        return None
    
    highest = results[0]
    for result in results:
        if result["total"] > highest["total"]:
            highest = result
    return highest

top = find_highest_order(results)

if top:
    print("\nHighest-value order :",top["order_id"])
else:
    print("No valid orders to compare")


def write_summary(results,top,filename="sales_summary.txt"):
    total_revenue = 0
    for result in results:
        total_revenue += result["total"]
    
    with open(filename,"w")as f:
        f.write("Daily Sales Summary Report\n")
        f.write("orders received :" + str(len(ORDERS))+ "\n")
        f.write("orders completed :" + str(len(results))+ "\n")
        f.write("order rejected :" + str(len(ORDERS)-len(results))+ "\n")
        f.write("total revenue : $" + str(round(total_revenue,2))+ "\n")

        if top:
            f.write("Highest-value order: #" + str(top["order_id"]) + " (" + top["customer"] + ") - $" + str(top["total"]) + "\n")
        else:
            f.write("Highest-value order: none\n")

    print("Summary written to " + filename)

write_summary(results,top)