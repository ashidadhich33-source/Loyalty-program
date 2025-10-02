import { useState } from 'react';
import { Plus, Search, Filter, Package, Edit, Trash2, MoreHorizontal } from 'lucide-react';

export default function Products() {
  const [search, setSearch] = useState('');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-secondary-900">Products</h1>
          <p className="text-secondary-600 mt-1">Manage your product catalog</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="btn btn-outline">
            <Filter className="w-4 h-4 mr-2" />
            Filters
          </button>
          <button className="btn btn-primary">
            <Plus className="w-4 h-4 mr-2" />
            Add Product
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="card-content">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="text-sm font-medium text-secondary-700 mb-2 block">Search</label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-secondary-400" />
                <input
                  type="text"
                  placeholder="Search products..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="input pl-10"
                />
              </div>
            </div>
            <div>
              <label className="text-sm font-medium text-secondary-700 mb-2 block">Category</label>
              <select className="input">
                <option value="">All Categories</option>
                <option value="clothing">Clothing</option>
                <option value="accessories">Accessories</option>
                <option value="shoes">Shoes</option>
              </select>
            </div>
            <div>
              <label className="text-sm font-medium text-secondary-700 mb-2 block">Status</label>
              <select className="input">
                <option value="">All Status</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
                <option value="out-of-stock">Out of Stock</option>
              </select>
            </div>
            <div className="flex items-end">
              <button className="btn btn-outline w-full">
                Clear Filters
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Products Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {[
          {
            id: 1,
            name: 'Kids T-Shirt',
            category: 'Clothing',
            price: 15.99,
            stock: 50,
            status: 'active',
            image: '/api/placeholder/300/300',
          },
          {
            id: 2,
            name: 'Children\'s Jeans',
            category: 'Clothing',
            price: 25.99,
            stock: 30,
            status: 'active',
            image: '/api/placeholder/300/300',
          },
          {
            id: 3,
            name: 'Kids Sneakers',
            category: 'Shoes',
            price: 45.99,
            stock: 0,
            status: 'out-of-stock',
            image: '/api/placeholder/300/300',
          },
          {
            id: 4,
            name: 'Children\'s Hat',
            category: 'Accessories',
            price: 12.99,
            stock: 25,
            status: 'active',
            image: '/api/placeholder/300/300',
          },
        ].map((product) => (
          <div key={product.id} className="card hover:shadow-lg transition-shadow">
            <div className="card-content p-0">
              <div className="aspect-square bg-secondary-100 rounded-t-lg flex items-center justify-center">
                <Package className="w-12 h-12 text-secondary-400" />
              </div>
              <div className="p-4">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="font-semibold text-secondary-900 line-clamp-2">{product.name}</h3>
                  <button className="btn btn-ghost btn-sm">
                    <MoreHorizontal className="w-4 h-4" />
                  </button>
                </div>
                <p className="text-sm text-secondary-600 mb-2">{product.category}</p>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-lg font-bold text-secondary-900">${product.price}</span>
                  <span className={`badge ${
                    product.status === 'active' ? 'badge-success' : 'badge-warning'
                  }`}>
                    {product.stock} in stock
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <button className="btn btn-ghost btn-sm flex-1">
                    <Edit className="w-4 h-4 mr-1" />
                    Edit
                  </button>
                  <button className="btn btn-ghost btn-sm text-error-600 hover:bg-error-50">
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      <div className="text-center py-12">
        <Package className="w-16 h-16 text-secondary-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-secondary-900 mb-2">No products found</h3>
        <p className="text-secondary-600 mb-4">Get started by adding your first product to the catalog.</p>
        <button className="btn btn-primary">
          <Plus className="w-4 h-4 mr-2" />
          Add Product
        </button>
      </div>
    </div>
  );
}