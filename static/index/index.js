document.addEventListener('DOMContentLoaded', initialize);

async function initialize() {
    setupRequestContainer();
    await populateOptions();
}

function setupRequestContainer() {
    const requestContainer = document.getElementById('requestContainer');
    requestContainer.appendChild(createEditor());
    requestContainer.appendChild(createLabel('iterations', 'Iterations:'));
    requestContainer.appendChild(createInput('iterations', '1', 'number', '1'));
    requestContainer.appendChild(createButton('Run Code', submitCode));
}

function createEditor() {
    const editorDiv = document.createElement('div');
    editorDiv.id = 'codeInput';
    editorDiv.style.height = '400px';
    editorDiv.style.width = '100%';

    const editor = ace.edit(editorDiv);
    editor.setTheme('ace/theme/twilight');
    editor.getSession().setMode('ace/mode/python');
    editor.setOptions({
        enableBasicAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: true,
        tabSize: 4,
        useSoftTabs: true
    });
    window.editor = editor; // Making editor globally accessible
    return editorDiv;
}

function createLabel(forId, text) {
    const label = document.createElement('label');
    label.htmlFor = forId;
    label.textContent = text;
    return label;
}

function createInput(id, value, type = 'text', min = '0') {
    const input = document.createElement('input');
    input.id = id;
    input.value = value;
    input.type = type;
    input.min = min;
    return input;
}

function createButton(text, onClickFunction) {
    const button = document.createElement('button');
    button.textContent = text;
    button.addEventListener('click', onClickFunction);
    return button;
}

async function populateOptions() {
    const strategies = await fetchStrategies();
    const optionsContainer = document.createElement('div');
    optionsContainer.className = 'options';
    strategies.forEach(strategy => {
        optionsContainer.appendChild(createCheckbox(strategy, formatLabel(strategy) + ' Analysis'));
    });
    document.getElementById('requestContainer').appendChild(optionsContainer);
}

async function fetchStrategies() {
    try {
        const response = await fetch('/strategies');
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Fetching strategies failed:', error);
        return [];
    }
}

function createCheckbox(id, label) {
    const container = document.createElement('div');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.id = checkbox.value = id;
    checkbox.name = 'option';

    const labelElement = document.createElement('label');
    labelElement.htmlFor = id;
    labelElement.textContent = label;

    container.append(checkbox, labelElement);
    return container;
}

function formatLabel(str) {
    return str.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ');
}

async function submitCode() {
    const code = window.editor.getValue();
    const iterations = document.getElementById('iterations').value;
    const options = Array.from(document.querySelectorAll('input[name="option"]:checked'))
        .map(el => el.value);

    if (!code || !iterations || options.length === 0) {
        document.getElementById('responseContainer').innerText = 'Please fill in all fields.';
        return;
    }

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, options, iterations })
        });

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        const data = await response.json();
        displayResponse(data);
    } catch (error) {
        console.error('Error fetching results:', error);
        document.getElementById('responseContainer').innerText = 'Failed to get results.';
    }
}

function displayResponse(data) {
    const responseContainer = document.getElementById('responseContainer');
    responseContainer.innerHTML = '';

    // TODO: Simplify this
    if (data.request.code) {
        data.request.code = splitLines(data.request.code);
    }

    if (data.request.profile && data.request.profile.profile) {
        data.request.profile.profile = splitLines(data.request.profile.profile);
    }

    if (data.request.advanced_profile) {
        data.request.advanced_profile.profile = splitLines(data.request.advanced_profile.profile);
        data.request.advanced.profile.line_profile = splitLines(data.request.advanced.profile.line_profile);
    }

    const pre = document.createElement('pre');
    pre.style.whiteSpace = 'pre-wrap';
    const codeElement = document.createElement('code');
    codeElement.className = 'json';

    let jsonString = JSON.stringify(data, null, 4);

    codeElement.innerHTML = escapeHtml(jsonString);

    pre.appendChild(codeElement);
    responseContainer.appendChild(pre);

    hljs.highlightBlock(codeElement);
}

function splitLines(data) {
    return data.split('\n');
}

function escapeHtml(text) {
    if (typeof text !== 'string') return text;
    return text.replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
