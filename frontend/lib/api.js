// API client utility to handle authenticated requests
// Attaches JWT token to API requests

class ApiClient {
  constructor(baseURL) {
    this.baseURL = baseURL || process.env.NEXT_PUBLIC_API_URL;
  }

  // Attach JWT token to request headers
  async attachToken() {
    // Get token from auth provider (to be implemented with your auth provider)
    // For now, this is a placeholder - the actual implementation will depend on your auth library
    if (typeof window !== 'undefined') {
      // Client-side code to get the token from your auth provider
      // This will vary depending on the auth library you're using
      const token = localStorage.getItem('auth-token'); // Example placeholder
      return token;
    }
    return null;
  }

  // Generic GET request
  async get(endpoint, options = {}) {
    const token = await this.attachToken();
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'GET',
      headers,
      ...options,
    });

    return this.handleResponse(response);
  }

  // Generic POST request
  async post(endpoint, data, options = {}) {
    const token = await this.attachToken();
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers,
      body: JSON.stringify(data),
      ...options,
    });

    return this.handleResponse(response);
  }

  // Generic PUT request
  async put(endpoint, data, options = {}) {
    const token = await this.attachToken();
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'PUT',
      headers,
      body: JSON.stringify(data),
      ...options,
    });

    return this.handleResponse(response);
  }

  // Generic DELETE request
  async delete(endpoint, options = {}) {
    const token = await this.attachToken();
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'DELETE',
      headers,
      ...options,
    });

    return this.handleResponse(response);
  }

  // Handle response and check for errors
  async handleResponse(response) {
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }
    return response.json();
  }
}

export default new ApiClient();