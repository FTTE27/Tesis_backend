import http from 'k6/http';
import { check } from 'k6';
import { open } from 'k6/fs';

export const options = {
  vus: 50,
  iterations: 200,
};

export default function () {
  const url = 'http://localhost:8000/models/predict';
  const img = open('./test_image.jpg', 'b'); 

  const formData = {
    file: http.file(img, 'radiografia.jpg', 'image/jpeg'),
  };

  const res = http.post(url, formData);

  check(res, {
    'predicción exitosa (200)': (r) => r.status === 200,
  });
}
