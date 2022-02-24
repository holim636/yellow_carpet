function createImg(){
    var option = document.getElementsByTagName("option")
    var optionVal=""

    for (var i=1 ; i<option.length ; i++){
        if (option[i].selected){
            optionVal=option[i].value
        }
    }

    var img = document.createElement("img")
    img.setAttribute("src",optionVal)

    var div = document.getElementById("imgview")
    var chd = document.querySelector("#imgview > img")
    div.replaceChild(img,chd)
}