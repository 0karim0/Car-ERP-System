import React from 'react';
import { Users, Plus } from 'lucide-react';

const Suppliers = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Suppliers</h1>
          <p className="text-gray-600">Manage supplier information</p>
        </div>
        <button className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 flex items-center space-x-2">
          <Plus className="h-5 w-5" />
          <span>Add Supplier</span>
        </button>
      </div>

      <div className="bg-white rounded-lg shadow p-8 text-center">
        <Users className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Supplier Management</h2>
        <p className="text-gray-600">This page will allow you to manage supplier information, contact details, and business relationships.</p>
      </div>
    </div>
  );
};

export default Suppliers;
