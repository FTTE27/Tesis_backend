import exec from 'k6/execution';

export function setup() {
  console.log('Iniciando pruebas completas de usuario');
}

export default function () {
  exec.test('test_usuario_create.js');
  exec.test('test_usuario_get.js');
  exec.test('test_usuario_update.js');
  exec.test('test_usuario_delete.js');
}
