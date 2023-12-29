// Navigation
document.addEventListener('DOMContentLoaded', function () {
    loadHeader();
    markActiveLink();
});

function loadHeader() {
    const headerHtml = `
        <header class="navbar">
            <nav>
                <ul>
                    <li><a href="/" class="nav-link">Code</a></li>
                    <li><a href="https://github.com/JoshCap20/CodeAuditWeb" target="_blank" class="nav-link github-link">
                        <img src="/static/favicon.ico" alt="GitHub" class="github-icon">
                    </a></li>
                    <li><a href="/endpoint" class="nav-link">Endpoint</a></li>
                </ul>
            </nav>
        </header>
    `;

    document.body.insertAdjacentHTML('afterbegin', headerHtml);
}

function markActiveLink() {
    const currentUrl = window.location.href;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        if (link.href === currentUrl) {
            link.classList.add('active');
        }
    });
};

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

function createInput(name, placeholder, type = 'text', value = '', min = 1,) {
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

function createButton(text, type, onClickFunction = () => { }) {
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

function createSelectWithPlaceHolder(name, options, placeholder) {
    const select = createSelect(name, options);
    select.insertAdjacentHTML('afterbegin', `<option value="" disabled selected>${placeholder}</option>`);
    return select;
}

function createSelect(name, options, id = true) {
    const select = document.createElement('select');
    select.name = name;
    if (id) {
        select.id = name;
    }

    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.textContent = option.charAt(0).toUpperCase()
        + option.slice(1)
        select.appendChild(optionElement);
    });

    return select;
}

function createMethodSelector(options) {
    return createSelect('method', options, false);
}