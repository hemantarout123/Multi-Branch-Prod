from flask import Flask, render_template_string, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Your products list remains unchanged
products = [ ... ]  # Keep the product list

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, products=products)

# Add to cart
@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = []

    data = request.get_json()
    product_id = data.get('product_id')

    product = next((p for p in products if p['id'] == product_id), None)

    if product:
        cart = session['cart']
        cart_item = next((item for item in cart if item['id'] == product_id), None)

        if cart_item:
            cart_item['quantity'] += 1
        else:
            cart.append({
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'image': product['image'],
                'quantity': 1
            })

        session['cart'] = cart
        session.modified = True  # Ensure session is saved
        return jsonify({'success': True, 'cart': cart})

    return jsonify({'success': False})

# Remove from cart
@app.route("/remove_from_cart", methods=["POST"])
def remove_from_cart():
    data = request.get_json()
    product_id = data.get('product_id')

    if 'cart' in session:
        cart = session['cart']
        cart = [item for item in cart if item['id'] != product_id]
        session['cart'] = cart
        session.modified = True
        return jsonify({'success': True, 'cart': cart})

    return jsonify({'success': False})

# Update quantity
@app.route("/update_quantity", methods=["POST"])
def update_quantity():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if 'cart' in session:
        cart = session['cart']
        cart_item = next((item for item in cart if item['id'] == product_id), None)

        if cart_item:
            if quantity <= 0:
                cart = [item for item in cart if item['id'] != product_id]
            else:
                cart_item['quantity'] = quantity

            session['cart'] = cart
            session.modified = True
            return jsonify({'success': True, 'cart': cart})

    return jsonify({'success': False})

# Get cart
@app.route("/get_cart")
def get_cart():
    return jsonify(session.get('cart', []))

# Checkout
@app.route("/checkout", methods=["POST"])
def checkout():
    cart = session.get('cart', [])
    if cart:
        # Here you could process payment
        session['cart'] = []
        session.modified = True
        return jsonify({'success': True, 'message': 'Order placed successfully!'})

    return jsonify({'success': False, 'message': 'Cart is empty!'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
