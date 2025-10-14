const modal = document.getElementById("modal");
const openBtn = document.getElementById("modal-btn");
const closeBtn = document.getElementById("close");
const overlay = document.getElementById("modal-overlay");


function openModal(){
    modal.style.display = "grid";
    overlay.style.display = "block"; 
}
function closeModal(){
    modal.style.display = "none";
    overlay.style.display = "none";
}
openBtn.addEventListener("click", openModal)
closeBtn.addEventListener("click", closeModal)

document.addEventListener('click', function(event) {
    if (event.target.id === "modal-overlay") {
        closeModal();
    }
    console.log(event.target.id);
});


