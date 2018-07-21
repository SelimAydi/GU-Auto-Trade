console.log(formlist);
var formlist = "<input type='file' name='invoice' class='invis' required='' id='id_invoice'>";
var row = document.getElementById("tr1");
var old = row.innerHTML;
var oldrow = "";
var xow = [];
var orderstb = document.getElementById('orderstable')
var frmitem = ""
function updateCells(rownum, orderid){
    $('.editbutton').hide();
    oldrow = document.getElementById(rownum).innerHTML;
    xow[rownum] = document.getElementById(rownum).innerHTML;
    var roww = document.getElementById(rownum);
    for (var i = 2; i < roww.cells.length; i++){
        var curr = roww.cells[i].innerHTML;
        console.log("am looping")
        if (curr === '<i class="fas fa-check"></i>'){
            var field = "<input id='check" + i + "x' type='hidden' value='True' name='check" + i + "x'/><input id='check" + i + "' type='checkbox' onchange='updateCheckbox(this)' name='check"+ i + "' value='True' checked />"
            console.log("IS CHECKED")
        } else if (curr === '<i class="fas fa-times"></i>') {
            var field = "<input id='check" + i + "x' type='hidden' value='False' name='check" + i + "x'/><input id='check" + i + "' name='check" + i + "' onchange='updateCheckbox(this)' type='checkbox' value='False' />"
        } else {
            if (i !== 5){
                if (i !== 2 && i !== 11) {
                    var field = "<input name='inp" + i + "' type='text' value='" + curr + "' />"
                } else {
                    var field = roww.cells[i].innerHTML
                }
            } else {
                var field = roww.cells[i].innerHTML
            }
        }
        roww.cells[i].innerHTML = field;
    }

    roww.cells[0].innerHTML = roww.cells[0].innerHTML + "<button onclick=cancelPost('" + String(rownum) + "') class='main-button'>Cancel</button>";
    roww.cells[roww.cells.length - 1].innerHTML = "<button type='submit' class='main-button' onclick='savePost()'>Save</button>";
    change.value = orderid;
    roww.cells[roww.cells.length - 2].innerHTML = formlist + "<label id='label1' class='custom-file-upload' for='id_invoice' style='width: 60%;'><i class='fas fa-upload'></i>Choose File</label>"


    var file = document.getElementById("id_invoice");
    var idClicked = "";

    $("label").click(function(e) {
        idClicked = e.target.id;
        console.log(idClicked);
    });

    file.onchange = function() {
        console.log("CHANGED FILE");
        console.log(file.files[0].name);
        if(idClicked){
            $('#' + idClicked).removeAttr("for");
            $('#' + idClicked)[0].innerHTML = "<i class='far fa-file'></i>";
            $('#' + idClicked)[0].innerHTML += file.files[0].name;
            // $('#' + idClicked).click(function(){
            //     $('form#orderchange').submit();
            // });
        }
    }

}

function cancelPost(rownum){
    console.log("CANCELLING");
    console.log("ROWNUM: " + rownum);
    document.getElementById(rownum).innerHTML = xow[rownum];

    document.getElementsByClassName("container")[1].style.width = "1170px";
    $('.editbutton').show();
}

function savePost(){
    if ($(element).is(":hidden")){
        $('.editbutton').hide();
    }
    for(var i = 3; i <= 21; i = i + 2){
        console.log(String(row.childNodes[i].childNodes[0].value))
    }
}

function updateCheckbox(obj){
    console.log(obj);
    console.log(obj.name + "x");
    hidden = document.getElementById(obj.name + "x");
    if (obj.checked){
        //console.log(obj.name + "x")
        obj.value = "True";
        hidden.value = "True"
    } else {
        obj.value = "False";
        hidden.value = "False"
    }
}



function updateButton(buttonid){
    $('#' + buttonid)[0].innerHTML = "<i class='fas fa-upload'></i>Upload";
}