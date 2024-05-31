const backendUrl = process.env.REACT_APP_BACKEND_URL;

export async function registerUser(username, password) {
  const response = await fetch(`${backendUrl}/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password })
  });

  if (!response.ok) {
    throw new Error('Registration failed');
  }

  return await response.text();
}

export async function loginUser(username, password) {
  const response = await fetch(`${backendUrl}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password })
  });

  if (!response.ok) {
    throw new Error('Login failed');
  }

  return await response.text();
}
