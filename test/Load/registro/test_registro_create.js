import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 50,
  iterations: 200, 
};

export default function () {
  const url = 'http://localhost:8000/registros/';
  const payload = JSON.stringify({
    nombre_archivo: `radiografia_${Math.random().toString(36).substring(7)}.png`,
    probabilidad_sano: Math.random() * 100,
    probabilidad_viral: Math.random() * 100,
    probabilidad_bacteriana: Math.random() * 100,
    estado: ['Sano', 'Viral', 'Bacteriana'][Math.floor(Math.random() * 3)],
    username: 'Tester',
    radiografia: 'prueba'
  });

  const params = {
    headers: { 'Content-Type': 'application/json' },
  };

  const res = http.post(url, payload, params);

  check(res, {
    'registro creado (200)': (r) => r.status === 201 || r.status === 200,
  });
}
