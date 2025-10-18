import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 50,
  iterations: 200,
};

const BASE_URL = 'http://localhost:8000/usuarios/';

export default function () {
  const user_id = Math.floor(Math.random() * 200) + 1;
  const res = http.del(`${BASE_URL}${user_id}`);

  check(res, {
    'status 200 o 404': (r) => r.status === 200 || r.status === 404,
  });

  sleep(0.5);
}
