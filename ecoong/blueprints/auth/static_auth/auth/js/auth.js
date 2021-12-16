const inputs = document.querySelectorAll(".input");

function addcl() {
  let parent = this.parentNode.parentNode;
  parent.classList.add("focus");
}

function remcl() {
  let parent = this.parentNode.parentNode;
  if (this.value == "") {
    parent.classList.remove("focus");
  }
}

inputs.forEach((input) => {
  input.addEventListener("focus", addcl);
  input.addEventListener("blur", remcl);
});

const inputdivs = document.querySelectorAll('.input-div');

inputdivs.forEach(function(inputdiv) {
    const divinterna = inputdiv.getElementsByClassName('div')[0];
    console.log(divinterna);
    let h5 = divinterna.getElementsByTagName('h5')[0];
    console.log(h5);
    let input = divinterna.getElementsByTagName('input')[0];
    if(input.value != ''){
        h5.style.top = "-5px";
        h5.style.fontSize = "15px";
    }
})