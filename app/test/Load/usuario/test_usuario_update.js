import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 50,
  iterations: 200,
};

const BASE_URL = 'http://localhost:8000/usuarios/';

export default function () {
  const user_id = Math.floor(Math.random() * 200) + 1;
  const payload = JSON.stringify({
    nombre: `UsuarioActualizado_${__ITER}`,
    password: "654321",
    disabled: false,
    rol: "admin"
  });

  const headers = { 'Content-Type': 'application/json' };
  const res = http.put(`${BASE_URL}${user_id}`, payload, { headers });

  check(res, {
    'status 200': (r) => r.status === 200,
    'actualizado correctamente': (r) => r.body.includes('UsuarioActualizado'),
  });

  sleep(0.5);
}
