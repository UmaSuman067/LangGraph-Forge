// Calculator logic and event handling
// This script is executed after the DOM has been fully parsed (deferred)

document.addEventListener('DOMContentLoaded', () => {
    // Select the display input element. The outer div also has id="display", so we target the input inside it.
    const display = document.querySelector('#display input');
    const buttons = document.querySelectorAll('.btn');

    // State variables
    let currentInput = '';
    let operator = null;
    let operand1 = null;
    let resetDisplay = false;

    // Helper to update the display value
    function updateDisplay(value) {
        display.value = value;
    }

    // Append a number or decimal to the current input
    function appendNumber(num) {
        if (resetDisplay) {
            currentInput = '';
            resetDisplay = false;
        }

        // Handle multiple decimal points
        if (num === '.' && currentInput.includes('.')) {
            return;
        }

        // Handle leading zeros
        if (currentInput === '0' && num !== '.') {
            currentInput = num;
        } else if (currentInput === '' && num === '.') {
            // If starting with a decimal, prepend 0
            currentInput = '0.';
        } else {
            currentInput += num;
        }

        updateDisplay(currentInput);
    }

    // Set the operator and compute if needed
    function setOperator(op) {
        if (operand1 !== null && operator !== null && currentInput !== '') {
            compute();
        }
        operand1 = parseFloat(currentInput);
        operator = op;
        resetDisplay = true;
    }

    // Perform the calculation
    function compute() {
        if (operator === null || currentInput === '') {
            return;
        }
        const operand2 = parseFloat(currentInput);
        let result;
        switch (operator) {
            case '+':
                result = operand1 + operand2;
                break;
            case '-':
                result = operand1 - operand2;
                break;
            case '*':
                result = operand1 * operand2;
                break;
            case '/':
                if (operand2 === 0) {
                    updateDisplay('Error');
                    operand1 = null;
                    operator = null;
                    currentInput = '';
                    return;
                }
                result = operand1 / operand2;
                break;
            default:
                return;
        }
        // Remove trailing .0 for whole numbers
        if (Number.isInteger(result)) {
            result = result.toString();
        } else {
            result = result.toString();
        }
        updateDisplay(result);
        operand1 = result;
        currentInput = '';
        resetDisplay = true;
    }

    // Event listeners for buttons
    buttons.forEach((button) => {
        if (button.classList.contains('number') || button.classList.contains('decimal')) {
            button.addEventListener('click', () => {
                const value = button.dataset.value;
                appendNumber(value);
            });
        } else if (button.classList.contains('operator')) {
            button.addEventListener('click', () => {
                const op = button.dataset.op;
                setOperator(op);
            });
        } else if (button.id === 'equals') {
            button.addEventListener('click', () => {
                compute();
            });
        } else if (button.id === 'clear') {
            button.addEventListener('click', () => {
                currentInput = '';
                operand1 = null;
                operator = null;
                resetDisplay = false;
                updateDisplay('');
            });
        }
    });
});
