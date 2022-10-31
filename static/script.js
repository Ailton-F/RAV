$(document).ready( () => { 
$('.delete').click(function(){
    let id = $(this).attr('value')
    let url = `/delete/${id}`
    Swal.fire({
        title: 'Tem certeza?',
        text: 'Quer mesmo excluir o usuário?',
        icon: 'error',
        showDenyButton: true,
        confirmButtonText: 'Sim',
        denyButtonText: `Não`,
      }).then(function (result) {
        if (result.isConfirmed){
          $.ajax({
            type: "POST",
            url: url
          }).done(function(res){
            let res_table = $(res).find('.table');
            // $(res).find('.table');
            $('.table').remove();
            $('main').append(res_table);
          }).fail(function(jqXHr, textStatus){
            console.log(textStatus, jqXHR);
          });
        }
      });
  });
});
