document.addEventListener("DOMContentLoaded", function () {
    var canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        canvasWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth,
        canvasHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight,
        requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame || window.msRequestAnimationFrame;

    var persons = [],
        numberOfFirefly = 30,
        birthToGive = 25;

    var colors = [];
    colors[2] = [];
    colors[2]["background"] = "#2F294F";
    colors[2][1] = "rgba(74,49,89,";
    colors[2][2] = "rgba(130,91,109,";
    colors[2][3] = "rgba(185,136,131,";
    colors[2][4] = "rgba(249,241,204,";

    var colorTheme = 2,
        mainSpeed = 1;

    function getRandomInt(min, max, exept) {
        var i = Math.floor(Math.random() * (max - min + 1)) + min;
        if (typeof exept == "undefined") return i;
        else if (typeof exept == "number" && i == exept) return getRandomInt(min, max, exept);
        else if (typeof exept == "object" && i >= exept[0] && i <= exept[1]) return getRandomInt(min, max, exept);
        else return i;
    }

    function degToRad(deg) {
        return deg * (Math.PI / 180);
    }

    function Firefly(id) {
        this.id = id;
        this.width = getRandomInt(3, 6);
        this.height = this.width;
        this.x = getRandomInt(0, canvas.width - this.width);
        this.y = getRandomInt(0, canvas.height - this.height);
        this.speed = this.width <= 10 ? 2 : 1;
        this.alpha = 1;
        this.alphaReduction = getRandomInt(1, 3) / 1000;
        this.color = colors[colorTheme][getRandomInt(1, colors[colorTheme].length - 1)];
        this.direction = getRandomInt(0, 360);
        this.turner = getRandomInt(0, 1) == 0 ? -1 : 1;
        this.turnerAmp = getRandomInt(1, 2);
        this.isHit = false;
        this.stepCounter = 0;
        this.changeDirectionFrequency = getRandomInt(1, 200);
        this.shadowBlur = getRandomInt(5, 25);
    }

    Firefly.prototype.walk = function () {
        var next_x = this.x + Math.cos(degToRad(this.direction)) * this.speed,
            next_y = this.y + Math.sin(degToRad(this.direction)) * this.speed;

        if (next_x >= canvas.width - this.width || next_x <= 0) this.direction = 180 - this.direction;
        if (next_y >= canvas.height - this.height || next_y <= 0) this.direction = 360 - this.direction;

        this.x += Math.cos(degToRad(this.direction)) * this.speed;
        this.y += Math.sin(degToRad(this.direction)) * this.speed;

        this.update();
    };

    Firefly.prototype.update = function () {
        context.beginPath();
        context.fillStyle = this.color + this.alpha + ")";
        context.arc(this.x + this.width / 2, this.y + this.height / 2, this.width / 2, 0, 2 * Math.PI, false);
        context.shadowColor = this.color + this.alpha + ")";
        context.shadowBlur = this.shadowBlur;
        context.shadowOffsetX = 0;
        context.shadowOffsetY = 0;
        context.fill();
    };

    window.onload = function () {
        canvas.width = canvasWidth;
        canvas.height = canvasHeight;

        instantiatePopulation();
        animate();
    };

    function instantiatePopulation() {
        for (let i = 0; i < numberOfFirefly; i++) {
            persons[i] = new Firefly(i);
        }
    }

    function animate() {
        context.clearRect(0, 0, canvas.width, canvas.height);
        persons.forEach((firefly) => firefly.walk());
        requestAnimationFrame(animate);
    }

    canvas.onclick = function (e) {
        for (let i = 0; i < birthToGive; i++) {
            let firefly = new Firefly(persons.length);
            firefly.x = e.offsetX;
            firefly.y = e.offsetY;
            persons.push(firefly);
        }
    };
});
