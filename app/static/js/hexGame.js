let targetColor = '';
let red, green, blue;

function genColor() {
    // Generate random RGB values (0-255)
    red = Math.floor(Math.random() * 256);
    green = Math.floor(Math.random() * 256);
    blue = Math.floor(Math.random() * 256);
    
    // Convert to hex color
    targetColor = '#' + red.toString(16).padStart(2, '0') + 
                       green.toString(16).padStart(2, '0') + 
                       blue.toString(16).padStart(2, '0');
    
    targetColor = targetColor.toUpperCase();
    // Display the target color
    document.getElementById("targetColor").style.background = targetColor;
    
    // Clear previous guess and feedback
    document.getElementById("guessColor").style.background = '#f0f0f0';
    document.getElementById("guess").value = '';
    document.getElementById("feedback").textContent = '';
    
    console.log('Target color:', targetColor, 'RGB:', red, green, blue);
}

function guessLogic() {
    const guessInput = document.getElementById("guess").value.toUpperCase();
    
    // Validate input for 6 hex digits
    if (!/^[0-9A-F]{6}$/.test(guessInput)) {
        document.getElementById("feedback").textContent = 'Invalid hex code (0-9, A-F)';
        document.getElementById("feedback").style.color = '#e74c3c';
        return;
    }
    
    // Use the 6-digit hex code directly
    const fullHex = '#' + guessInput;
    console.log('Guess:', guessInput);
    
    // Display the guessed color
    document.getElementById("guessColor").style.background = fullHex;
    
    // Check if correct
    if (fullHex === targetColor) {
        document.getElementById("feedback").textContent = 'Correct! Generating new color...';
        document.getElementById("feedback").style.color = '#27ae60';
        setTimeout(() => {
            genColor();
        }, 2000);
    } else {
        // Provide feedback on how close the guess is
        const feedback = getColorFeedback(fullHex);
        document.getElementById("feedback").textContent = feedback;
        document.getElementById("feedback").style.color = '#f39c12';
    }
}

function getColorFeedback(guessHex) {
    // Parse the guessed color
    const guessR = parseInt(guessHex.slice(1, 3), 16);
    const guessG = parseInt(guessHex.slice(3, 5), 16);
    const guessB = parseInt(guessHex.slice(5, 7), 16);
    
    // Calculate differences
    const rDiff = Math.abs(red - guessR);
    const gDiff = Math.abs(green - guessG);
    const bDiff = Math.abs(blue - guessB);
    
    const totalDiff = rDiff + gDiff + bDiff;
    
    if (totalDiff < 50) {
        return 'Very close';
    } else if (totalDiff < 100) {
        return 'Close';
    } else if (totalDiff < 200) {
        return 'Kinda close';
    } else {
        return 'Very far';
    }
}

// Add event listener for Enter key
document.addEventListener('DOMContentLoaded', function() {
    const guessInput = document.getElementById("guess");
    guessInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            guessLogic();
        }
    });
});