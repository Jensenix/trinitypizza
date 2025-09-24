from flask import Flask, render_template, request
import os

app = Flask(__name__)

# =====================
# Classes
# =====================
class Topping:
    def __init__(self, name, price=10, img=None):
        self.name = name
        self.price = price
        self.img = img

class Pizza:
    BASE_PRICE = {"Small": 50, "Medium": 75, "Large": 100}

    def __init__(self, size, toppings):
        if size not in self.BASE_PRICE:
            raise ValueError("Ukuran pizza tidak valid!")
        self.size = size
        self.toppings = toppings

    def price(self):
        return self.BASE_PRICE[self.size] + sum(t.price for t in self.toppings)

class Order:
    def __init__(self):
        self.pizzas = []

    def add_pizza(self, pizza):
        self.pizzas.append(pizza)

    def total(self):
        return sum(p.price() for p in self.pizzas)

class Customer:
    def __init__(self, name):
        self.name = name
        self.order = Order()

class PizzaShop:
    def __init__(self):
        self.customers = {}
        self.available_toppings = {
            "Sosis": Topping("Sosis", img="images/sausage.png"),
            "Keju": Topping("Keju", img="images/keju.png"),
            "Jamur": Topping("Jamur", img="images/jamur.png"),
            "Bacon": Topping("Bacon", img="images/bacon.png")
        }

    def add_order(self, customer_name, size, topping_names):
        if not customer_name:
            raise ValueError("Nama customer tidak boleh kosong!")
        if customer_name not in self.customers:
            self.customers[customer_name] = Customer(customer_name)
        toppings = [self.available_toppings[n] for n in topping_names if n in self.available_toppings]
        pizza = Pizza(size, toppings)
        self.customers[customer_name].order.add_pizza(pizza)
        return self.customers[customer_name]

shop = PizzaShop()

# =====================
# Routes
# =====================
@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    customer_name = ""
    pizzas = []
    total_price = 0
    topping_names_selected = []
    selected_size = ""

    if request.method == "POST":
        customer_name = request.form.get("customerName", "").strip()
        selected_size = request.form.get("pizzaSize", "")
        topping_names_selected = request.form.getlist("topping")

        try:
            customer = shop.add_order(customer_name, selected_size, topping_names_selected)
            pizzas = customer.order.pizzas
            total_price = customer.order.total()
            print(f"Customer: {customer_name}, Size: {selected_size}, Toppings: {topping_names_selected}")
            for pizza in pizzas:
                print(f"Pizza: {pizza.size}, Toppings: {[t.name for t in pizza.toppings]}")
        except ValueError as e:
            message = str(e)

    print("Available toppings:", list(shop.available_toppings.keys()))

    return render_template("index.html",
                           message=message,
                           customer_name=customer_name,
                           pizzas=pizzas,
                           total_price=total_price,
                           topping_names_selected=topping_names_selected,
                           selected_size=selected_size,
                           shop=shop)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)