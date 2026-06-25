// CKEditor 5 Initialization for Django Admin BlogPost content field
window.addEventListener('load', function() {
    var contentField = document.getElementById('id_content');
    if (contentField && typeof ClassicEditor !== 'undefined') {
        ClassicEditor
            .create(contentField)
            .catch(error => {
                console.error('CKEditor 5 initialization failed:', error);
            });
    }
});
