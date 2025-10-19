import exec from 'k6/execution';

export function setup() {
  console.log('Iniciando pruebas completas de registros');
}

export default function () {
  exec.test('test_registro_create.js');
  exec.test('test_registro_get.js');
  exec.test('test_registro_update.js');
  exec.test('test_registro_delete.js');
}
