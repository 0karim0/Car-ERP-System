import React from 'react';

const VehicleDetail = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Vehicle Details</h1>
        <p className="text-gray-600">Detailed vehicle information and service history</p>
      </div>
      
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <div className="text-gray-400 text-4xl mb-4">🚗</div>
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Vehicle Details Page</h2>
        <p className="text-gray-600">This page will show detailed vehicle information, service history, and related job orders.</p>
      </div>
    </div>
  );
};

export default VehicleDetail;
