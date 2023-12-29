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
    form.style.height = '400px';
    form.style.width = '100%';

    const methodSelector = createMethodSelector(['GET', 'POST', 'PUT', 'DELETE']);
    form.appendChild(methodSelector);

    const urlInput = createInput('url', 'URL');
    form.appendChild(urlInput);

    const headersInput = createInput('headers', 'Headers');
    form.appendChild(headersInput);

    const bodyInput = createTextArea('body', 'Body');
    form.appendChild(bodyInput);

    const submitButton = createButton('Send Request', 'submit', handleFormSubmit);
    form.appendChild(submitButton);

    return form;
}

async function handleFormSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const method = formData.get('method');
    const url = formData.get('url');
    const headers = parseHeaders(formData.get('headers'));
    const body = formData.get('body');

    const response = await fetch(url, { method, headers, body });
    const responseBody = await response.text();

    displayResponse(responseBody);
}

function parseHeaders(headersString) {
    const headers = new Headers();
    headersString.split('\n').forEach(line => {
        const [key, value] = line.split(':');
        headers.append(key.trim(), value.trim());
    });
    return headers;
}

function displayResponse(response) {
    const responseContainer = document.getElementById('responseContainer');
    responseContainer.textContent = response;
}
