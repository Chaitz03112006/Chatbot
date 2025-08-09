const canvas = document.getElementById('petalsCanvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const petals = [];
const petalImage = new Image();
petalImage.src = '/static/petal.png';

class Petal {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * -canvas.height;
        this.size = Math.random() * 20 + 10;
        this.speed = Math.random() + 0.5;
    }
    update() {
        this.y += this.speed;
        if (this.y > canvas.height) {
            this.y = -this.size;
            this.x = Math.random() * canvas.width;
        }
    }
    draw() {
        ctx.drawImage(petalImage, this.x, this.y, this.size, this.size);
    }
}

for (let i = 0; i < 30; i++) {
    petals.push(new Petal());
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    petals.forEach(petal => {
        petal.update();
        petal.draw();
    });
    requestAnimationFrame(animate);
}

petalImage.onload = animate;
