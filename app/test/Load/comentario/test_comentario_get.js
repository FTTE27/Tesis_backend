import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 50,
  duration: '1m',
};

export default function () {
  const res = http.get('http://localhost:8000/comentarios');
  check(res, {
    'comentarios obtenidos (200)': (r) => r.status === 200,
  });
}
