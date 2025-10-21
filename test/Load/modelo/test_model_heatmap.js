import http from 'k6/http';
import { check } from 'k6';

const img = open('./IM-0001-0001.jpeg', 'b');

export const options = {
  vus: 50,
  iterations: 200,
};

export default function () {
  const url = 'http://localhost:8000/models/predict_with_heatmap';


  const formData = {
    file: http.file(img, 'radiografia.jpg', 'image/jpeg'),
  };

  const params = {
      timeout: '360s',
  };
  
  const res = http.post(url, formData, params);

  check(res, {
    'heatmap generado (200)': (r) => r.status === 200
  });
}
