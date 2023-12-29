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
    requestContainer.appendChild(createButton('Run Code', 'submit', submitCode));
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

    if (!code || !iterations) {
        document.getElementById('responseContainer').innerText = 'Please fill in all fields.';
        return;
    }

    clearResponse();

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
    // TODO: Simplify this
    if (data.request.code) {
        data.request.code = splitLines(data.request.code);
    }

    if (data.request.output) {
        data.request.output = splitLines(data.request.output);
    }

    if (data.profile) {
        data.profile.profile = splitLines(data.profile.profile);
    }

    if (data.advanced_profile) {
        data.advanced_profile.profile = splitLines(data.advanced_profile.profile);
        data.advanced_profile.line_profile = splitLines(data.advanced_profile.line_profile);
    }

    const pre = document.createElement('pre');
    pre.style.whiteSpace = 'pre-wrap';
    const codeElement = document.createElement('code');
    codeElement.className = 'json';

    let jsonString = JSON.stringify(data, null, 4);

    if (data.dotgraph) {
        displayImage(data.dotgraph.link);
    }

    codeElement.innerHTML = escapeHtml(jsonString);

    pre.appendChild(codeElement);

    document.getElementById('responseContainer').appendChild(pre);

    hljs.highlightElement(codeElement);
}

function splitLines(data) {
    return data.split('\n');
}

function clearResponse() {
    document.getElementById('responseContainer').innerHTML = '';
    document.getElementById('graphContainer').innerHTML = '';
}

function displayImage(link) {
    // Defeats browser caching old image
    const uniqueString = new Date().getTime();
    const cachedBusterLink = link + '?v=' + uniqueString;

    const img = document.createElement('img');
    img.src = cachedBusterLink;
    img.style.width = '100%';
    document.getElementById('graphContainer').appendChild(img);
}

function escapeHtml(text) {
    if (typeof text !== 'string') return text;
    return text.replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
