import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 50,
  iterations: 200, 
};

export default function () {
  const url = 'http://localhost:8000/comentarios';
  const payload = JSON.stringify({
    titulo: `Comentario ${Math.random().toString(36).substring(7)}`,
    nombre: 'Usuario Test',
    correo: 'test@example.com',
    mensaje: 'Este es un comentario de prueba automatizada.'
  });

  const params = {
    headers: { 'Content-Type': 'application/json' },
  };

  const res = http.post(url, payload, params);

  check(res, {
    'comentario creado (200)': (r) => r.status === 201 || r.status === 200,
    'contiene titulo': (r) => r.body.includes('titulo'),
  });
}
