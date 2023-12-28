function displayResponse(jsonResponse) {
    let formattedResults = '<div style="white-space: pre-wrap;">' + formatJson(jsonResponse, '') + '</div>';
    document.getElementById('outputs').innerHTML = formattedResults;
}

function formatJson(jsonObj, indent) {
    let formattedJson = '';
    for (const key in jsonObj) {
        if (jsonObj.hasOwnProperty(key)) {
            if (jsonObj[key] === null) {
                continue;
            }
            formattedJson += `${indent}<strong>${key}:</strong> `;
            if (typeof jsonObj[key] === 'object' && jsonObj[key] !== null) {
                if (jsonObj[key].link) {
                    // Handle link
                    formattedJson += `<a href="${jsonObj[key].link}" target="_blank">${jsonObj[key].link}</a>\n`;
                } else {
                    // Recursive call for nested objects with increased indent
                    formattedJson += '\n' + formatJson(jsonObj[key], indent + '  ');
                }
            } else {
                // Handle normal and multiline strings
                formattedJson += `${escapeHtml(jsonObj[key])}<br>`;
            }
        }
    }
    return formattedJson;
}

async function getResults(code, options, iterations) {
    document.getElementById('outputs').innerHTML = 'Loading...';

    if (!code) {
        document.getElementById('outputs').innerHTML = 'No code to run.';
        return;
    }

    if (!iterations) {
        document.getElementById('outputs').innerHTML = 'No iterations to run.';
        return;
    }

    if (!options || options.length === 0) {
        document.getElementById('outputs').innerHTML = 'No options selected.';
        return;
    }

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: code,
                options: options,
                iterations: iterations
            })
        });
        const myJson = await response.json();
        displayResponse(myJson);
    } catch (error) {
        console.error('Error fetching results:', error);
        document.getElementById('outputs').innerHTML = 'Failed to get results.';
    }
}

function escapeHtml(text) {
    if (typeof text === 'string') {
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
    return text;
}

document.addEventListener('DOMContentLoaded', function () {
    var editor = ace.edit("codeInput");
    editor.setTheme("ace/theme/twilight");
    editor.setOption("enableFoldWidgets", true);
    editor.getSession().setMode("ace/mode/python");
    editor.getSession().setUseWrapMode(true);
    editor.setOptions({
        enableBasicAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: true,
        tabSize: 4,
        useSoftTabs: true
    });

    window.submitCode = function () {
        var code = editor.getValue();
        var iterations = document.getElementById('iterations').value;
        var options = document.querySelectorAll('input[name="option"]:checked');
        var selectedOptions = Array.from(options).map(function (el) { return el.value; });

        getResults(code, selectedOptions, iterations);
    }
});
