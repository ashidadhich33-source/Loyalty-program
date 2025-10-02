import { useQuery } from 'react-query';
import { api, endpoints } from '../services/api';
import { Users, Building2, Package, TrendingUp, DollarSign, ShoppingCart } from 'lucide-react';

interface DashboardStats {
  users: {
    total: number;
    active: number;
    inactive: number;
  };
  companies: {
    total: number;
    active: number;
    inactive: number;
  };
  sales: {
    total: number;
    today: number;
    growth: number;
  };
  revenue: {
    total: number;
    today: number;
    growth: number;
  };
}

export default function Dashboard() {
  const { data: stats, isLoading } = useQuery<DashboardStats>(
    'dashboard-stats',
    async () => {
      const [usersRes, companiesRes] = await Promise.all([
        api.get(endpoints.users.stats),
        api.get(endpoints.companies.stats),
      ]);

      return {
        users: usersRes.data.data.stats,
        companies: companiesRes.data.data.stats,
        sales: {
          total: 1250,
          today: 45,
          growth: 12.5,
        },
        revenue: {
          total: 125000,
          today: 4500,
          growth: 8.2,
        },
      };
    }
  );

  const statCards = [
    {
      title: 'Total Users',
      value: stats?.users.total || 0,
      change: '+12%',
      changeType: 'positive' as const,
      icon: Users,
      color: 'primary',
    },
    {
      title: 'Active Companies',
      value: stats?.companies.active || 0,
      change: '+5%',
      changeType: 'positive' as const,
      icon: Building2,
      color: 'success',
    },
    {
      title: 'Total Sales',
      value: stats?.sales.total || 0,
      change: `+${stats?.sales.growth || 0}%`,
      changeType: 'positive' as const,
      icon: ShoppingCart,
      color: 'warning',
    },
    {
      title: 'Revenue',
      value: `$${(stats?.revenue.total || 0).toLocaleString()}`,
      change: `+${stats?.revenue.growth || 0}%`,
      changeType: 'positive' as const,
      icon: DollarSign,
      color: 'success',
    },
  ];

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-secondary-900">Dashboard</h1>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="card animate-pulse">
              <div className="card-content">
                <div className="h-4 bg-secondary-200 rounded w-3/4 mb-2"></div>
                <div className="h-8 bg-secondary-200 rounded w-1/2"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-secondary-900">Dashboard</h1>
          <p className="text-secondary-600 mt-1">Welcome back! Here's what's happening with your business.</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="btn btn-outline">
            <TrendingUp className="w-4 h-4 mr-2" />
            View Reports
          </button>
          <button className="btn btn-primary">
            <Package className="w-4 h-4 mr-2" />
            Add Product
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => (
          <div key={index} className="card hover:shadow-lg transition-shadow">
            <div className="card-content">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-secondary-600">{stat.title}</p>
                  <p className="text-2xl font-bold text-secondary-900 mt-1">{stat.value}</p>
                </div>
                <div className={`w-12 h-12 rounded-lg flex items-center justify-center bg-${stat.color}-100`}>
                  <stat.icon className={`w-6 h-6 text-${stat.color}-600`} />
                </div>
              </div>
              <div className="mt-4 flex items-center">
                <span className={`text-sm font-medium ${
                  stat.changeType === 'positive' ? 'text-success-600' : 'text-error-600'
                }`}>
                  {stat.change}
                </span>
                <span className="text-sm text-secondary-500 ml-2">from last month</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Charts and Tables */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Sales */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Recent Sales</h3>
            <p className="card-description">Latest transactions from your POS system</p>
          </div>
          <div className="card-content">
            <div className="space-y-4">
              {[
                { id: 1, customer: 'John Doe', amount: '$125.50', status: 'Completed', time: '2 min ago' },
                { id: 2, customer: 'Jane Smith', amount: '$89.99', status: 'Completed', time: '5 min ago' },
                { id: 3, customer: 'Bob Johnson', amount: '$234.75', status: 'Pending', time: '10 min ago' },
                { id: 4, customer: 'Alice Brown', amount: '$67.25', status: 'Completed', time: '15 min ago' },
              ].map((sale) => (
                <div key={sale.id} className="flex items-center justify-between p-3 bg-secondary-50 rounded-lg">
                  <div>
                    <p className="font-medium text-secondary-900">{sale.customer}</p>
                    <p className="text-sm text-secondary-500">{sale.time}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold text-secondary-900">{sale.amount}</p>
                    <span className={`badge badge-${
                      sale.status === 'Completed' ? 'success' : 'warning'
                    }`}>
                      {sale.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Quick Actions</h3>
            <p className="card-description">Common tasks and shortcuts</p>
          </div>
          <div className="card-content">
            <div className="grid grid-cols-2 gap-4">
              {[
                { name: 'New Sale', icon: ShoppingCart, href: '/pos', color: 'primary' },
                { name: 'Add Product', icon: Package, href: '/products', color: 'success' },
                { name: 'View Inventory', icon: Package, href: '/inventory', color: 'warning' },
                { name: 'Generate Report', icon: TrendingUp, href: '/reports', color: 'secondary' },
              ].map((action) => (
                <button
                  key={action.name}
                  className="flex flex-col items-center p-4 border border-secondary-200 rounded-lg hover:bg-secondary-50 transition-colors"
                >
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center bg-${action.color}-100 mb-2`}>
                    <action.icon className={`w-5 h-5 text-${action.color}-600`} />
                  </div>
                  <span className="text-sm font-medium text-secondary-900">{action.name}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* System Status */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">System Status</h3>
          <p className="card-description">Current system health and performance</p>
        </div>
        <div className="card-content">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-16 h-16 bg-success-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <TrendingUp className="w-8 h-8 text-success-600" />
              </div>
              <h4 className="font-semibold text-secondary-900">Database</h4>
              <p className="text-sm text-success-600">Healthy</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-success-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <Building2 className="w-8 h-8 text-success-600" />
              </div>
              <h4 className="font-semibold text-secondary-900">API</h4>
              <p className="text-sm text-success-600">Online</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-warning-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <Package className="w-8 h-8 text-warning-600" />
              </div>
              <h4 className="font-semibold text-secondary-900">Modules</h4>
              <p className="text-sm text-warning-600">Loading</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}