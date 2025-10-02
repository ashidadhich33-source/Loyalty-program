import { useState } from 'react';
import { User, Mail, Phone, MapPin, Calendar, Edit, Save, Camera } from 'lucide-react';

export default function Profile() {
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    firstName: 'John',
    lastName: 'Doe',
    email: 'john@example.com',
    phone: '+1 (555) 123-4567',
    address: '123 Main St, City, State 12345',
    role: 'Admin',
    company: 'Example Company',
    joinDate: '2024-01-01',
  });

  const handleSave = () => {
    // Save logic here
    setIsEditing(false);
  };

  const handleCancel = () => {
    setIsEditing(false);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-secondary-900">Profile</h1>
          <p className="text-secondary-600 mt-1">Manage your personal information</p>
        </div>
        <div className="flex items-center gap-3">
          {isEditing ? (
            <>
              <button onClick={handleCancel} className="btn btn-outline">
                Cancel
              </button>
              <button onClick={handleSave} className="btn btn-primary">
                <Save className="w-4 h-4 mr-2" />
                Save Changes
              </button>
            </>
          ) : (
            <button onClick={() => setIsEditing(true)} className="btn btn-primary">
              <Edit className="w-4 h-4 mr-2" />
              Edit Profile
            </button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Profile Card */}
        <div className="lg:col-span-1">
          <div className="card">
            <div className="card-content text-center">
              <div className="relative inline-block mb-4">
                <div className="w-24 h-24 bg-primary-100 rounded-full flex items-center justify-center mx-auto">
                  <User className="w-12 h-12 text-primary-600" />
                </div>
                {isEditing && (
                  <button className="absolute bottom-0 right-0 w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center hover:bg-primary-700">
                    <Camera className="w-4 h-4" />
                  </button>
                )}
              </div>
              <h2 className="text-xl font-bold text-secondary-900 mb-1">
                {formData.firstName} {formData.lastName}
              </h2>
              <p className="text-secondary-600 mb-2">{formData.email}</p>
              <span className="badge badge-primary">{formData.role}</span>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="card mt-6">
            <div className="card-header">
              <h3 className="card-title">Quick Stats</h3>
            </div>
            <div className="card-content">
              <div className="space-y-4">
                <div className="flex justify-between">
                  <span className="text-secondary-600">Member Since</span>
                  <span className="font-medium">{formData.joinDate}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-secondary-600">Company</span>
                  <span className="font-medium">{formData.company}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-secondary-600">Last Login</span>
                  <span className="font-medium">2 hours ago</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Profile Details */}
        <div className="lg:col-span-2">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Personal Information</h3>
              <p className="card-description">Update your personal details</p>
            </div>
            <div className="card-content space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-secondary-700 mb-2 block">First Name</label>
                  <input
                    type="text"
                    value={formData.firstName}
                    onChange={(e) => setFormData({ ...formData, firstName: e.target.value })}
                    disabled={!isEditing}
                    className="input"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-secondary-700 mb-2 block">Last Name</label>
                  <input
                    type="text"
                    value={formData.lastName}
                    onChange={(e) => setFormData({ ...formData, lastName: e.target.value })}
                    disabled={!isEditing}
                    className="input"
                  />
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-secondary-700 mb-2 block">Email Address</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-secondary-400" />
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    disabled={!isEditing}
                    className="input pl-10"
                  />
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-secondary-700 mb-2 block">Phone Number</label>
                <div className="relative">
                  <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-secondary-400" />
                  <input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    disabled={!isEditing}
                    className="input pl-10"
                  />
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-secondary-700 mb-2 block">Address</label>
                <div className="relative">
                  <MapPin className="absolute left-3 top-3 w-4 h-4 text-secondary-400" />
                  <textarea
                    value={formData.address}
                    onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                    disabled={!isEditing}
                    className="input pl-10"
                    rows={3}
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-secondary-700 mb-2 block">Role</label>
                  <input
                    type="text"
                    value={formData.role}
                    disabled
                    className="input bg-secondary-50"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-secondary-700 mb-2 block">Join Date</label>
                  <div className="relative">
                    <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-secondary-400" />
                    <input
                      type="text"
                      value={formData.joinDate}
                      disabled
                      className="input pl-10 bg-secondary-50"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Security Settings */}
          <div className="card mt-6">
            <div className="card-header">
              <h3 className="card-title">Security</h3>
              <p className="card-description">Manage your account security</p>
            </div>
            <div className="card-content">
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-secondary-50 rounded-lg">
                  <div>
                    <h4 className="font-medium text-secondary-900">Password</h4>
                    <p className="text-sm text-secondary-600">Last updated 3 months ago</p>
                  </div>
                  <button className="btn btn-outline btn-sm">
                    Change Password
                  </button>
                </div>
                <div className="flex items-center justify-between p-4 bg-secondary-50 rounded-lg">
                  <div>
                    <h4 className="font-medium text-secondary-900">Two-Factor Authentication</h4>
                    <p className="text-sm text-secondary-600">Add an extra layer of security</p>
                  </div>
                  <button className="btn btn-outline btn-sm">
                    Enable 2FA
                  </button>
                </div>
                <div className="flex items-center justify-between p-4 bg-secondary-50 rounded-lg">
                  <div>
                    <h4 className="font-medium text-secondary-900">Login Sessions</h4>
                    <p className="text-sm text-secondary-600">Manage your active sessions</p>
                  </div>
                  <button className="btn btn-outline btn-sm">
                    View Sessions
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}