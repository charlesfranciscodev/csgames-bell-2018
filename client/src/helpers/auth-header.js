export function authHeader() {
  let header = {
    "secretKey": "qwerty123"
  };

  let user = JSON.parse(localStorage.getItem("user"));
  if (user && user.token) {
    header.Authorization = `Bearer ${user.token}`;
  }

  return header;
}
