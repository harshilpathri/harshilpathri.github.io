function genColor() {
    red = Math.floor(Math.random() * 16);
    green = Math.floor(Math.random() * 16);
    blue = Math.floor(Math.random() * 16);
    color = '#'+(red* 16 ** 5 + green * 16 ** 3 + blue * 16 ** 1).toString(16).padStart(6, '0');
    genBadColor("#475569");
    myFunction();
}

function genBadColor(guess) {
    console.log(red, green, blue);
    console.log(color);
    document.getElementById("rectangle2").style.background = guess;
}

function myFunction() {
    console.log(red, green, blue);
    console.log(color);
    document.getElementById("rectangle").style.background = color;
}

function guessLogic() {
    guess = document.getElementById("guess").value;
    console.log(guess);
    guess = "#" + guess[0] + "0" + guess[1] + "0" + guess[2] + "0";
    console.log(guess)
    if (color == guess) {
        genColor();
    }
    else {
        genBadColor(guess);
    }
}