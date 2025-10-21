import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 50,
  iterations: 200,
};

export default function () {
  const id = Math.floor(Math.random() * 200) + 1; 
  const url = `http://localhost:8000/registros/${id}`;
  const payload = JSON.stringify({
    nombre_archivo: `radiografia_actualizada_${id}.png`,
    probabilidad_sano: Math.random() * 100,
    probabilidad_viral: Math.random() * 100,
    probabilidad_bacteriana: Math.random() * 100,
    estado: ['Sano', 'Viral', 'Bacteriana'][Math.floor(Math.random() * 3)],
    username: 'TesterUpdate',
    radiografia: 'nuevo'
  });

  const params = {
    headers: { 'Content-Type': 'application/json' },
  };

  const res = http.put(url, payload, params);

  check(res, {
    'registro actualizado (200)': (r) => r.status === 200,
  });
}
