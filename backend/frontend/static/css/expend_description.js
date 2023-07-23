$(document).ready(function() {
    $("#toggleButton").click(function(e) {
        e.preventDefault();

        if ($("#fullDescription").is(':hidden')) {
            $("#shortDescription").hide();
            $("#fullDescription").show();
            $(this).text("Afficher moins");
        } else {
            $("#fullDescription").hide();
            $("#shortDescription").show();
            $(this).text("Afficher plus");
        }
    });
});
