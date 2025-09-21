import React from 'react';
import { Package } from 'lucide-react';

const Inventory = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Inventory</h1>
        <p className="text-gray-600">Manage inventory and spare parts</p>
      </div>

      <div className="bg-white rounded-lg shadow p-8 text-center">
        <Package className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Inventory Management</h2>
        <p className="text-gray-600 mb-6">This module will allow you to manage parts inventory, track stock levels, and manage suppliers.</p>
        <div className="text-sm text-gray-500">
          Features coming soon:
          <ul className="mt-2 space-y-1">
            <li>• Parts and inventory management</li>
            <li>• Stock level tracking</li>
            <li>• Supplier management</li>
            <li>• Purchase order processing</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Inventory;
