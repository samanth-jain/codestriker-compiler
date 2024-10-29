// static/js/editor.js
// static/js/editor.js

// Configure the path for Monaco Editor
require.config({ 
    paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.33.0/min/vs' }
});

// Load the Monaco Editor and initialize it
require(['vs/editor/editor.main'], function() {
    // Create the editor
    var editor = monaco.editor.create(document.getElementById('editor'), {
        value: '',
        language: 'python',
        theme: 'vs-dark',
    });

    // Load code from local storage if available
    var savedCode = localStorage.getItem('editorContent');
    if (savedCode) {
        editor.setValue(savedCode);
    }

    // Handle form submission
    document.getElementById('codeForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        // Save editor content to local storage
        localStorage.setItem('editorContent', editor.getValue());

        // Set the value of the hidden input field and submit the form
        document.getElementById('code').value = editor.getValue();
        this.submit(); // Submit the form

        document.getElementById('')
    });

    // Optional: Save editor content to local storage on every change
    editor.getModel().onDidChangeContent(function() {
        localStorage.setItem('editorContent', editor.getValue());
    });
});
