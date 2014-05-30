/*
    Sample script.js JavaScript file

    Author: Mike Dory
    11.12.11, updated 11.24.12
*/


// your fancy JS code goes here!

function search() {
    query = $("#search").val();
    document.location.href = '/search/?query=' + query;
}


$(document).ready(function() {
    $("#tag-field").tagit({
        allowSpaces: true
    });


    $(".definition").on("click", ".vote-button", function(event) {
        action = "vote";
        vote = $(this).attr("class").split(" ")[1];
        definition = $(this).parent().find("p").text();
        word_name = $(this).parent().attr("class").split(" ")[2];
        data = {
            "_xsrf": $("[name='_xsrf']").val(),
            "action": action,
            "vote": vote,
            "definition": definition,
            "word_name": word_name

        }
        $.ajax({
            type: 'POST',
            url: "/word/",
            data: data,
            error: function(error) {
                console.debug(JSON.stringify(error));
            },
            beforeSend: function(xhr, settings) {},
            success: function(data) {
                if (vote == "up") {
                    $(".vote-message").text("+1").show().delay(5000).fadeOut();
                } else if (vote == "down") {
                    $(".vote-message").text("-1").show().delay(5000).fadeOut();
                }
                $(".vote-tally").text("Votes: " + data['vote']);
                //document.location.href = '/thanks/';
            }
        });
    });

});