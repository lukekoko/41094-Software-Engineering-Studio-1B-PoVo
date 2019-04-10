// Highlight buttons (used as hover event handler)
// usage:  onmouseover="buttonHighlight(this);" onmouseout="buttonUnHighlight(this);"
function buttonHighlight(element) {
    element.getElementsByTagName("input")[0].style.color = "rgba(52,155,229,1)";
    element.style.borderColor = "rgba(52,155,229,1)";

}

function buttonUnhighlight(element) {
    element.getElementsByTagName("input")[0].style.color = "rgba(52,155,229,1)";
    element.style.borderColor = "rgba(52,155,229,1)";

}


// Format current date
function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    return [day, month, year].join('-');
}

function generateDate() {
    var d = new Date();
    d = d.toDateString();
    d = formatDate(d);
    document.getElementById("dateInput").value = d;
}