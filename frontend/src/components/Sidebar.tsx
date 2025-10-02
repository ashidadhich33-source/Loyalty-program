import { NavLink } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import {
  LayoutDashboard,
  Users,
  Building2,
  Package,
  ShoppingCart,
  CreditCard,
  Warehouse,
  ShoppingBag,
  Calculator,
  BarChart3,
  Settings,
  User,
  LogOut,
  Menu,
  X,
} from 'lucide-react';
import { useState } from 'react';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Users', href: '/users', icon: Users, roles: ['admin', 'manager'] },
  { name: 'Companies', href: '/companies', icon: Building2, roles: ['admin', 'manager'] },
  { name: 'Products', href: '/products', icon: Package },
  { name: 'Sales', href: '/sales', icon: ShoppingCart },
  { name: 'POS', href: '/pos', icon: CreditCard },
  { name: 'Inventory', href: '/inventory', icon: Warehouse },
  { name: 'Purchase', href: '/purchase', icon: ShoppingBag },
  { name: 'Accounting', href: '/accounting', icon: Calculator },
  { name: 'Reports', href: '/reports', icon: BarChart3 },
];

const settings = [
  { name: 'Settings', href: '/settings', icon: Settings },
  { name: 'Profile', href: '/profile', icon: User },
];

export default function Sidebar() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
  };

  const canAccess = (roles?: string[]) => {
    if (!roles) return true;
    return user?.role && roles.includes(user.role);
  };

  const NavItem = ({ item }: { item: typeof navigation[0] }) => {
    if (!canAccess(item.roles)) return null;

    return (
      <NavLink
        to={item.href}
        className={({ isActive }) =>
          `nav-item ${isActive ? 'nav-item-active' : ''}`
        }
        onClick={() => setIsMobileMenuOpen(false)}
      >
        <item.icon className="w-5 h-5" />
        {item.name}
      </NavLink>
    );
  };

  return (
    <>
      {/* Mobile menu button */}
      <div className="lg:hidden fixed top-4 left-4 z-50">
        <button
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          className="btn btn-secondary btn-sm"
        >
          {isMobileMenuOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
        </button>
      </div>

      {/* Mobile overlay */}
      {isMobileMenuOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`sidebar ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'} fixed lg:static inset-y-0 left-0 z-50 transition-transform duration-300 ease-in-out`}>
        {/* Header */}
        <div className="sidebar-header">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <Building2 className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-secondary-900">ERP System</h1>
              <p className="text-xs text-secondary-500">Kids Clothing Retail</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <div className="sidebar-content">
          <nav className="space-y-1 px-3">
            {navigation.map((item) => (
              <NavItem key={item.name} item={item} />
            ))}
          </nav>

          {/* Settings Section */}
          <div className="nav-separator" />
          <div className="nav-group">Settings</div>
          <nav className="space-y-1 px-3">
            {settings.map((item) => (
              <NavLink
                key={item.name}
                to={item.href}
                className={({ isActive }) =>
                  `nav-item ${isActive ? 'nav-item-active' : ''}`
                }
                onClick={() => setIsMobileMenuOpen(false)}
              >
                <item.icon className="w-5 h-5" />
                {item.name}
              </NavLink>
            ))}
          </nav>
        </div>

        {/* Footer */}
        <div className="sidebar-footer">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-8 h-8 bg-secondary-100 rounded-full flex items-center justify-center">
              <User className="w-4 h-4 text-secondary-600" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-secondary-900 truncate">
                {user?.first_name} {user?.last_name}
              </p>
              <p className="text-xs text-secondary-500 truncate">
                {user?.email}
              </p>
            </div>
          </div>
          
          <button
            onClick={handleLogout}
            className="nav-item w-full text-left text-error-600 hover:bg-error-50 hover:text-error-700"
          >
            <LogOut className="w-5 h-5" />
            Sign Out
          </button>
        </div>
      </div>
    </>
  );
}