import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout/Layout';
import Login from './pages/Auth/Login';
import Dashboard from './pages/Dashboard/Dashboard';
import Customers from './pages/Customers/Customers';
import CustomerDetail from './pages/Customers/CustomerDetail';
import Vehicles from './pages/Vehicles/Vehicles';
import VehicleDetail from './pages/Vehicles/VehicleDetail';
import JobOrders from './pages/JobOrders/JobOrders';
import JobOrderDetail from './pages/JobOrders/JobOrderDetail';
import Inventory from './pages/Inventory/Inventory';
import Parts from './pages/Inventory/Parts';
import Suppliers from './pages/Inventory/Suppliers';
import PurchaseOrders from './pages/Inventory/PurchaseOrders';
import Invoices from './pages/Accounting/Invoices';
import Payments from './pages/Accounting/Payments';
import Reports from './pages/Reports/Reports';
import ProtectedRoute from './components/Auth/ProtectedRoute';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router>
          <div className="App">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
                <Route index element={<Navigate to="/dashboard" replace />} />
                <Route path="dashboard" element={<Dashboard />} />
                
                {/* Customer Management Routes */}
                <Route path="customers" element={<Customers />} />
                <Route path="customers/:id" element={<CustomerDetail />} />
                
                {/* Vehicle Management Routes */}
                <Route path="vehicles" element={<Vehicles />} />
                <Route path="vehicles/:id" element={<VehicleDetail />} />
                
                {/* Job Orders Routes */}
                <Route path="job-orders" element={<JobOrders />} />
                <Route path="job-orders/:id" element={<JobOrderDetail />} />
                
                {/* Inventory Management Routes */}
                <Route path="inventory" element={<Inventory />} />
                <Route path="inventory/parts" element={<Parts />} />
                <Route path="inventory/suppliers" element={<Suppliers />} />
                <Route path="inventory/purchase-orders" element={<PurchaseOrders />} />
                
                {/* Accounting Routes */}
                <Route path="accounting/invoices" element={<Invoices />} />
                <Route path="accounting/payments" element={<Payments />} />
                
                {/* Reports Routes */}
                <Route path="reports" element={<Reports />} />
              </Route>
            </Routes>
            <Toaster
              position="top-right"
              toastOptions={{
                duration: 4000,
                style: {
                  background: '#363636',
                  color: '#fff',
                },
                success: {
                  duration: 3000,
                  iconTheme: {
                    primary: '#4ade80',
                    secondary: '#fff',
                  },
                },
                error: {
                  duration: 5000,
                  iconTheme: {
                    primary: '#ef4444',
                    secondary: '#fff',
                  },
                },
              }}
            />
          </div>
        </Router>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
