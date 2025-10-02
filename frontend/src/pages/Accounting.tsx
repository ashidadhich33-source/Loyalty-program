import { useState } from 'react';
import { Plus, Search, Filter, Calculator, Edit, Trash2, MoreHorizontal, DollarSign } from 'lucide-react';

export default function Accounting() {
  const [search, setSearch] = useState('');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-secondary-900">Accounting</h1>
          <p className="text-secondary-600 mt-1">Manage financial transactions and reports</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="btn btn-outline">
            <Filter className="w-4 h-4 mr-2" />
            Filters
          </button>
          <button className="btn btn-primary">
            <Plus className="w-4 h-4 mr-2" />
            New Entry
          </button>
        </div>
      </div>

      {/* Financial Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-secondary-600">Total Revenue</p>
                <p className="text-2xl font-bold text-success-600">$125,450</p>
                <p className="text-sm text-success-600">+12.5% from last month</p>
              </div>
              <div className="w-12 h-12 bg-success-100 rounded-lg flex items-center justify-center">
                <DollarSign className="w-6 h-6 text-success-600" />
              </div>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-secondary-600">Total Expenses</p>
                <p className="text-2xl font-bold text-error-600">$45,230</p>
                <p className="text-sm text-error-600">+8.2% from last month</p>
              </div>
              <div className="w-12 h-12 bg-error-100 rounded-lg flex items-center justify-center">
                <Calculator className="w-6 h-6 text-error-600" />
              </div>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-secondary-600">Net Profit</p>
                <p className="text-2xl font-bold text-primary-600">$80,220</p>
                <p className="text-sm text-primary-600">+15.3% from last month</p>
              </div>
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                <Calculator className="w-6 h-6 text-primary-600" />
              </div>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-secondary-600">Outstanding</p>
                <p className="text-2xl font-bold text-warning-600">$12,450</p>
                <p className="text-sm text-warning-600">5 pending invoices</p>
              </div>
              <div className="w-12 h-12 bg-warning-100 rounded-lg flex items-center justify-center">
                <Calculator className="w-6 h-6 text-warning-600" />
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
                  placeholder="Search transactions..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="input pl-10"
                />
              </div>
            </div>
            <div>
              <label className="text-sm font-medium text-secondary-700 mb-2 block">Type</label>
              <select className="input">
                <option value="">All Types</option>
                <option value="invoice">Invoice</option>
                <option value="payment">Payment</option>
                <option value="expense">Expense</option>
                <option value="refund">Refund</option>
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

      {/* Transactions Table */}
      <div className="card">
        <div className="card-content p-0">
          <div className="overflow-x-auto">
            <table className="table">
              <thead className="table-header">
                <tr>
                  <th className="table-head">Transaction</th>
                  <th className="table-head">Type</th>
                  <th className="table-head">Date</th>
                  <th className="table-head">Account</th>
                  <th className="table-head">Amount</th>
                  <th className="table-head">Status</th>
                  <th className="table-head">Actions</th>
                </tr>
              </thead>
              <tbody className="table-body">
                {[
                  {
                    id: 'TXN001',
                    type: 'invoice',
                    date: '2024-01-15',
                    account: 'Sales Account',
                    amount: 125.50,
                    status: 'paid',
                  },
                  {
                    id: 'TXN002',
                    type: 'payment',
                    date: '2024-01-14',
                    account: 'Bank Account',
                    amount: -89.99,
                    status: 'completed',
                  },
                  {
                    id: 'TXN003',
                    type: 'expense',
                    date: '2024-01-13',
                    account: 'Office Supplies',
                    amount: -234.75,
                    status: 'pending',
                  },
                  {
                    id: 'TXN004',
                    type: 'refund',
                    date: '2024-01-12',
                    account: 'Sales Account',
                    amount: -67.25,
                    status: 'completed',
                  },
                ].map((transaction) => (
                  <tr key={transaction.id} className="table-row">
                    <td className="table-cell">
                      <div className="font-medium text-secondary-900">{transaction.id}</div>
                    </td>
                    <td className="table-cell">
                      <span className={`badge ${
                        transaction.type === 'invoice' ? 'badge-success' :
                        transaction.type === 'payment' ? 'badge-primary' :
                        transaction.type === 'expense' ? 'badge-error' :
                        'badge-warning'
                      }`}>
                        {transaction.type}
                      </span>
                    </td>
                    <td className="table-cell">
                      <div className="text-secondary-600">{transaction.date}</div>
                    </td>
                    <td className="table-cell">
                      <div className="text-secondary-900">{transaction.account}</div>
                    </td>
                    <td className="table-cell">
                      <div className={`font-semibold ${
                        transaction.amount > 0 ? 'text-success-600' : 'text-error-600'
                      }`}>
                        ${Math.abs(transaction.amount)}
                      </div>
                    </td>
                    <td className="table-cell">
                      <span className={`badge ${
                        transaction.status === 'paid' || transaction.status === 'completed' ? 'badge-success' :
                        transaction.status === 'pending' ? 'badge-warning' :
                        'badge-secondary'
                      }`}>
                        {transaction.status}
                      </span>
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
        <Calculator className="w-16 h-16 text-secondary-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-secondary-900 mb-2">No transactions found</h3>
        <p className="text-secondary-600 mb-4">Get started by creating your first accounting entry.</p>
        <button className="btn btn-primary">
          <Plus className="w-4 h-4 mr-2" />
          New Entry
        </button>
      </div>
    </div>
  );
}