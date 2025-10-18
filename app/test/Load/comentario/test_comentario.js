import { exec } from 'k6/execution';

export function setup() {
  console.log('Iniciando pruebas completas de comentarios');
}

export default function () {
  exec.test('test_comentario_create.js');
  exec.test('test_comentario_get.js');
  exec.test('test_comentario_update.js');
  exec.test('test_comentario_delete.js');
}
