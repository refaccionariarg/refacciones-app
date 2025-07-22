// Animación de carga suave
document.addEventListener("DOMContentLoaded", () => {
    document.querySelector('.container').style.opacity = 0;
    setTimeout(() => {
        document.querySelector('.container').style.transition = "opacity 0.8s ease";
        document.querySelector('.container').style.opacity = 1;
    }, 200);
});
