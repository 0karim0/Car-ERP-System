import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import {
  Home,
  Users,
  Car,
  Wrench,
  Package,
  DollarSign,
  BarChart3,
  X,
  ChevronRight,
  ShoppingCart,
  FileText,
  CreditCard
} from 'lucide-react';

const Sidebar = ({ isOpen, onClose }) => {
  const location = useLocation();
  const { user } = useAuth();

  const navigation = [
    {
      name: 'Dashboard',
      href: '/dashboard',
      icon: Home,
      roles: ['super_admin', 'receptionist', 'technician', 'inventory_manager', 'accountant']
    },
    {
      name: 'Customers',
      href: '/customers',
      icon: Users,
      roles: ['super_admin', 'receptionist']
    },
    {
      name: 'Vehicles',
      href: '/vehicles',
      icon: Car,
      roles: ['super_admin', 'receptionist']
    },
    {
      name: 'Job Orders',
      href: '/job-orders',
      icon: Wrench,
      roles: ['super_admin', 'receptionist', 'technician']
    },
    {
      name: 'Inventory',
      href: '/inventory',
      icon: Package,
      roles: ['super_admin', 'inventory_manager', 'technician'],
      children: [
        { name: 'Parts', href: '/inventory/parts', icon: Package },
        { name: 'Suppliers', href: '/inventory/suppliers', icon: Users },
        { name: 'Purchase Orders', href: '/inventory/purchase-orders', icon: ShoppingCart },
      ]
    },
    {
      name: 'Accounting',
      href: '/accounting',
      icon: DollarSign,
      roles: ['super_admin', 'accountant'],
      children: [
        { name: 'Invoices', href: '/accounting/invoices', icon: FileText },
        { name: 'Payments', href: '/accounting/payments', icon: CreditCard },
      ]
    },
    {
      name: 'Reports',
      href: '/reports',
      icon: BarChart3,
      roles: ['super_admin', 'accountant']
    },
  ];

  const filteredNavigation = navigation.filter(item => 
    user && item.roles.includes(user.role)
  );

  const NavItem = ({ item, level = 0 }) => {
    const isActive = location.pathname === item.href || 
      (item.children && item.children.some(child => location.pathname === child.href));
    
    const hasChildren = item.children && item.children.length > 0;
    const [isExpanded, setIsExpanded] = React.useState(isActive);

    if (hasChildren) {
      return (
        <div>
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className={`group flex items-center w-full px-3 py-2 text-sm font-medium rounded-md transition-colors duration-200 ${
              isActive
                ? 'bg-primary-100 text-primary-900'
                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
            }`}
            style={{ paddingLeft: `${level * 12 + 12}px` }}
          >
            <item.icon className="mr-3 h-5 w-5" />
            {item.name}
            <ChevronRight className={`ml-auto h-4 w-4 transition-transform duration-200 ${
              isExpanded ? 'rotate-90' : ''
            }`} />
          </button>
          
          {isExpanded && (
            <div className="mt-1 space-y-1">
              {item.children.map((child) => (
                <NavItem key={child.href} item={child} level={level + 1} />
              ))}
            </div>
          )}
        </div>
      );
    }

    return (
      <NavLink
        to={item.href}
        className={`group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors duration-200 ${
          location.pathname === item.href
            ? 'bg-primary-100 text-primary-900'
            : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
        }`}
        style={{ paddingLeft: `${level * 12 + 12}px` }}
        onClick={onClose}
      >
        <item.icon className="mr-3 h-5 w-5" />
        {item.name}
      </NavLink>
    );
  };

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 lg:hidden"
          onClick={onClose}
        >
          <div className="absolute inset-0 bg-gray-600 opacity-75" />
        </div>
      )}

      {/* Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex items-center justify-between h-16 px-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Navigation</h2>
          <button
            type="button"
            className="lg:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
            onClick={onClose}
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        <nav className="mt-5 px-3 space-y-1">
          {filteredNavigation.map((item) => (
            <NavItem key={item.name} item={item} />
          ))}
        </nav>
      </div>
    </>
  );
};

export default Sidebar;
