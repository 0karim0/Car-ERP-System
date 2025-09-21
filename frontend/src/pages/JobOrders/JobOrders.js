import React from 'react';
import { Wrench, Plus } from 'lucide-react';

const JobOrders = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Job Orders</h1>
          <p className="text-gray-600">Manage work orders and track progress</p>
        </div>
        <button className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 flex items-center space-x-2">
          <Plus className="h-5 w-5" />
          <span>Create Job Order</span>
        </button>
      </div>

      <div className="bg-white rounded-lg shadow p-8 text-center">
        <Wrench className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Job Order Management</h2>
        <p className="text-gray-600 mb-6">This module will allow you to create, track, and manage job orders throughout the repair process.</p>
        <div className="text-sm text-gray-500">
          Features coming soon:
          <ul className="mt-2 space-y-1">
            <li>• Create and assign job orders</li>
            <li>• Track work progress and status</li>
            <li>• Manage parts and labor</li>
            <li>• Technician time tracking</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default JobOrders;
