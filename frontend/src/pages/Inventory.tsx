import { useState } from 'react';
import { Plus, Search, Filter, Package, Edit, Trash2, MoreHorizontal, AlertTriangle } from 'lucide-react';

export default function Inventory() {
  const [search, setSearch] = useState('');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-secondary-900">Inventory</h1>
          <p className="text-secondary-600 mt-1">Manage stock levels and warehouse operations</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="btn btn-outline">
            <Filter className="w-4 h-4 mr-2" />
            Filters
          </button>
          <button className="btn btn-primary">
            <Plus className="w-4 h-4 mr-2" />
            Add Stock
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-secondary-600">Total Products</p>
                <p className="text-2xl font-bold text-secondary-900">1,250</p>
              </div>
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                <Package className="w-6 h-6 text-primary-600" />
              </div>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-secondary-600">Low Stock</p>
                <p className="text-2xl font-bold text-warning-600">12</p>
              </div>
              <div className="w-12 h-12 bg-warning-100 rounded-lg flex items-center justify-center">
                <AlertTriangle className="w-6 h-6 text-warning-600" />
              </div>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-secondary-600">Out of Stock</p>
                <p className="text-2xl font-bold text-error-600">5</p>
              </div>
              <div className="w-12 h-12 bg-error-100 rounded-lg flex items-center justify-center">
                <AlertTriangle className="w-6 h-6 text-error-600" />
              </div>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-secondary-600">Total Value</p>
                <p className="text-2xl font-bold text-success-600">$45,250</p>
              </div>
              <div className="w-12 h-12 bg-success-100 rounded-lg flex items-center justify-center">
                <Package className="w-6 h-6 text-success-600" />
              </div>
            </div>
          </div>
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
                  placeholder="Search inventory..."
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
              <label className="text-sm font-medium text-secondary-700 mb-2 block">Stock Status</label>
              <select className="input">
                <option value="">All Status</option>
                <option value="in-stock">In Stock</option>
                <option value="low-stock">Low Stock</option>
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

      {/* Inventory Table */}
      <div className="card">
        <div className="card-content p-0">
          <div className="overflow-x-auto">
            <table className="table">
              <thead className="table-header">
                <tr>
                  <th className="table-head">Product</th>
                  <th className="table-head">SKU</th>
                  <th className="table-head">Category</th>
                  <th className="table-head">Stock</th>
                  <th className="table-head">Status</th>
                  <th className="table-head">Value</th>
                  <th className="table-head">Actions</th>
                </tr>
              </thead>
              <tbody className="table-body">
                {[
                  {
                    id: 1,
                    name: 'Kids T-Shirt',
                    sku: 'KT001',
                    category: 'Clothing',
                    stock: 50,
                    status: 'in-stock',
                    value: 799.50,
                  },
                  {
                    id: 2,
                    name: 'Children\'s Jeans',
                    sku: 'CJ002',
                    category: 'Clothing',
                    stock: 5,
                    status: 'low-stock',
                    value: 1299.50,
                  },
                  {
                    id: 3,
                    name: 'Kids Sneakers',
                    sku: 'KS003',
                    category: 'Shoes',
                    stock: 0,
                    status: 'out-of-stock',
                    value: 0,
                  },
                  {
                    id: 4,
                    name: 'Children\'s Hat',
                    sku: 'CH004',
                    category: 'Accessories',
                    stock: 25,
                    status: 'in-stock',
                    value: 324.75,
                  },
                ].map((item) => (
                  <tr key={item.id} className="table-row">
                    <td className="table-cell">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-secondary-100 rounded-lg flex items-center justify-center">
                          <Package className="w-5 h-5 text-secondary-600" />
                        </div>
                        <div>
                          <p className="font-medium text-secondary-900">{item.name}</p>
                        </div>
                      </div>
                    </td>
                    <td className="table-cell">
                      <span className="text-sm text-secondary-600">{item.sku}</span>
                    </td>
                    <td className="table-cell">
                      <span className="text-sm text-secondary-600">{item.category}</span>
                    </td>
                    <td className="table-cell">
                      <span className="font-medium text-secondary-900">{item.stock}</span>
                    </td>
                    <td className="table-cell">
                      <span className={`badge ${
                        item.status === 'in-stock' ? 'badge-success' :
                        item.status === 'low-stock' ? 'badge-warning' :
                        'badge-error'
                      }`}>
                        {item.status}
                      </span>
                    </td>
                    <td className="table-cell">
                      <span className="font-semibold text-secondary-900">${item.value}</span>
                    </td>
                    <td className="table-cell">
                      <div className="flex items-center gap-2">
                        <button className="btn btn-ghost btn-sm">
                          <Edit className="w-4 h-4" />
                        </button>
                        <button className="btn btn-ghost btn-sm text-error-600 hover:bg-error-50">
                          <Trash2 className="w-4 h-4" />
                        </button>
                        <button className="btn btn-ghost btn-sm">
                          <MoreHorizontal className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Empty State */}
      <div className="text-center py-12">
        <Package className="w-16 h-16 text-secondary-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-secondary-900 mb-2">No inventory found</h3>
        <p className="text-secondary-600 mb-4">Get started by adding products to your inventory.</p>
        <button className="btn btn-primary">
          <Plus className="w-4 h-4 mr-2" />
          Add Product
        </button>
      </div>
    </div>
  );
}