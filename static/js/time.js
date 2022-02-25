function createImg3(){
    var option = document.getElementsByClassName("time")
    var optionVal=""

    for (var i=0 ; i<option.length ; i++){
        if (option[i].selected){
            optionVal=option[i].value
        }
    }

    var img = document.createElement("img")
    img.setAttribute("src",optionVal)

    var div = document.getElementById("imgview3")
    var chd = document.querySelector("#imgview3 > img")
    div.replaceChild(img,chd)
}