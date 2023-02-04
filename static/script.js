$(document).ready( () => {
  $(".cpf-cnpj").mask("999.999.999-99");
  
  var socket = io.connect('https://asylum.ailtonborges.repl.co');

  socket.on('message', function (data) {
    // console.log(data)
    $.ajax({
      type: "GET",
      url: '/usuarios/chat_template'
    }).done((res)=>{
      let dados = $(res);
      if($('#sendMsg').val() != data.id){
        dados.addClass('align-self-start'); 
      }else{
        dados.addClass('align-self-end')
      }
        
      dados.find('.user-msg').text(data.email);
      dados.find('.msg-with-data').text(data.data);
      $('#chat').append(dados);
    });
  });

  $('#sendMsg').on('click', function() {
    if($.trim($('#msg').val()) == ''){
      return $('#msg').val('');
    }
    
    socket.emit('message', {data: $('#msg').val()});
    $('#msg').val('');
  })
  
  $('.admin-delete').click(function(){
    let id = $(this).attr('id')
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
            console.log(res);
            window.location.href = res;
          });
        }
      });
  });

  $('.config-radius').on('change', function(){
    if($('#cpf-radius').is(':checked')){
      $(".cpf-cnpj").mask("999.999.999-99");
      $('.cpf-cnpj').attr('placeholder', 'CPF')
    } else {
      $(".cpf-cnpj").mask("99.999.999/9999-99");
      $('.cpf-cnpj').attr('placeholder', 'CNPJ')
    }
  });

  
  $('.config').css({opacity: 0, visibility: "visible"}).animate({opacity: 1}, 'slow');
});

function subdReload(e){
  e.preventDefault();
}

var Cal = function(divId) {

  //Store div id
  this.divId = divId;

  // Days of week, starting on Sunday
  this.DaysOfWeek = [
    'Seg',
    'Ter',
    'Qua',
    'Qui',
    'Sex',
    'Sáb',
    'Dom'
  ];

  // Months, stating on January
  this.Months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro' ];

  // Set the current month, year
  var d = new Date();

  this.currMonth = d.getMonth();
  this.currYear = d.getFullYear();
  this.currDay = d.getDate();

};

// Goes to next month
Cal.prototype.nextMonth = function() {
  if ( this.currMonth == 11 ) {
    this.currMonth = 0;
    this.currYear = this.currYear + 1;
  }
  else {
    this.currMonth = this.currMonth + 1;
  }
  this.showcurr();
};

// Goes to previous month
Cal.prototype.previousMonth = function() {
  if ( this.currMonth == 0 ) {
    this.currMonth = 11;
    this.currYear = this.currYear - 1;
  }
  else {
    this.currMonth = this.currMonth - 1;
  }
  this.showcurr();
};

// Show current month
Cal.prototype.showcurr = function() {
  this.showMonth(this.currYear, this.currMonth);
};

// Show month (year, month)
Cal.prototype.showMonth = function(y, m) {

  var d = new Date()
  // First day of the week in the selected month
  , firstDayOfMonth = new Date(y, m, 1).getDay()
  // Last day of the selected month
  , lastDateOfMonth =  new Date(y, m+1, 0).getDate()
  // Last day of the previous month
  , lastDayOfLastMonth = m == 0 ? new Date(y-1, 11, 0).getDate() : new Date(y, m, 0).getDate();


  var html = '<table>';

  // Write selected month and year
  html += '<thead><tr>';
  html += '<td colspan="7">' + this.Months[m] + ' ' + y + '</td>';
  html += '</tr></thead>';


  // Write the header of the days of the week
  html += '<tr class="days">';
  for(var i=0; i < this.DaysOfWeek.length;i++) {
    html += '<td>' + this.DaysOfWeek[i] + '</td>';
  }
  html += '</tr>';

  // Write the days
  var i=1;
  do {

    var dow = new Date(y, m, i).getDay();

    // If Sunday, start new row
    if ( dow == 0 ) {
      html += '<tr>';
    }
    // If not Sunday but first day of the month
    // it will write the last days from the previous month
    else if ( i == 1 ) {
      html += '<tr>';
      var k = lastDayOfLastMonth - firstDayOfMonth+1;
      for(var j=0; j < firstDayOfMonth; j++) {
        html += '<td class="not-current">' + k + '</td>';
        k++;
      }
    }

    // Write the current day in the loop
    var chk = new Date();
    var chkY = chk.getFullYear();
    var chkM = chk.getMonth();
    if (chkY == this.currYear && chkM == this.currMonth && i == this.currDay) {
      html += '<td class="today">' + i + '</td>';
    } else {
      html += '<td class="normal">' + i + '</td>';
    }
    // If Saturday, closes the row
    if ( dow == 6 ) {
      html += '</tr>';
    }
    // If not Saturday, but last day of the selected month
    // it will write the next few days from the next month
    else if ( i == lastDateOfMonth ) {
      var k=1;
      for(dow; dow < 6; dow++) {
        html += '<td class="not-current">' + k + '</td>';
        k++;
      }
    }

    i++;
  }while(i <= lastDateOfMonth);

  // Closes table
  html += '</table>';

  // Write HTML to the div
  document.getElementById(this.divId).innerHTML = html;
};

// On Load of the window
window.onload = function() {

  // Start calendar
  var c = new Cal("divCal");			
  c.showcurr();

  // Bind next and previous button clicks
  getId('btnNext').onclick = function() {
    c.nextMonth();
  };
  getId('btnPrev').onclick = function() {
    c.previousMonth();
  };
}

// Get element by id
function getId(id) {
  return document.getElementById(id);
}