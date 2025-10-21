import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 50,
  duration: '1m',
};

export default function () {
  const res = http.get('http://localhost:8000/registros/');
  check(res, {
    'registros obtenidos (200)': (r) => r.status === 200,
  });
  const id = Math.floor(Math.random() * 200) + 1;
  const res2 = http.get(`http://localhost:8000/registros/${id}`);
  check(res2, {
    'registro individual obtenido (200)': (r) => r.status === 200,
  });
}
