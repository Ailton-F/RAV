//DELETA USUÁRIOS
function deleteUser(e){
  let id = $(e).attr('id')
  let url = `/usuarios/delete/${id}/`
  Swal.fire({
      title: 'Tem certeza?',
      text: 'Quer mesmo excluir o usuário:? ',
      icon: 'error',
      showDenyButton: true,
      confirmButtonText: 'Sim',
      denyButtonText: `Não`,
    }).then(function (result) {
      if (result.isConfirmed){
        $.ajax({
          type: "POST",
          url: url
        }).done((res)=>{
          let table = $(res).find('table').children()
          $('table').html(table);
        });
      }
    });
}

// DELETA VISITAS
function deleteVisit(e) {
    let id = $(e).attr('id')
    let url = `/usuarios/delete_visit/${id}`
    Swal.fire({
        title: 'Tem certeza?',
        text: 'Quer mesmo desmarcar o agendamento? ',
        icon: 'error',
        showDenyButton: true,
        confirmButtonText: 'Sim',
        denyButtonText: `Não`,
      }).then(function (result) {
        if (result.isConfirmed){
          $.ajax({
            type: "POST",
            url: url
          }).done((res)=>{
            let table = $(res).find('table').children()
            $('table').html(table);
          });
        }
      });
  }