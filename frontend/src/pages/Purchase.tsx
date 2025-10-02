import { useState } from 'react';
import { Plus, Search, Filter, ShoppingBag, Edit, Trash2, MoreHorizontal } from 'lucide-react';

export default function Purchase() {
  const [search, setSearch] = useState('');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-secondary-900">Purchase</h1>
          <p className="text-secondary-600 mt-1">Manage purchase orders and suppliers</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="btn btn-outline">
            <Filter className="w-4 h-4 mr-2" />
            Filters
          </button>
          <button className="btn btn-primary">
            <Plus className="w-4 h-4 mr-2" />
            New Purchase
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
                  placeholder="Search purchases..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="input pl-10"
                />
              </div>
            </div>
            <div>
              <label className="text-sm font-medium text-secondary-700 mb-2 block">Status</label>
              <select className="input">
                <option value="">All Status</option>
                <option value="draft">Draft</option>
                <option value="sent">Sent</option>
                <option value="to_approve">To Approve</option>
                <option value="purchase">Purchase Order</option>
                <option value="done">Done</option>
                <option value="cancel">Cancelled</option>
              </select>
            </div>
            <div>
              <label className="text-sm font-medium text-secondary-700 mb-2 block">Supplier</label>
              <select className="input">
                <option value="">All Suppliers</option>
                <option value="supplier1">Supplier 1</option>
                <option value="supplier2">Supplier 2</option>
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

      {/* Purchase Orders Table */}
      <div className="card">
        <div className="card-content p-0">
          <div className="overflow-x-auto">
            <table className="table">
              <thead className="table-header">
                <tr>
                  <th className="table-head">Order</th>
                  <th className="table-head">Supplier</th>
                  <th className="table-head">Date</th>
                  <th className="table-head">Status</th>
                  <th className="table-head">Total</th>
                  <th className="table-head">Actions</th>
                </tr>
              </thead>
              <tbody className="table-body">
                {[
                  {
                    id: 'PO001',
                    supplier: 'Kids Clothing Co.',
                    date: '2024-01-15',
                    status: 'done',
                    total: 1250.50,
                  },
                  {
                    id: 'PO002',
                    supplier: 'Fashion Supplier',
                    date: '2024-01-14',
                    status: 'purchase',
                    total: 899.99,
                  },
                  {
                    id: 'PO003',
                    supplier: 'Accessories Inc.',
                    date: '2024-01-13',
                    status: 'to_approve',
                    total: 234.75,
                  },
                  {
                    id: 'PO004',
                    supplier: 'Shoe Company',
                    date: '2024-01-12',
                    status: 'draft',
                    total: 567.25,
                  },
                ].map((order) => (
                  <tr key={order.id} className="table-row">
                    <td className="table-cell">
                      <div className="font-medium text-secondary-900">{order.id}</div>
                    </td>
                    <td className="table-cell">
                      <div className="text-secondary-900">{order.supplier}</div>
                    </td>
                    <td className="table-cell">
                      <div className="text-secondary-600">{order.date}</div>
                    </td>
                    <td className="table-cell">
                      <span className={`badge ${
                        order.status === 'done' ? 'badge-success' :
                        order.status === 'purchase' ? 'badge-primary' :
                        order.status === 'to_approve' ? 'badge-warning' :
                        'badge-secondary'
                      }`}>
                        {order.status}
                      </span>
                    </td>
                    <td className="table-cell">
                      <div className="font-semibold text-secondary-900">${order.total}</div>
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
        <ShoppingBag className="w-16 h-16 text-secondary-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-secondary-900 mb-2">No purchase orders found</h3>
        <p className="text-secondary-600 mb-4">Get started by creating your first purchase order.</p>
        <button className="btn btn-primary">
          <Plus className="w-4 h-4 mr-2" />
          New Purchase
        </button>
      </div>
    </div>
  );
}