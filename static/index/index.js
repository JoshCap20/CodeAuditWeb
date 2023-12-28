function displayResponse(jsonResponse) {
    // Pretty print JSON response
    let formattedResults = '<pre>' + escapeHtml(JSON.stringify(jsonResponse, null, 4)) + '</pre>';

    document.getElementById('outputs').innerHTML = formattedResults;
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
                code: {
                    code_str: code,
                },
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
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
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
