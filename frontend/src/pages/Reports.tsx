import { useState } from 'react';
import { Plus, Search, Filter, BarChart3, Download, Eye, Edit, Trash2 } from 'lucide-react';

export default function Reports() {
  const [search, setSearch] = useState('');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-secondary-900">Reports</h1>
          <p className="text-secondary-600 mt-1">Generate and manage business reports</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="btn btn-outline">
            <Filter className="w-4 h-4 mr-2" />
            Filters
          </button>
          <button className="btn btn-primary">
            <Plus className="w-4 h-4 mr-2" />
            New Report
          </button>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-secondary-600">Total Reports</p>
                <p className="text-2xl font-bold text-secondary-900">24</p>
              </div>
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-primary-600" />
              </div>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-secondary-600">This Month</p>
                <p className="text-2xl font-bold text-success-600">8</p>
              </div>
              <div className="w-12 h-12 bg-success-100 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-success-600" />
              </div>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-secondary-600">Scheduled</p>
                <p className="text-2xl font-bold text-warning-600">5</p>
              </div>
              <div className="w-12 h-12 bg-warning-100 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-warning-600" />
              </div>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-secondary-600">Templates</p>
                <p className="text-2xl font-bold text-secondary-600">12</p>
              </div>
              <div className="w-12 h-12 bg-secondary-100 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-secondary-600" />
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
                  placeholder="Search reports..."
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
                <option value="sales">Sales</option>
                <option value="inventory">Inventory</option>
                <option value="financial">Financial</option>
                <option value="custom">Custom</option>
              </select>
            </div>
            <div>
              <label className="text-sm font-medium text-secondary-700 mb-2 block">Status</label>
              <select className="input">
                <option value="">All Status</option>
                <option value="active">Active</option>
                <option value="scheduled">Scheduled</option>
                <option value="archived">Archived</option>
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

      {/* Reports Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[
          {
            id: 1,
            name: 'Sales Report',
            category: 'Sales',
            description: 'Monthly sales performance and trends',
            status: 'active',
            lastRun: '2024-01-15',
            nextRun: '2024-02-15',
          },
          {
            id: 2,
            name: 'Inventory Report',
            category: 'Inventory',
            description: 'Stock levels and movement analysis',
            status: 'scheduled',
            lastRun: '2024-01-10',
            nextRun: '2024-01-20',
          },
          {
            id: 3,
            name: 'Financial Summary',
            category: 'Financial',
            description: 'Revenue, expenses, and profit analysis',
            status: 'active',
            lastRun: '2024-01-14',
            nextRun: '2024-02-14',
          },
          {
            id: 4,
            name: 'Customer Analysis',
            category: 'Custom',
            description: 'Customer behavior and preferences',
            status: 'archived',
            lastRun: '2024-01-05',
            nextRun: null,
          },
        ].map((report) => (
          <div key={report.id} className="card hover:shadow-lg transition-shadow">
            <div className="card-content">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="font-semibold text-secondary-900 mb-1">{report.name}</h3>
                  <p className="text-sm text-secondary-600">{report.description}</p>
                </div>
                <span className={`badge ${
                  report.status === 'active' ? 'badge-success' :
                  report.status === 'scheduled' ? 'badge-warning' :
                  'badge-secondary'
                }`}>
                  {report.status}
                </span>
              </div>
              
              <div className="space-y-2 mb-4">
                <div className="flex justify-between text-sm">
                  <span className="text-secondary-600">Category:</span>
                  <span className="text-secondary-900">{report.category}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-secondary-600">Last Run:</span>
                  <span className="text-secondary-900">{report.lastRun}</span>
                </div>
                {report.nextRun && (
                  <div className="flex justify-between text-sm">
                    <span className="text-secondary-600">Next Run:</span>
                    <span className="text-secondary-900">{report.nextRun}</span>
                  </div>
                )}
              </div>

              <div className="flex items-center gap-2">
                <button className="btn btn-ghost btn-sm flex-1">
                  <Eye className="w-4 h-4 mr-1" />
                  View
                </button>
                <button className="btn btn-ghost btn-sm">
                  <Download className="w-4 h-4" />
                </button>
                <button className="btn btn-ghost btn-sm">
                  <Edit className="w-4 h-4" />
                </button>
                <button className="btn btn-ghost btn-sm text-error-600 hover:bg-error-50">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      <div className="text-center py-12">
        <BarChart3 className="w-16 h-16 text-secondary-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-secondary-900 mb-2">No reports found</h3>
        <p className="text-secondary-600 mb-4">Get started by creating your first report.</p>
        <button className="btn btn-primary">
          <Plus className="w-4 h-4 mr-2" />
          New Report
        </button>
      </div>
    </div>
  );
}