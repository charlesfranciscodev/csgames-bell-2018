import { authHeader } from "../helpers";

export const userService = {
  login,
  logout,
  register
}

function login(username, password) {
  const requestOptions = {
    method: "POST",
    headers: {
      "Content-type": "application/json"
    },
    body: JSON.stringify({
      username,
      password
    })
  }

  const url = `${process.env.REACT_APP_BELL_SERVICE_URL}/bell/authentication`;
  return fetch(url, requestOptions)
  .then(handleResponse)
  .then(data => {
    localStorage.setItem("user", JSON.stringify(data));
    return data;
  });
}

function logout() {
  const requestOptions = {
    method: "POST",
    headers: {
      "Content-type": "application/json"
    }
  }

  const url = `${process.env.REACT_APP_BELL_SERVICE_URL}/bell/logout`;
  return fetch(url, requestOptions)
  .then(handleResponse)
  .then(data => {
    localStorage.removeItem("user");
    return data;
  });
}

function register(user) {
  const requestOptions = {
    method: "POST",
    headers: {
      ...authHeader(),
      "Content-type": "application/json"
    },
    body: JSON.stringify(user)
  }

  const url = `${process.env.REACT_APP_BELL_SERVICE_URL}/bell/hidden/account`;
  return fetch(url, requestOptions).then(handleResponse);
}

function handleResponse(response) {
  return response.json().then(data => {
    if (!response.ok) {
      return Promise.reject(data.message);
    }
    return data;
  });
}
