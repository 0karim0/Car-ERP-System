import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { 
  Users, 
  Car, 
  Wrench, 
  Package, 
  DollarSign, 
  AlertTriangle,
  TrendingUp,
  Clock,
  CheckCircle
} from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuth();

  // Mock data - in a real app, this would come from API calls
  const stats = [
    {
      name: 'Total Customers',
      value: '1,247',
      change: '+12%',
      changeType: 'increase',
      icon: Users,
      color: 'bg-blue-500'
    },
    {
      name: 'Active Vehicles',
      value: '892',
      change: '+8%',
      changeType: 'increase',
      icon: Car,
      color: 'bg-green-500'
    },
    {
      name: 'Pending Job Orders',
      value: '23',
      change: '-5%',
      changeType: 'decrease',
      icon: Wrench,
      color: 'bg-yellow-500'
    },
    {
      name: 'Low Stock Items',
      value: '7',
      change: '+2%',
      changeType: 'increase',
      icon: Package,
      color: 'bg-red-500'
    },
    {
      name: 'Monthly Revenue',
      value: '$45,230',
      change: '+15%',
      changeType: 'increase',
      icon: DollarSign,
      color: 'bg-purple-500'
    },
    {
      name: 'Completed Jobs',
      value: '156',
      change: '+22%',
      changeType: 'increase',
      icon: CheckCircle,
      color: 'bg-indigo-500'
    }
  ];

  const recentActivities = [
    {
      id: 1,
      type: 'job_order',
      message: 'New job order #JO2024120001 created for John Doe',
      time: '2 minutes ago',
      icon: Wrench,
      color: 'text-blue-500'
    },
    {
      id: 2,
      type: 'payment',
      message: 'Payment of $450 received for Invoice #INV2024120005',
      time: '15 minutes ago',
      icon: DollarSign,
      color: 'text-green-500'
    },
    {
      id: 3,
      type: 'inventory',
      message: 'Stock alert: Brake pads running low (5 remaining)',
      time: '1 hour ago',
      icon: AlertTriangle,
      color: 'text-red-500'
    },
    {
      id: 4,
      type: 'customer',
      message: 'New customer Sarah Wilson registered',
      time: '2 hours ago',
      icon: Users,
      color: 'text-blue-500'
    },
    {
      id: 5,
      type: 'job_order',
      message: 'Job order #JO2024120002 marked as completed',
      time: '3 hours ago',
      icon: CheckCircle,
      color: 'text-green-500'
    }
  ];

  const quickActions = [
    {
      name: 'Create Job Order',
      href: '/job-orders',
      icon: Wrench,
      color: 'bg-blue-500 hover:bg-blue-600'
    },
    {
      name: 'Add Customer',
      href: '/customers',
      icon: Users,
      color: 'bg-green-500 hover:bg-green-600'
    },
    {
      name: 'Check Inventory',
      href: '/inventory/parts',
      icon: Package,
      color: 'bg-yellow-500 hover:bg-yellow-600'
    },
    {
      name: 'Generate Invoice',
      href: '/accounting/invoices',
      icon: DollarSign,
      color: 'bg-purple-500 hover:bg-purple-600'
    }
  ];

  const getRoleBasedActions = () => {
    if (!user) return quickActions;
    
    switch (user.role) {
      case 'receptionist':
        return quickActions.filter(action => 
          ['Create Job Order', 'Add Customer'].includes(action.name)
        );
      case 'technician':
        return quickActions.filter(action => 
          ['Create Job Order', 'Check Inventory'].includes(action.name)
        );
      case 'inventory_manager':
        return quickActions.filter(action => 
          ['Check Inventory'].includes(action.name)
        );
      case 'accountant':
        return quickActions.filter(action => 
          ['Generate Invoice'].includes(action.name)
        );
      default:
        return quickActions;
    }
  };

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              Welcome back, {user?.first_name || 'User'}!
            </h1>
            <p className="text-gray-600 mt-1">
              Here's what's happening with your auto service center today.
            </p>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-500">Today</p>
            <p className="text-lg font-semibold text-gray-900">
              {new Date().toLocaleDateString('en-US', { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
              })}
            </p>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {stats.map((stat) => (
          <div key={stat.name} className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                <div className="flex items-center mt-2">
                  <TrendingUp className={`h-4 w-4 mr-1 ${
                    stat.changeType === 'increase' ? 'text-green-500' : 'text-red-500'
                  }`} />
                  <span className={`text-sm font-medium ${
                    stat.changeType === 'increase' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {stat.change}
                  </span>
                  <span className="text-sm text-gray-500 ml-1">from last month</span>
                </div>
              </div>
              <div className={`p-3 rounded-full ${stat.color}`}>
                <stat.icon className="h-6 w-6 text-white" />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-2 gap-4">
            {getRoleBasedActions().map((action) => (
              <a
                key={action.name}
                href={action.href}
                className={`${action.color} text-white rounded-lg p-4 flex flex-col items-center justify-center text-center transition-colors duration-200`}
              >
                <action.icon className="h-8 w-8 mb-2" />
                <span className="font-medium">{action.name}</span>
              </a>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h2>
          <div className="space-y-4">
            {recentActivities.map((activity) => (
              <div key={activity.id} className="flex items-start space-x-3">
                <div className={`p-2 rounded-full bg-gray-100`}>
                  <activity.icon className={`h-4 w-4 ${activity.color}`} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-900">{activity.message}</p>
                  <p className="text-xs text-gray-500 mt-1">{activity.time}</p>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-4 pt-4 border-t border-gray-200">
            <a
              href="#"
              className="text-sm font-medium text-primary-600 hover:text-primary-500"
            >
              View all activity →
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
