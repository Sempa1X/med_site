document.querySelectorAll('.pacient_choice')[2].oninput = (ev) => {
    if (ev.target.checked) {
      document.querySelector('#aim-text').disabled = false;
    }
  }