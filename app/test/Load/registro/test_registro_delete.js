import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 50,
  iterations: 50,
};

export default function () {
  const id = Math.floor(Math.random() * 200) + 1;
  const res = http.del(`http://localhost:8000/registros/${id}`);

  check(res, {
    'registro eliminado (200)': (r) =>
      r.status === 200 || r.status === 204 || r.status === 404,
  });
}
