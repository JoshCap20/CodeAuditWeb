// Nav Bar Active Link

document.addEventListener('DOMContentLoaded', () => {
    const currentUrl = window.location.href;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        if (link.href === currentUrl) {
            link.classList.add('active');
        }
    });
});

// Hidden Elements

function showElement(element) {
    element.classList.remove('hidden');
}

function hideElement(element) {
    element.classList.add('hidden');
}

// Form Factory Functions

function createTextArea(name, placeholder) {
    const textArea = document.createElement('textarea');
    textArea.name = name;
    textArea.placeholder = placeholder;
    return textArea;
}

function createInput(name, placeholder, type = 'text', value = '', min = 1, ) {
    const input = document.createElement('input');
    input.type = type;
    input.name = name;
    input.id = name;
    input.value = value;
    input.placeholder = placeholder;

    if (type === 'number') {
        input.type = 'number';
        input.min = min;
    }

    return input;
}

function createButton(text, type, onClickFunction = () => {}) {
    const button = document.createElement('button');
    button.type = type;
    button.textContent = text;
    button.addEventListener('click', onClickFunction);
    return button;
}

function createLabel(forId, text) {
    const label = document.createElement('label');
    label.htmlFor = forId;
    label.textContent = text;
    return label;
}

function createMethodSelector(options) {
    const select = document.createElement('select');
    select.name = 'method';
    options.forEach(method => {
        const option = document.createElement('option');
        option.value = method;
        option.textContent = method;
        select.appendChild(option);
    });
    return select;
}