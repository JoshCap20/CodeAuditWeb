function displayRequest(code, iterations, options) {
    document.getElementById('inputs').innerHTML = 'Code: ' + code +
        '<br>Iterations: ' + iterations +
        '<br>Selected Options: ' + options.join(', ');
}

function displayResponse(jsonResponse) {
    let formattedResults = '<h2>Results:</h2>';

    if (jsonResponse.time) {
        formattedResults += '<div><strong>Execution Time:</strong><br>';
        formattedResults += `Milliseconds: ${jsonResponse.time.milliseconds}<br>`;
        formattedResults += `Seconds: ${jsonResponse.time.seconds}<br>`;
        formattedResults += `Minutes: ${jsonResponse.time.minutes}</div>`;
    }

    if (jsonResponse.memory) {
        formattedResults += '<div><strong>Memory Usage:</strong><br>';
        formattedResults += `Kilobytes: ${jsonResponse.memory.kilobytes}<br>`;
        formattedResults += `Megabytes: ${jsonResponse.memory.megabytes}<br>`;
        formattedResults += `Gigabytes: ${jsonResponse.memory.gigabytes}</div>`;
    }

    if (jsonResponse.profile) {
        formattedResults += `<div><strong>Profile Data:</strong><pre style="font-family: monospace;">${escapeHtml(jsonResponse.profile)}</pre></div>`;
    }

    if (jsonResponse.flamegraph) {
        formattedResults += `<div><strong>Flame Graph:</strong> <a href="/flamegraph" target="_blank">View</a></div>`;
    }

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

        displayRequest(code, iterations, selectedOptions);
        getResults(code, selectedOptions, iterations);
    }
});
