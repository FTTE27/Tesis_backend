import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 50,
  iterations: 200,
};

export default function () {
  const id = Math.floor(Math.random() * 200) + 1; 
  const url = `http://localhost:8000/comentarios/${id}`;
  const payload = JSON.stringify({
    titulo: `Comentario ${Math.random().toString(36).substring(7)} Actualizado`,
    nombre: 'Usuario Test',
    correo: 'test@example.com',
    mensaje: 'Este comentario fue actualizado.'
  });

  const params = {
    headers: { 'Content-Type': 'application/json' },
  };

  const res = http.put(url, payload, params);

  check(res, {
    'comentario actualizado (200)': (r) => r.status === 200,
  });
}
