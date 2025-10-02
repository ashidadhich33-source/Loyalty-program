import { useState } from 'react';
import { Plus, Minus, ShoppingCart, CreditCard, Package, Search } from 'lucide-react';

export default function POS() {
  const [cart, setCart] = useState<Array<{
    id: number;
    name: string;
    price: number;
    quantity: number;
  }>>([]);

  const products = [
    { id: 1, name: 'Kids T-Shirt', price: 15.99, stock: 50 },
    { id: 2, name: 'Children\'s Jeans', price: 25.99, stock: 30 },
    { id: 3, name: 'Kids Sneakers', price: 45.99, stock: 20 },
    { id: 4, name: 'Children\'s Hat', price: 12.99, stock: 25 },
  ];

  const addToCart = (product: typeof products[0]) => {
    const existingItem = cart.find(item => item.id === product.id);
    if (existingItem) {
      setCart(cart.map(item =>
        item.id === product.id
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ));
    } else {
      setCart([...cart, { ...product, quantity: 1 }]);
    }
  };

  const updateQuantity = (id: number, quantity: number) => {
    if (quantity <= 0) {
      setCart(cart.filter(item => item.id !== id));
    } else {
      setCart(cart.map(item =>
        item.id === id ? { ...item, quantity } : item
      ));
    }
  };

  const removeFromCart = (id: number) => {
    setCart(cart.filter(item => item.id !== id));
  };

  const getTotal = () => {
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const getTax = () => {
    return getTotal() * 0.08; // 8% tax
  };

  const getGrandTotal = () => {
    return getTotal() + getTax();
  };

  return (
    <div className="h-screen flex">
      {/* Products Section */}
      <div className="flex-1 p-6">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-secondary-900 mb-2">Point of Sale</h1>
          <p className="text-secondary-600">Select products and process sales</p>
        </div>

        {/* Search */}
        <div className="mb-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-secondary-400" />
            <input
              type="text"
              placeholder="Search products..."
              className="input pl-10 w-full"
            />
          </div>
        </div>

        {/* Products Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {products.map((product) => (
            <div key={product.id} className="card hover:shadow-lg transition-shadow cursor-pointer">
              <div className="card-content p-4">
                <div className="aspect-square bg-secondary-100 rounded-lg flex items-center justify-center mb-3">
                  <Package className="w-8 h-8 text-secondary-400" />
                </div>
                <h3 className="font-semibold text-secondary-900 mb-1">{product.name}</h3>
                <p className="text-lg font-bold text-primary-600 mb-2">${product.price}</p>
                <p className="text-sm text-secondary-500 mb-3">{product.stock} in stock</p>
                <button
                  onClick={() => addToCart(product)}
                  className="btn btn-primary w-full"
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Add to Cart
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Cart Section */}
      <div className="w-96 bg-white border-l border-secondary-200 p-6 flex flex-col">
        <div className="mb-6">
          <h2 className="text-xl font-bold text-secondary-900 mb-2">Shopping Cart</h2>
          <p className="text-secondary-600">{cart.length} items</p>
        </div>

        {/* Cart Items */}
        <div className="flex-1 overflow-y-auto mb-6">
          {cart.length === 0 ? (
            <div className="text-center py-8">
              <ShoppingCart className="w-12 h-12 text-secondary-400 mx-auto mb-3" />
              <p className="text-secondary-600">Cart is empty</p>
            </div>
          ) : (
            <div className="space-y-3">
              {cart.map((item) => (
                <div key={item.id} className="flex items-center gap-3 p-3 bg-secondary-50 rounded-lg">
                  <div className="flex-1">
                    <h4 className="font-medium text-secondary-900">{item.name}</h4>
                    <p className="text-sm text-secondary-600">${item.price}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => updateQuantity(item.id, item.quantity - 1)}
                      className="btn btn-ghost btn-sm"
                    >
                      <Minus className="w-4 h-4" />
                    </button>
                    <span className="w-8 text-center font-medium">{item.quantity}</span>
                    <button
                      onClick={() => updateQuantity(item.id, item.quantity + 1)}
                      className="btn btn-ghost btn-sm"
                    >
                      <Plus className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => removeFromCart(item.id)}
                      className="btn btn-ghost btn-sm text-error-600 hover:bg-error-50 ml-2"
                    >
                      <Minus className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Cart Summary */}
        {cart.length > 0 && (
          <div className="border-t border-secondary-200 pt-6">
            <div className="space-y-2 mb-4">
              <div className="flex justify-between">
                <span className="text-secondary-600">Subtotal:</span>
                <span className="font-medium">${getTotal().toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-secondary-600">Tax (8%):</span>
                <span className="font-medium">${getTax().toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-lg font-bold border-t border-secondary-200 pt-2">
                <span>Total:</span>
                <span>${getGrandTotal().toFixed(2)}</span>
              </div>
            </div>

            <div className="space-y-3">
              <button className="btn btn-primary w-full">
                <CreditCard className="w-4 h-4 mr-2" />
                Process Payment
              </button>
              <button className="btn btn-outline w-full">
                Save as Draft
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}