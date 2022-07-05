const invalidInput = document.querySelector('.invalid-input');
const formFields = document.querySelectorAll('.form-field');

const checkInputValidity = (inputField, errMsg) => {
  inputField.addEventListener('input', function (e) {
    if (e.target.checkValidity()) {
      this.classList.remove('invalid-input');
      errMsg.classList.add('display-none');
    } else {
      this.classList.add('invalid-input');
      errMsg.classList.remove('display-none');
    }
  });
};

let inputErrMsg;

for (let inputField of formFields) {
  if (inputField.classList.contains('invalid-input')) {
    inputErrMsg = inputField.nextElementSibling;
    checkInputValidity(inputField, inputErrMsg);
  }
}

//add input values
const addValue = (inputValue, inputValuesList, hiddenInput, valuesContainer, textInputField) => {
  if (inputValue.trim() !== '') {
    let p = document.createElement('p');
    let b = document.createElement('button');
    b.innerHTML = '&times;';
    b.classList.add('input-values_delete');
    b.setAttribute('title', 'click to remove');
    b.setAttribute('type', 'b');
    p.append(inputValue, b);
    p.classList.add('input-values_display');
    valuesContainer.append(p);

    inputValuesList.push(inputValue);
    hiddenInput.value = inputValuesList.join(',');
    textInputField.value = '';

    b.addEventListener('click', function () {
      this.parentElement.remove();
      let valueNum = inputValuesList.indexOf(inputValue)
      inputValuesList.splice(valueNum, 1);
      hiddenInput.value = inputValuesList.join(',');
    });

  }
};

function addInputValues(
  inputFieldClass,
  btnClass,
  valuesContainerClass,
  hiddenInputClass
) {
  let textInputField = document.querySelector(`.${inputFieldClass}`);
  let inputBtn = document.querySelector(`.${btnClass}`);
  let valuesContainer = document.querySelector(`.${valuesContainerClass}`);
  let hiddenInput = document.querySelector(`.${hiddenInputClass}`);

  if(hiddenInput) {

    let inputValuesList = [];
    
    for( let value of hiddenInput.value.split(",")) {
      addValue(value,inputValuesList, hiddenInput, valuesContainer, textInputField)
    }
  
    function callAddValue() {
      addValue(textInputField.value,inputValuesList, hiddenInput, valuesContainer, textInputField)
    }
  
    inputBtn.addEventListener('click', callAddValue);
    window.addEventListener('keypress', (e) => {
      if (e.key == 'Enter' && textInputField == document.activeElement) {
        e.preventDefault();
        callAddValue();
      }
    });
    
  }

}

addInputValues('cast-value', 'add-cast-btn', 'casts-values', 'casts-input');
addInputValues('series-value', 'add-series-btn','series-values','series-input');
addInputValues('tag-value', 'add-tag-btn', 'tags-values', 'tags-input');
