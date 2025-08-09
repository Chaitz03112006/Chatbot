document.addEventListener("DOMContentLoaded", function () {
    const numPetals = 20; // number of petals
    const container = document.body;

    for (let i = 0; i < numPetals; i++) {
        const petal = document.createElement("img");
        petal.src = "/static/petal.png";
        petal.classList.add("petal");

        petal.style.left = Math.random() * 100 + "vw";
        petal.style.animationDuration = 5 + Math.random() * 5 + "s"; 
        petal.style.opacity = Math.random();
        petal.style.transform = `scale(${Math.random()})`;

        container.appendChild(petal);
    }
});
