const hamburguer = document.querySelector('#toggle-btn');

hamburguer.addEventListener('click', ()=>{
    document.querySelector('#sidebar').classList.toggle('expanded');
})