import { useState } from 'react';
import { Plus, Search, Filter, ShoppingCart, Edit, Trash2, MoreHorizontal } from 'lucide-react';

export default function Sales() {
  const [search, setSearch] = useState('');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-secondary-900">Sales</h1>
          <p className="text-secondary-600 mt-1">Manage sales orders and quotations</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="btn btn-outline">
            <Filter className="w-4 h-4 mr-2" />
            Filters
          </button>
          <button className="btn btn-primary">
            <Plus className="w-4 h-4 mr-2" />
            New Sale
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
                  placeholder="Search sales..."
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
                <option value="quotation">Quotation</option>
                <option value="sale">Sale</option>
                <option value="done">Done</option>
                <option value="cancel">Cancelled</option>
              </select>
            </div>
            <div>
              <label className="text-sm font-medium text-secondary-700 mb-2 block">Date Range</label>
              <select className="input">
                <option value="">All Time</option>
                <option value="today">Today</option>
                <option value="week">This Week</option>
                <option value="month">This Month</option>
                <option value="year">This Year</option>
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

      {/* Sales Table */}
      <div className="card">
        <div className="card-content p-0">
          <div className="overflow-x-auto">
            <table className="table">
              <thead className="table-header">
                <tr>
                  <th className="table-head">Order</th>
                  <th className="table-head">Customer</th>
                  <th className="table-head">Date</th>
                  <th className="table-head">Status</th>
                  <th className="table-head">Total</th>
                  <th className="table-head">Actions</th>
                </tr>
              </thead>
              <tbody className="table-body">
                {[
                  {
                    id: 'SO001',
                    customer: 'John Doe',
                    date: '2024-01-15',
                    status: 'done',
                    total: 125.50,
                  },
                  {
                    id: 'SO002',
                    customer: 'Jane Smith',
                    date: '2024-01-14',
                    status: 'sale',
                    total: 89.99,
                  },
                  {
                    id: 'SO003',
                    customer: 'Bob Johnson',
                    date: '2024-01-13',
                    status: 'quotation',
                    total: 234.75,
                  },
                  {
                    id: 'SO004',
                    customer: 'Alice Brown',
                    date: '2024-01-12',
                    status: 'draft',
                    total: 67.25,
                  },
                ].map((sale) => (
                  <tr key={sale.id} className="table-row">
                    <td className="table-cell">
                      <div className="font-medium text-secondary-900">{sale.id}</div>
                    </td>
                    <td className="table-cell">
                      <div className="text-secondary-900">{sale.customer}</div>
                    </td>
                    <td className="table-cell">
                      <div className="text-secondary-600">{sale.date}</div>
                    </td>
                    <td className="table-cell">
                      <span className={`badge ${
                        sale.status === 'done' ? 'badge-success' :
                        sale.status === 'sale' ? 'badge-primary' :
                        sale.status === 'quotation' ? 'badge-warning' :
                        'badge-secondary'
                      }`}>
                        {sale.status}
                      </span>
                    </td>
                    <td className="table-cell">
                      <div className="font-semibold text-secondary-900">${sale.total}</div>
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
        <ShoppingCart className="w-16 h-16 text-secondary-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-secondary-900 mb-2">No sales found</h3>
        <p className="text-secondary-600 mb-4">Get started by creating your first sale order.</p>
        <button className="btn btn-primary">
          <Plus className="w-4 h-4 mr-2" />
          New Sale
        </button>
      </div>
    </div>
  );
}