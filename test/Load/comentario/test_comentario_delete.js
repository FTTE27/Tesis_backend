import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 50,
  iterations: 200,
};

export default function () {
  const id = Math.floor(Math.random() * 200) + 1;
  const res = http.del(`http://localhost:8000/comentarios/${id}`);

  check(res, {
    'comentario eliminado (200)': (r) => r.status === 200 ,
  });
}
