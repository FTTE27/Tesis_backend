import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 50, 
  iterations: 200, 
};

const BASE_URL = 'http://localhost:8000/usuarios/';

export default function () {
  const payload = JSON.stringify({
    nombre: `Usuario_${__ITER}`,
    username: `user_${__VU}_${__ITER}`,
    password: "123456",
    disabled: false,
    rol: "usuario"
  });

  const headers = { 'Content-Type': 'application/json' };
  const res = http.post(BASE_URL, payload, { headers });

  check(res, {
    'status 201 o 200': (r) => r.status === 201 || r.status === 200,
    'contiene username': (r) => r.body.includes('username'),
  });

  sleep(0.5);
}
