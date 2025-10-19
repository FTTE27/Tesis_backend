import exec from 'k6/execution';

export function setup() {
  console.log('Iniciando pruebas de carga para /models...');
}

export default function () {
  exec.test('test_model_predict.js');
  exec.test('test_model_heatmap.js');
}
