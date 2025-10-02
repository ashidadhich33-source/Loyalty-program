import { useState } from 'react';
import { useQuery } from 'react-query';
import { api, endpoints } from '../services/api';
import { Plus, Search, Filter, MoreHorizontal, Edit, Trash2, Building2 } from 'lucide-react';

interface Company {
  id: string;
  name: string;
  legal_name?: string;
  email?: string;
  type: string;
  status: string;
  created_at: string;
  users?: Array<{
    id: string;
    username: string;
    role: string;
  }>;
}

export default function Companies() {
  const [search, setSearch] = useState('');
  const [type, setType] = useState('');
  const [status, setStatus] = useState('');
  const [page, setPage] = useState(1);
  const [limit] = useState(10);

  const { data, isLoading, error } = useQuery(
    ['companies', { search, type, status, page, limit }],
    async () => {
      const params = new URLSearchParams({
        page: page.toString(),
        limit: limit.toString(),
        ...(search && { search }),
        ...(type && { type }),
        ...(status && { status }),
      });

      const response = await api.get(`${endpoints.companies.list}?${params}`);
      return response.data.data;
    }
  );

  const companies = data?.companies || [];
  const pagination = data?.pagination;

  const getTypeBadgeColor = (type: string) => {
    switch (type) {
      case 'retail': return 'primary';
      case 'wholesale': return 'success';
      case 'manufacturing': return 'warning';
      case 'service': return 'secondary';
      default: return 'secondary';
    }
  };

  const getStatusBadgeColor = (status: string) => {
    switch (status) {
      case 'active': return 'success';
      case 'inactive': return 'secondary';
      case 'pending': return 'warning';
      case 'suspended': return 'error';
      case 'trial': return 'primary';
      default: return 'secondary';
    }
  };

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <p className="text-error-600 mb-4">Failed to load companies</p>
          <button className="btn btn-primary" onClick={() => window.location.reload()}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-secondary-900">Companies</h1>
          <p className="text-secondary-600 mt-1">Manage companies and their settings</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="btn btn-outline">
            <Filter className="w-4 h-4 mr-2" />
            Filters
          </button>
          <button className="btn btn-primary">
            <Plus className="w-4 h-4 mr-2" />
            Add Company
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
                  placeholder="Search companies..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="input pl-10"
                />
              </div>
            </div>
            <div>
              <label className="text-sm font-medium text-secondary-700 mb-2 block">Type</label>
              <select
                value={type}
                onChange={(e) => setType(e.target.value)}
                className="input"
              >
                <option value="">All Types</option>
                <option value="retail">Retail</option>
                <option value="wholesale">Wholesale</option>
                <option value="manufacturing">Manufacturing</option>
                <option value="service">Service</option>
              </select>
            </div>
            <div>
              <label className="text-sm font-medium text-secondary-700 mb-2 block">Status</label>
              <select
                value={status}
                onChange={(e) => setStatus(e.target.value)}
                className="input"
              >
                <option value="">All Status</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
                <option value="pending">Pending</option>
                <option value="suspended">Suspended</option>
                <option value="trial">Trial</option>
              </select>
            </div>
            <div className="flex items-end">
              <button
                onClick={() => {
                  setSearch('');
                  setType('');
                  setStatus('');
                  setPage(1);
                }}
                className="btn btn-outline w-full"
              >
                Clear Filters
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Companies Table */}
      <div className="card">
        <div className="card-content p-0">
          {isLoading ? (
            <div className="p-6">
              <div className="space-y-4">
                {[...Array(5)].map((_, i) => (
                  <div key={i} className="flex items-center space-x-4 animate-pulse">
                    <div className="w-10 h-10 bg-secondary-200 rounded-full"></div>
                    <div className="flex-1 space-y-2">
                      <div className="h-4 bg-secondary-200 rounded w-1/4"></div>
                      <div className="h-3 bg-secondary-200 rounded w-1/2"></div>
                    </div>
                    <div className="h-6 bg-secondary-200 rounded w-16"></div>
                    <div className="h-6 bg-secondary-200 rounded w-20"></div>
                  </div>
                ))}
              </div>
            </div>
          ) : companies.length === 0 ? (
            <div className="p-6 text-center">
              <Building2 className="w-12 h-12 text-secondary-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-secondary-900 mb-2">No companies found</h3>
              <p className="text-secondary-600 mb-4">Get started by adding your first company.</p>
              <button className="btn btn-primary">
                <Plus className="w-4 h-4 mr-2" />
                Add Company
              </button>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="table">
                <thead className="table-header">
                  <tr>
                    <th className="table-head">Company</th>
                    <th className="table-head">Type</th>
                    <th className="table-head">Status</th>
                    <th className="table-head">Users</th>
                    <th className="table-head">Created</th>
                    <th className="table-head">Actions</th>
                  </tr>
                </thead>
                <tbody className="table-body">
                  {companies.map((company: Company) => (
                    <tr key={company.id} className="table-row">
                      <td className="table-cell">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                            <Building2 className="w-5 h-5 text-primary-600" />
                          </div>
                          <div>
                            <p className="font-medium text-secondary-900">{company.name}</p>
                            <p className="text-sm text-secondary-500">{company.email || 'No email'}</p>
                          </div>
                        </div>
                      </td>
                      <td className="table-cell">
                        <span className={`badge badge-${getTypeBadgeColor(company.type)}`}>
                          {company.type}
                        </span>
                      </td>
                      <td className="table-cell">
                        <span className={`badge badge-${getStatusBadgeColor(company.status)}`}>
                          {company.status}
                        </span>
                      </td>
                      <td className="table-cell">
                        <span className="text-sm text-secondary-600">
                          {company.users?.length || 0} users
                        </span>
                      </td>
                      <td className="table-cell">
                        <span className="text-sm text-secondary-600">
                          {new Date(company.created_at).toLocaleDateString()}
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
          )}
        </div>

        {/* Pagination */}
        {pagination && pagination.pages > 1 && (
          <div className="card-footer">
            <div className="flex items-center justify-between">
              <p className="text-sm text-secondary-600">
                Showing {((pagination.page - 1) * pagination.limit) + 1} to{' '}
                {Math.min(pagination.page * pagination.limit, pagination.total)} of{' '}
                {pagination.total} results
              </p>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setPage(page - 1)}
                  disabled={page === 1}
                  className="btn btn-outline btn-sm"
                >
                  Previous
                </button>
                <span className="text-sm text-secondary-600">
                  Page {pagination.page} of {pagination.pages}
                </span>
                <button
                  onClick={() => setPage(page + 1)}
                  disabled={page === pagination.pages}
                  className="btn btn-outline btn-sm"
                >
                  Next
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}