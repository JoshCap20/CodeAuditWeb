document.addEventListener('DOMContentLoaded', initialize);

async function initialize() {
    setupRequestContainer();
}

function setupRequestContainer() {
    const requestContainer = document.getElementById('requestContainer');
    requestContainer.appendChild(createForm());
}

function createForm() {
    const form = document.createElement('form');
    form.id = 'endpointRequest';
    form.method = 'POST';
    form.action = '/endpoint';
    form.style.width = '100%';

    const methodSelector = createMethodSelector(['GET', 'POST', 'PUT', 'DELETE']);
    form.appendChild(methodSelector);

    const urlInput = createInput('url', 'URL');
    form.appendChild(urlInput);

    const headersInput = createInput('headers', 'Headers');
    form.appendChild(headersInput);

    const bodyInput = createTextArea('body', 'Body');
    bodyInput.setAttribute('rows', '10');
    form.appendChild(bodyInput);

    const submitButton = createButton('Send Request', 'submit');
    form.appendChild(submitButton);

    form.addEventListener('submit', handleFormSubmit);

    return form;
}

async function handleFormSubmit(event) {
    event.preventDefault();

    clearResponse();

    const form = event.currentTarget;
    const formData = new FormData(form);
    const method = formData.get('method');
    const url = formData.get('url');
    const headers = parseHeaders(formData.get('headers'));
    let body = formData.get('body');

    if (headers.get('Content-Type') === 'application/json') {
        try {
            body = JSON.parse(body);
        } catch (error) {
            return displayResponse('Invalid JSON body');
        }
    }

    try {
        if (method === 'GET' || method === 'DELETE') {
            body = undefined;
        }
        const response = await fetch(url, { method, headers, body });
        const contentType = response.headers.get('Content-Type');

        let responseBody;
        if (contentType && contentType.includes('application/json')) {
            responseBody = JSON.stringify(await response.json(), null, 2);
        } else {
            responseBody = await response.text();
        }

        displayResponse(responseBody);
    } catch (error) {
        displayResponse(`Error: ${error.message}`);
    }
}

function parseHeaders(headersString) {
    const headers = new Headers();
    if (headersString) {
        headersString.split('\n').forEach(line => {
            const parts = line.split(':');
            if (parts.length === 2) {
                headers.append(parts[0].trim(), parts[1].trim());
            }
        });
    }
    return headers;
}

function displayResponse(response) {
    const responseElement = document.createElement('pre');
    responseElement.style.whiteSpace = 'pre-wrap';
    const responseText = document.createElement('code');
    responseText.className = 'json';
    responseText.textContent = response;
    responseElement.appendChild(responseText);

    const responseContainer = document.getElementById('responseContainer');
    responseContainer.appendChild(responseElement);
    hljs.highlightElement(responseElement);

    showElement(responseContainer);
}

function clearResponse() {
    const responseContainer = document.getElementById('responseContainer');
    responseContainer.innerHTML = '';
    hideElement(responseContainer);
}