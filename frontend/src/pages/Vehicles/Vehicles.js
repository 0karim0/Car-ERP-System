import React from 'react';
import { Car, Plus, Search, Filter } from 'lucide-react';

const Vehicles = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Vehicles</h1>
          <p className="text-gray-600">Manage vehicle database</p>
        </div>
        <button className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 flex items-center space-x-2">
          <Plus className="h-5 w-5" />
          <span>Add Vehicle</span>
        </button>
      </div>

      <div className="bg-white rounded-lg shadow p-8 text-center">
        <Car className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Vehicle Management</h2>
        <p className="text-gray-600 mb-6">This module will allow you to manage vehicle information, track service history, and maintain vehicle records.</p>
        <div className="text-sm text-gray-500">
          Features coming soon:
          <ul className="mt-2 space-y-1">
            <li>• Vehicle registration and details</li>
            <li>• Service history tracking</li>
            <li>• Document management</li>
            <li>• Photo documentation</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Vehicles;
