// admin editor stuff

console.log("admin setting up");
$(document).ready(function() {
    console.log("admin is a go!");

    $("textarea").each(function(index) {
        var editor = new Editor();
        console.log("Editorising ", this);
        editor.render(this);
    });
});
