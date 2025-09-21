import React from 'react';
import { ShoppingCart, Plus } from 'lucide-react';

const PurchaseOrders = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Purchase Orders</h1>
          <p className="text-gray-600">Manage purchase orders and procurement</p>
        </div>
        <button className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 flex items-center space-x-2">
          <Plus className="h-5 w-5" />
          <span>Create PO</span>
        </button>
      </div>

      <div className="bg-white rounded-lg shadow p-8 text-center">
        <ShoppingCart className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Purchase Order Management</h2>
        <p className="text-gray-600">This page will allow you to create, track, and manage purchase orders with suppliers.</p>
      </div>
    </div>
  );
};

export default PurchaseOrders;
