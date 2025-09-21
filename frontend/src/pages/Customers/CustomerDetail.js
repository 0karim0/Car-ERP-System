import React from 'react';
import { useParams } from 'react-router-dom';
import { ArrowLeft, Edit, Phone, Mail, MapPin, Calendar, Car, Wrench } from 'lucide-react';

const CustomerDetail = () => {
  const { id } = useParams();

  // Mock data - in a real app, this would come from API
  const customer = {
    id: parseInt(id),
    first_name: 'John',
    last_name: 'Doe',
    email: 'john.doe@email.com',
    phone: '+1-555-0123',
    alternate_phone: '+1-555-0124',
    address_line1: '123 Main Street',
    address_line2: 'Apt 4B',
    city: 'New York',
    state: 'NY',
    postal_code: '10001',
    country: 'USA',
    company_name: 'Doe Enterprises',
    tax_id: '12-3456789',
    notes: 'Preferred customer, always pays on time.',
    preferred_contact_method: 'phone',
    is_active: true,
    created_at: '2024-01-15T10:30:00Z',
    vehicles: [
      {
        id: 1,
        make: 'Toyota',
        model: 'Camry',
        year: 2020,
        license_plate: 'ABC-123',
        vin: '1HGBH41JXMN109186',
        color: 'Silver',
        fuel_type: 'gasoline',
        transmission: 'automatic',
        mileage: 45000,
        is_active: true
      },
      {
        id: 2,
        make: 'Honda',
        model: 'Civic',
        year: 2018,
        license_plate: 'XYZ-789',
        vin: '2HGBH41JXMN109187',
        color: 'Blue',
        fuel_type: 'gasoline',
        transmission: 'manual',
        mileage: 62000,
        is_active: true
      }
    ],
    job_orders: [
      {
        id: 1,
        job_number: 'JO2024120001',
        service_type: 'Oil Change',
        status: 'completed',
        received_date: '2024-01-20T09:00:00Z',
        actual_completion: '2024-01-20T11:30:00Z',
        total_amount: 85.50
      },
      {
        id: 2,
        job_number: 'JO2024120002',
        service_type: 'Brake Service',
        status: 'in_progress',
        received_date: '2024-01-25T08:00:00Z',
        estimated_completion: '2024-01-26T17:00:00Z',
        estimated_cost: 450.00
      }
    ],
    appointments: [
      {
        id: 1,
        appointment_date: '2024-02-01T10:00:00Z',
        service_type: 'Regular Maintenance',
        status: 'scheduled',
        description: '30,000 mile service'
      }
    ]
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'in_progress':
        return 'bg-yellow-100 text-yellow-800';
      case 'scheduled':
        return 'bg-blue-100 text-blue-800';
      case 'cancelled':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button className="text-gray-600 hover:text-gray-900">
            <ArrowLeft className="h-6 w-6" />
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              {customer.first_name} {customer.last_name}
            </h1>
            <p className="text-gray-600">Customer Details</p>
          </div>
        </div>
        <button className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 flex items-center space-x-2">
          <Edit className="h-5 w-5" />
          <span>Edit Customer</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Customer Information */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Customer Information</h2>
            
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <Mail className="h-5 w-5 text-gray-400" />
                <div>
                  <p className="text-sm font-medium text-gray-900">{customer.email}</p>
                  <p className="text-xs text-gray-500">Email</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <Phone className="h-5 w-5 text-gray-400" />
                <div>
                  <p className="text-sm font-medium text-gray-900">{customer.phone}</p>
                  <p className="text-xs text-gray-500">Primary Phone</p>
                </div>
              </div>
              
              {customer.alternate_phone && (
                <div className="flex items-center space-x-3">
                  <Phone className="h-5 w-5 text-gray-400" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">{customer.alternate_phone}</p>
                    <p className="text-xs text-gray-500">Alternate Phone</p>
                  </div>
                </div>
              )}
              
              <div className="flex items-center space-x-3">
                <MapPin className="h-5 w-5 text-gray-400" />
                <div>
                  <p className="text-sm font-medium text-gray-900">
                    {customer.address_line1}
                    {customer.address_line2 && `, ${customer.address_line2}`}
                  </p>
                  <p className="text-sm text-gray-900">
                    {customer.city}, {customer.state} {customer.postal_code}
                  </p>
                  <p className="text-xs text-gray-500">Address</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <Calendar className="h-5 w-5 text-gray-400" />
                <div>
                  <p className="text-sm font-medium text-gray-900">
                    {new Date(customer.created_at).toLocaleDateString()}
                  </p>
                  <p className="text-xs text-gray-500">Customer Since</p>
                </div>
              </div>
            </div>

            {customer.company_name && (
              <div className="mt-6 pt-6 border-t border-gray-200">
                <h3 className="text-sm font-medium text-gray-900 mb-2">Business Information</h3>
                <p className="text-sm text-gray-900">{customer.company_name}</p>
                {customer.tax_id && (
                  <p className="text-xs text-gray-500">Tax ID: {customer.tax_id}</p>
                )}
              </div>
            )}

            {customer.notes && (
              <div className="mt-6 pt-6 border-t border-gray-200">
                <h3 className="text-sm font-medium text-gray-900 mb-2">Notes</h3>
                <p className="text-sm text-gray-900">{customer.notes}</p>
              </div>
            )}

            <div className="mt-6 pt-6 border-t border-gray-200">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-900">Status</span>
                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                  customer.is_active 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  {customer.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Vehicles and Activity */}
        <div className="lg:col-span-2 space-y-6">
          {/* Vehicles */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900 flex items-center">
                <Car className="h-5 w-5 mr-2" />
                Vehicles ({customer.vehicles.length})
              </h2>
              <button className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                Add Vehicle
              </button>
            </div>
            
            <div className="space-y-4">
              {customer.vehicles.map((vehicle) => (
                <div key={vehicle.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-medium text-gray-900">
                        {vehicle.year} {vehicle.make} {vehicle.model}
                      </h3>
                      <p className="text-sm text-gray-500">
                        {vehicle.license_plate} • {vehicle.vin}
                      </p>
                      <p className="text-sm text-gray-500">
                        {vehicle.color} • {vehicle.fuel_type} • {vehicle.transmission}
                      </p>
                      <p className="text-sm text-gray-500">
                        Mileage: {vehicle.mileage.toLocaleString()} miles
                      </p>
                    </div>
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      vehicle.is_active 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {vehicle.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Recent Job Orders */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900 flex items-center">
                <Wrench className="h-5 w-5 mr-2" />
                Recent Job Orders
              </h2>
              <button className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                View All
              </button>
            </div>
            
            <div className="space-y-4">
              {customer.job_orders.map((job) => (
                <div key={job.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-medium text-gray-900">
                        {job.job_number} - {job.service_type}
                      </h3>
                      <p className="text-sm text-gray-500">
                        Received: {new Date(job.received_date).toLocaleDateString()}
                      </p>
                      {job.actual_completion && (
                        <p className="text-sm text-gray-500">
                          Completed: {new Date(job.actual_completion).toLocaleDateString()}
                        </p>
                      )}
                      {job.estimated_completion && !job.actual_completion && (
                        <p className="text-sm text-gray-500">
                          Estimated: {new Date(job.estimated_completion).toLocaleDateString()}
                        </p>
                      )}
                    </div>
                    <div className="text-right">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(job.status)}`}>
                        {job.status.replace('_', ' ')}
                      </span>
                      <p className="text-sm font-medium text-gray-900 mt-1">
                        ${job.total_amount || job.estimated_cost}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Upcoming Appointments */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Upcoming Appointments</h2>
            
            <div className="space-y-4">
              {customer.appointments.map((appointment) => (
                <div key={appointment.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-medium text-gray-900">
                        {appointment.service_type}
                      </h3>
                      <p className="text-sm text-gray-500">
                        {new Date(appointment.appointment_date).toLocaleString()}
                      </p>
                      {appointment.description && (
                        <p className="text-sm text-gray-500">
                          {appointment.description}
                        </p>
                      )}
                    </div>
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(appointment.status)}`}>
                      {appointment.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CustomerDetail;
