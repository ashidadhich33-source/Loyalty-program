import { useState } from 'react';
import { Settings as SettingsIcon, Save, User, Building2, Shield, Bell, Palette } from 'lucide-react';

export default function Settings() {
  const [activeTab, setActiveTab] = useState('general');

  const tabs = [
    { id: 'general', name: 'General', icon: SettingsIcon },
    { id: 'profile', name: 'Profile', icon: User },
    { id: 'company', name: 'Company', icon: Building2 },
    { id: 'security', name: 'Security', icon: Shield },
    { id: 'notifications', name: 'Notifications', icon: Bell },
    { id: 'appearance', name: 'Appearance', icon: Palette },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-secondary-900">Settings</h1>
          <p className="text-secondary-600 mt-1">Manage your account and system preferences</p>
        </div>
      </div>

      <div className="flex gap-6">
        {/* Sidebar */}
        <div className="w-64">
          <div className="card">
            <div className="card-content p-0">
              <nav className="space-y-1">
                {tabs.map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center gap-3 px-4 py-3 text-left text-sm font-medium rounded-lg transition-colors ${
                      activeTab === tab.id
                        ? 'bg-primary-100 text-primary-900'
                        : 'text-secondary-600 hover:bg-secondary-100 hover:text-secondary-900'
                    }`}
                  >
                    <tab.icon className="w-4 h-4" />
                    {tab.name}
                  </button>
                ))}
              </nav>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1">
          {activeTab === 'general' && (
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">General Settings</h3>
                <p className="card-description">Basic system configuration</p>
              </div>
              <div className="card-content space-y-6">
                <div>
                  <label className="text-sm font-medium text-secondary-700 mb-2 block">System Name</label>
                  <input
                    type="text"
                    defaultValue="ERP System"
                    className="input"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-secondary-700 mb-2 block">Default Language</label>
                  <select className="input">
                    <option value="en">English</option>
                    <option value="es">Spanish</option>
                    <option value="fr">French</option>
                  </select>
                </div>
                <div>
                  <label className="text-sm font-medium text-secondary-700 mb-2 block">Default Currency</label>
                  <select className="input">
                    <option value="USD">USD - US Dollar</option>
                    <option value="EUR">EUR - Euro</option>
                    <option value="GBP">GBP - British Pound</option>
                  </select>
                </div>
                <div>
                  <label className="text-sm font-medium text-secondary-700 mb-2 block">Timezone</label>
                  <select className="input">
                    <option value="UTC">UTC</option>
                    <option value="America/New_York">Eastern Time</option>
                    <option value="America/Los_Angeles">Pacific Time</option>
                  </select>
                </div>
                <div className="flex items-center gap-3">
                  <button className="btn btn-primary">
                    <Save className="w-4 h-4 mr-2" />
                    Save Changes
                  </button>
                  <button className="btn btn-outline">
                    Reset
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'profile' && (
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">Profile Settings</h3>
                <p className="card-description">Manage your personal information</p>
              </div>
              <div className="card-content space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-secondary-700 mb-2 block">First Name</label>
                    <input
                      type="text"
                      defaultValue="John"
                      className="input"
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium text-secondary-700 mb-2 block">Last Name</label>
                    <input
                      type="text"
                      defaultValue="Doe"
                      className="input"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-sm font-medium text-secondary-700 mb-2 block">Email</label>
                  <input
                    type="email"
                    defaultValue="john@example.com"
                    className="input"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-secondary-700 mb-2 block">Phone</label>
                  <input
                    type="tel"
                    defaultValue="+1 (555) 123-4567"
                    className="input"
                  />
                </div>
                <div className="flex items-center gap-3">
                  <button className="btn btn-primary">
                    <Save className="w-4 h-4 mr-2" />
                    Save Changes
                  </button>
                  <button className="btn btn-outline">
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'company' && (
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">Company Settings</h3>
                <p className="card-description">Manage company information and preferences</p>
              </div>
              <div className="card-content space-y-6">
                <div>
                  <label className="text-sm font-medium text-secondary-700 mb-2 block">Company Name</label>
                  <input
                    type="text"
                    defaultValue="Example Company"
                    className="input"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-secondary-700 mb-2 block">Address</label>
                  <textarea
                    defaultValue="123 Main St, City, State 12345"
                    className="input"
                    rows={3}
                  />
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-secondary-700 mb-2 block">Phone</label>
                    <input
                      type="tel"
                      defaultValue="+1 (555) 123-4567"
                      className="input"
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium text-secondary-700 mb-2 block">Email</label>
                    <input
                      type="email"
                      defaultValue="info@example.com"
                      className="input"
                    />
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <button className="btn btn-primary">
                    <Save className="w-4 h-4 mr-2" />
                    Save Changes
                  </button>
                  <button className="btn btn-outline">
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'security' && (
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">Security Settings</h3>
                <p className="card-description">Manage your account security</p>
              </div>
              <div className="card-content space-y-6">
                <div>
                  <label className="text-sm font-medium text-secondary-700 mb-2 block">Current Password</label>
                  <input
                    type="password"
                    className="input"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-secondary-700 mb-2 block">New Password</label>
                  <input
                    type="password"
                    className="input"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-secondary-700 mb-2 block">Confirm New Password</label>
                  <input
                    type="password"
                    className="input"
                  />
                </div>
                <div className="flex items-center gap-3">
                  <button className="btn btn-primary">
                    <Save className="w-4 h-4 mr-2" />
                    Update Password
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'notifications' && (
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">Notification Settings</h3>
                <p className="card-description">Manage your notification preferences</p>
              </div>
              <div className="card-content space-y-6">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-secondary-900">Email Notifications</h4>
                      <p className="text-sm text-secondary-600">Receive notifications via email</p>
                    </div>
                    <input type="checkbox" defaultChecked className="rounded" />
                  </div>
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-secondary-900">Push Notifications</h4>
                      <p className="text-sm text-secondary-600">Receive push notifications</p>
                    </div>
                    <input type="checkbox" defaultChecked className="rounded" />
                  </div>
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-secondary-900">SMS Notifications</h4>
                      <p className="text-sm text-secondary-600">Receive SMS notifications</p>
                    </div>
                    <input type="checkbox" className="rounded" />
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <button className="btn btn-primary">
                    <Save className="w-4 h-4 mr-2" />
                    Save Changes
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'appearance' && (
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">Appearance Settings</h3>
                <p className="card-description">Customize the look and feel</p>
              </div>
              <div className="card-content space-y-6">
                <div>
                  <label className="text-sm font-medium text-secondary-700 mb-2 block">Theme</label>
                  <select className="input">
                    <option value="light">Light</option>
                    <option value="dark">Dark</option>
                    <option value="auto">Auto</option>
                  </select>
                </div>
                <div>
                  <label className="text-sm font-medium text-secondary-700 mb-2 block">Primary Color</label>
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-primary-600 rounded-full border-2 border-white shadow-lg"></div>
                    <div className="w-8 h-8 bg-blue-600 rounded-full border-2 border-white shadow-lg"></div>
                    <div className="w-8 h-8 bg-green-600 rounded-full border-2 border-white shadow-lg"></div>
                    <div className="w-8 h-8 bg-purple-600 rounded-full border-2 border-white shadow-lg"></div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <button className="btn btn-primary">
                    <Save className="w-4 h-4 mr-2" />
                    Save Changes
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}