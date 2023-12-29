document.addEventListener('DOMContentLoaded', initialize);

async function initialize() {
    setupRequestContainer();
    await populateLanguages();
}

function setupRequestContainer() {
    const requestContainer = document.getElementById('requestContainer');
    const topRow = createTopRow();
    const optionsRow = createOptionsRow();
    const bottomRow = createBottomRow();

    requestContainer.appendChild(topRow);
    requestContainer.appendChild(createEditor());
    requestContainer.appendChild(optionsRow);
    requestContainer.appendChild(bottomRow);
}

function createTopRow() {
    const topRow = document.createElement('div');
    topRow.className = 'top-row';

    const iterationsContainer = createIterationsContainer();
    topRow.appendChild(iterationsContainer);

    return topRow;
}

function createIterationsContainer() {
    const iterationsContainer = document.createElement('div');
    iterationsContainer.className = 'iterations-container';

    const iterationsLabel = createLabel('iterations', 'Iterations:');
    const iterationsInput = createInput('iterations', '1', 'number', '1');

    iterationsContainer.appendChild(iterationsLabel);
    iterationsContainer.appendChild(iterationsInput);

    return iterationsContainer;
}

function createOptionsRow() {
    const optionsRow = document.createElement('div');
    optionsRow.className = 'options-row';

    const fullScreenBtn = createButton('Full Screen', 'button', toggleFullScreen, 'fullScreenBtn');
    fullScreenBtn.id = 'fullScreenBtn';
    optionsRow.appendChild(fullScreenBtn);
    optionsRow.appendChild(createButton('Clear Editor', 'button', () => window.editor.setValue('')));
    optionsRow.appendChild(createButton('-', 'button', () => window.editor.setFontSize(window.editor.getFontSize() - 1)));
    optionsRow.appendChild(createButton('+', 'button', () => window.editor.setFontSize(window.editor.getFontSize() + 1)));

    return optionsRow;
}

function createBottomRow() {
    const bottomRow = document.createElement('div');
    bottomRow.className = 'bottom-row';
    bottomRow.appendChild(createButton('Analyze Code', 'submit', submitCode));

    return bottomRow;
}

async function populateLanguages() {
    try {
        const response = await fetch('/languages');
        const languages = await response.json();
        const languageSelector = createLanguageSelector(languages);
        document.querySelector('.top-row').appendChild(languageSelector);
    } catch (error) {
        console.error('Error fetching languages:', error);
    }
}

function createLanguageSelector(languages) {
    const container = document.createElement('div');
    const label = createLabel('language', 'Language:');
    const select = createSelectWithPlaceHolder('language', languages, "Select a Language");

    select.addEventListener('change', async () => {
        await populateStrategies(select.value);
        showElement(document.getElementById('strategyOptions'));
    });

    container.append(label, select);
    return container;
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

async function populateStrategies(language) {
    try {
        const response = await fetch(`/strategies?language=${language}`);
        const strategies = await response.json();
        const optionsContainer = document.getElementById('strategyOptions');
        optionsContainer.innerHTML = '';

        const gridContainer = document.createElement('div');
        gridContainer.className = 'grid-container';

        strategies.forEach(strategy => {
            gridContainer.appendChild(createCheckbox(strategy, formatLabel(strategy) + ' Analysis'));
        });

        optionsContainer.appendChild(gridContainer);
    } catch (error) {
        console.error('Error fetching strategies:', error);
    }
}

function toggleFullScreen() {
    const editorDiv = document.getElementById('codeInput');
    editorDiv.classList.toggle('full-screen');

    const fullScreenBtn = document.getElementById('fullScreenBtn');
    if (editorDiv.classList.contains('full-screen')) {
        fullScreenBtn.textContent = 'Exit Full Screen';
        fullScreenBtn.classList.add('full-screen-btn');
    } else {
        fullScreenBtn.textContent = 'Full Screen';
        fullScreenBtn.classList.remove('full-screen-btn');
    }

    window.editor.resize();
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

    if (data.output) {
        data.output = splitLines(data.output);
    }

    if (data.profile) {
        data.profile.profile = splitLines(data.profile.profile);
    }

    if (data.advanced_profile) {
        data.advanced_profile.profile = splitLines(data.advanced_profile.profile);
        data.advanced_profile.line_profile = splitLines(data.advanced_profile.line_profile);
    }

    data = Object.keys(data).reduce((acc, key) => {
        if (data[key]) {
            acc[key] = data[key];
        }
        return acc;
    }
        , {});

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

    const responseContainer = document.getElementById('responseContainer');
    responseContainer.appendChild(pre);
    showElement(responseContainer);

    hljs.highlightElement(codeElement);
}

function splitLines(data) {
    return data.split('\n');
}

function clearResponse() {
    const responseContainer = document.getElementById('responseContainer');
    const graphContainer = document.getElementById('graphContainer');

    responseContainer.innerHTML = '';
    graphContainer.innerHTML = '';

    hideElement(responseContainer);
    hideElement(graphContainer);
}

function displayImage(link) {
    // Defeats browser caching old image
    const uniqueString = new Date().getTime();
    const cachedBusterLink = link + '?v=' + uniqueString;

    const img = document.createElement('img');
    img.src = cachedBusterLink;
    img.style.width = '100%';

    const graphContainer = document.getElementById('graphContainer');
    graphContainer.appendChild(img);
    showElement(graphContainer);
}

function escapeHtml(text) {
    if (typeof text !== 'string') return text;
    return text.replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
