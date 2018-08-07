var frm = $('form');
console.log(frm);

console.log("TESTING");
frm.submit(function () {
    var data = new FormData($('form').get(0));
    console.log(data);
    $("#suc").html("");
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function (data) {
            if (data['status'] === 'failed') {
                $("#sp").html("");
                for (var k in data['formerr']) {
                    var curr = data['formerr'][k][0];
                    console.log(curr);
                    console.log(document.getElementById('sp'));
                    document.getElementById('sp').innerHTML += curr;
                }
                $("#er").addClass("err");
                $("#sp").addClass("error");
                $("html, body").animate({scrollTop: 0}, "fast");
            } else {
                $("#er").remove();
                frm.fadeOut(400);
                setTimeout(
                    function () {
                        $("#suc").addClass("success");
                        $("#suc").html("Succesfully created");
                    }, 440);

                frm[0].reset();
            }
        },
        error: function (data) {
            $("#er").html("Something went wrong!");
            frm[0].reset();
        }
    });
    return false;
});