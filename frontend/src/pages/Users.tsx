import { useState } from 'react';
import { useQuery } from 'react-query';
import { api, endpoints } from '../services/api';
import { Plus, Search, Filter, MoreHorizontal, Edit, Trash2, UserPlus } from 'lucide-react';

interface User {
  id: string;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  role: string;
  status: string;
  created_at: string;
  company?: {
    id: string;
    name: string;
  };
}

export default function Users() {
  const [search, setSearch] = useState('');
  const [role, setRole] = useState('');
  const [status, setStatus] = useState('');
  const [page, setPage] = useState(1);
  const [limit] = useState(10);

  const { data, isLoading, error } = useQuery(
    ['users', { search, role, status, page, limit }],
    async () => {
      const params = new URLSearchParams({
        page: page.toString(),
        limit: limit.toString(),
        ...(search && { search }),
        ...(role && { role }),
        ...(status && { status }),
      });

      const response = await api.get(`${endpoints.users.list}?${params}`);
      return response.data.data;
    }
  );

  const users = data?.users || [];
  const pagination = data?.pagination;

  const getRoleBadgeColor = (role: string) => {
    switch (role) {
      case 'admin': return 'error';
      case 'manager': return 'warning';
      case 'employee': return 'primary';
      default: return 'secondary';
    }
  };

  const getStatusBadgeColor = (status: string) => {
    switch (status) {
      case 'active': return 'success';
      case 'inactive': return 'secondary';
      case 'pending': return 'warning';
      case 'suspended': return 'error';
      default: return 'secondary';
    }
  };

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <p className="text-error-600 mb-4">Failed to load users</p>
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
          <h1 className="text-3xl font-bold text-secondary-900">Users</h1>
          <p className="text-secondary-600 mt-1">Manage system users and their permissions</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="btn btn-outline">
            <Filter className="w-4 h-4 mr-2" />
            Filters
          </button>
          <button className="btn btn-primary">
            <UserPlus className="w-4 h-4 mr-2" />
            Add User
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
                  placeholder="Search users..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="input pl-10"
                />
              </div>
            </div>
            <div>
              <label className="text-sm font-medium text-secondary-700 mb-2 block">Role</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="input"
              >
                <option value="">All Roles</option>
                <option value="admin">Admin</option>
                <option value="manager">Manager</option>
                <option value="employee">Employee</option>
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
              </select>
            </div>
            <div className="flex items-end">
              <button
                onClick={() => {
                  setSearch('');
                  setRole('');
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

      {/* Users Table */}
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
          ) : users.length === 0 ? (
            <div className="p-6 text-center">
              <UserPlus className="w-12 h-12 text-secondary-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-secondary-900 mb-2">No users found</h3>
              <p className="text-secondary-600 mb-4">Get started by adding your first user.</p>
              <button className="btn btn-primary">
                <UserPlus className="w-4 h-4 mr-2" />
                Add User
              </button>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="table">
                <thead className="table-header">
                  <tr>
                    <th className="table-head">User</th>
                    <th className="table-head">Role</th>
                    <th className="table-head">Status</th>
                    <th className="table-head">Company</th>
                    <th className="table-head">Created</th>
                    <th className="table-head">Actions</th>
                  </tr>
                </thead>
                <tbody className="table-body">
                  {users.map((user: User) => (
                    <tr key={user.id} className="table-row">
                      <td className="table-cell">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                            <span className="text-sm font-medium text-primary-600">
                              {user.first_name?.[0] || user.username[0].toUpperCase()}
                            </span>
                          </div>
                          <div>
                            <p className="font-medium text-secondary-900">
                              {user.first_name && user.last_name 
                                ? `${user.first_name} ${user.last_name}`
                                : user.username
                              }
                            </p>
                            <p className="text-sm text-secondary-500">{user.email}</p>
                          </div>
                        </div>
                      </td>
                      <td className="table-cell">
                        <span className={`badge badge-${getRoleBadgeColor(user.role)}`}>
                          {user.role}
                        </span>
                      </td>
                      <td className="table-cell">
                        <span className={`badge badge-${getStatusBadgeColor(user.status)}`}>
                          {user.status}
                        </span>
                      </td>
                      <td className="table-cell">
                        <span className="text-sm text-secondary-600">
                          {user.company?.name || 'No company'}
                        </span>
                      </td>
                      <td className="table-cell">
                        <span className="text-sm text-secondary-600">
                          {new Date(user.created_at).toLocaleDateString()}
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