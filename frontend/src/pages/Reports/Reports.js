import React from 'react';
import { BarChart3, Download, Filter } from 'lucide-react';

const Reports = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Reports</h1>
          <p className="text-gray-600">Generate and view business reports</p>
        </div>
        <div className="flex space-x-3">
          <button className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 flex items-center space-x-2">
            <Filter className="h-5 w-5" />
            <span>Filters</span>
          </button>
          <button className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 flex items-center space-x-2">
            <Download className="h-5 w-5" />
            <span>Export</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Sales Report</h3>
            <BarChart3 className="h-6 w-6 text-primary-600" />
          </div>
          <p className="text-gray-600 mb-4">Generate comprehensive sales reports with date filtering and analysis.</p>
          <button className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700">
            Generate Report
          </button>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Inventory Report</h3>
            <BarChart3 className="h-6 w-6 text-primary-600" />
          </div>
          <p className="text-gray-600 mb-4">Track inventory levels, stock movements, and low stock alerts.</p>
          <button className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700">
            Generate Report
          </button>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Customer Report</h3>
            <BarChart3 className="h-6 w-6 text-primary-600" />
          </div>
          <p className="text-gray-600 mb-4">Analyze customer data, loyalty, and service history.</p>
          <button className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700">
            Generate Report
          </button>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Technician Performance</h3>
            <BarChart3 className="h-6 w-6 text-primary-600" />
          </div>
          <p className="text-gray-600 mb-4">Track technician productivity and work performance metrics.</p>
          <button className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700">
            Generate Report
          </button>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Financial Report</h3>
            <BarChart3 className="h-6 w-6 text-primary-600" />
          </div>
          <p className="text-gray-600 mb-4">Comprehensive financial analysis and profit & loss statements.</p>
          <button className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700">
            Generate Report
          </button>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Custom Report</h3>
            <BarChart3 className="h-6 w-6 text-primary-600" />
          </div>
          <p className="text-gray-600 mb-4">Create custom reports with your own parameters and filters.</p>
          <button className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700">
            Create Report
          </button>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Reports</h2>
        <div className="text-center py-8">
          <BarChart3 className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No reports generated yet. Create your first report to get started.</p>
        </div>
      </div>
    </div>
  );
};

export default Reports;
