const myModal = document.getElementById('myModal')

myModal.addEventListener('show.bs.modal', event => {
  const button = event.relatedTarget
  
  const idPedido = button.getAttribute('endereco-pedido-id')
  
  const confirmBtn = myModal.querySelector('#delete')
  
  confirmBtn.href = "/excluir_pedido/" + idPedido
})
