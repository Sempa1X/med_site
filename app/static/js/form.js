var $add = document.getElementsByClassName('add')[0];
var $form = document.getElementsByClassName('form')[0];
$add.addEventListener('click', function(event) {
  var $input = document.createElement('input');
  $input.type = 'text';
  $input.placeholder = 'Кол-во';
  $input.classList.add('amount');
  $form.insertBefore($input, $add);
});


function changeHandler(event) {
  const step = event.target.step;

    // здесь я получаю оба значения одной строкой, нужно одно
    if (step === '15') {
        alert(step)
        }
    // здесь я получаю оба значения одной строкой, нужно одно
    if (step === 'accountSelect') {
        this.accountId = event.target.value;
        }    
    }

var a=document.getElementById('s1').value;