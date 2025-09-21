import React from 'react';

const JobOrderDetail = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Job Order Details</h1>
        <p className="text-gray-600">Detailed job order information and progress tracking</p>
      </div>
      
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <div className="text-gray-400 text-4xl mb-4">🔧</div>
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Job Order Details Page</h2>
        <p className="text-gray-600">This page will show detailed job order information, work progress, parts used, and technician time.</p>
      </div>
    </div>
  );
};

export default JobOrderDetail;
