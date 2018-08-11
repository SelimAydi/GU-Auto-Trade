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
                console.log("failed state");
                console.log(data['formerr']);
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
                console.log("success state");
                $("#er").remove();
                frm.fadeOut(400);
                console.log(data['result']);
                setTimeout(
                    function () {
                        $("#suc").addClass("success");
                        $("#suc").html(data['result']);
                    }, 440);

                frm[0].reset();
            }
        },
        error: function (data) {
            console.log("err");
            $("#er").html("Something went wrong!");
            frm[0].reset();
        }
    });
    return false;
});