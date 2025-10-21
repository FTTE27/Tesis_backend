import http from 'k6/http';
import { check } from 'k6';

const img = open('./IM-0001-0001.jpeg', 'b');

export const options = {
  vus: 50,
  iterations: 200,
};

export default function () {
  const url = 'http://localhost:8000/models/predict';

  const formData = {
    file: http.file(img, 'radiografia.jpg', 'image/jpeg'),
  };

  const params = {
    timeout: '180s',
  };

  const res = http.post(url, formData, params);

  check(res, {
    'predicción exitosa (200)': (r) => r.status === 200,
  });
}
