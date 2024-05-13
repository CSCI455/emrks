/*
CSCI 455 EMRKS Project - Optomet.me Optometry Clinic
Copyright (C) 2024  Julia Dewhurst, Joseph Melancon, Anna Wille, Maya Wyganowska

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

function toggleCurAppt(){
    theTable = document.getElementById("curappt")
    toggleButton = document.getElementById("togglecur")
    toggleSpan = toggleButton.getElementsByTagName('span')[1]

    if (theTable.style["display"] === "none"){
        if (window.screen.width < 800){
            theTable.style["display"] = "block"
        } else {
            theTable.style["display"] = "table"
        }
        toggleSpan.innerHTML = "Hide"
    } else {
        theTable.style["display"] = "none"
        toggleSpan.innerHTML = "Show"
    }
}

function modCon(){
    window.location.href = "/updatecontact.html"
}

// https://stackoverflow.com/a/11381730
window.mobileCheck = function() {
    let check = false;
    (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
    return check;
  };

function callClinic(){
    theDiv = document.getElementById("qrdropdown")
    toggleButton = document.getElementById("book")

    if (window.mobileCheck()){
        window.location.href = "tel:7017773000";
        toggleButton.classList.toggle("highlight");
    } else {
        if (theDiv.style["display"] === "none"){
            theDiv.style["display"] = "block"
        } else {
            theDiv.style["display"] = "none"
        }
    }
}

function togglePrevAppt(){
    theTable = document.getElementById("prevappt")
    toggleButton = document.getElementById("toggleprev")
    toggleSpan = toggleButton.getElementsByTagName('span')[1]

    if (theTable.style["display"] === "none"){
        if (window.screen.width < 800){
            theTable.style["display"] = "block"
        } else {
            theTable.style["display"] = "table"
        }
        toggleSpan.innerHTML = "Hide"
    } else {
        theTable.style["display"] = "none"
        toggleSpan.innerHTML = "Show"
    }
}

function togglePresc(){
    theTable = document.getElementById("presc")
    toggleButton = document.getElementById("togglepresc")
    toggleSpan = toggleButton.getElementsByTagName('span')[1]

    if (theTable.style["display"] === "none"){
        if (window.screen.width < 800){
            theTable.style["display"] = "block"
        } else {
            theTable.style["display"] = "table"
        }
        toggleSpan.innerHTML = "Hide"
    } else {
        theTable.style["display"] = "none"
        toggleSpan.innerHTML = "Show"
    }
}

function logOut(){
    invalidatePass()
    window.location.href = "/"
}

function setPageFromJSON(theJSON){
    console.log(theJSON)
    document.getElementById("helloname").innerHTML = "Welcome, " + theJSON.content.bio.name + "!"
    document.getElementById("phonefile").innerHTML = "Phone on File: <b>" + theJSON.content.bio.phone + "</b>"
    document.getElementById("emailfile").innerHTML = "Email on File: <b>" + theJSON.content.bio.email + "</b>"
    document.getElementById("cardfile").innerHTML = "Payment on File: <b>Credit Card ending in " + theJSON.content.bio.credcard + "</b>"

    curApptTable = document.getElementById("curappt")
    curApptText = curApptTable.innerHTML.split("</tbody>")[0]
    curApptCount = 0
    actionableCount = 0

    theJSON.content.upcoming.forEach(element => {
        elementCopy = element
        action = ""
        if (elementCopy[3] == false && elementCopy[0] === "Scheduled"){
            elementCopy[3] = "<a onclick=\"callClinic()\" href=\"#\">Call to Request Cancellation</a>"
            elementCopy[0] = "🟢 " + elementCopy[0]
        } else if (elementCopy[0] === "Cancelled"){
            elementCopy[3] = "<a onclick=\"callClinic()\" href=\"#\">Call to Request Rebooking</a>"
            elementCopy[0] = "🔴 " + elementCopy[0]
        } else if (elementCopy[0] === "Scheduled"){
            elementCopy[3] = "<a href=\"/cancelappt.html#" + element[1] + "\">Cancel Online</a>"
            elementCopy[0] = "🟢 " + elementCopy[0]
            actionableCount += 1
        } else {
            elementCopy[3] = "<a onclick=\"callClinic()\" href=\"#\">Call to Modify Booking</a>"
            elementCopy[0] = "🟡 " + elementCopy[0]
        }
        
        newRow = "<tr><td>" + elementCopy.join("</td><td>") + "</td></tr>"
        curApptText += newRow
        curApptCount += 1
    });

    curApptText += "</tbody>"
    curApptTable.innerHTML = curApptText

    if (curApptCount == 0){
        document.getElementById("togglecur").remove()
        document.getElementById("curappt").remove()
    } 
    document.getElementById("upcomingcount").innerHTML = "Upcoming Appointment Count: <b>" + curApptCount + "</b>"
    document.getElementById("actionablecount").innerHTML = "Appointments Actionable Online: <b>" + actionableCount + "</b>"

    

    billTable = document.getElementById("prevappt")
    billText = billTable.innerHTML.split("</tbody>")[0]
    curBillCount = 0
    unpaidCount = 0

    theJSON.content.bills.forEach(element => {
        elementCopy = element
        if (elementCopy[4] === "Payment Pending"){
            info = {
                type: "Invoice",
                accesstime: new Date().toLocaleString(),
                billid: element[0],
                date: element[2],
                servrend: "Office Visit",
                cost: element[3],
                paymentstat: "UNPAID"
            }
            printUrl = "/receipt.html#" + encodeURIComponent(JSON.stringify(info))
            elementCopy[4] = "<a href=\"/billpay.html#" + element[0] + "\">Pay Now</a> - <a href=\"/receipt.html#" + printUrl + "\" target=\"_blank\">Print Invoice</a>"
            elementCopy = ["🔴 Unpaid"].concat(elementCopy)
            unpaidCount += 1
        } else {
            info = {
                type: "Receipt",
                accesstime: new Date().toLocaleString(),
                billid: element[0],
                date: element[2],
                servrend: "Office Visit",
                cost: element[3],
                paymentstat: "PAID via " + element[4]
            }
            printUrl = "/receipt.html#" + encodeURIComponent(JSON.stringify(info))
            elementCopy[4] = "<a href=\"/receipt.html#" + printUrl + "\" target=\"_blank\">Print Receipt</a>"
            elementCopy = ["🟢 Paid"].concat(elementCopy)
        }
        
        newRow = "<tr><td>" + elementCopy.join("</td><td>") + "</td></tr>"
        billText += newRow
        curBillCount += 1
    });

    billText += "</tbody>"
    billTable.innerHTML = billText

    if (curBillCount == 0){
        document.getElementById("billentry").remove()
    } else {
        document.getElementById("prevcount").innerHTML = "Previous Appointment Count: <b>" + curBillCount + "</b>"
        document.getElementById("unpaidcount").innerHTML = "Appointments Unpaid: <b>" + unpaidCount + "</b>"
    }


    prescTable = document.getElementById("presc")
    prescText = prescTable.innerHTML.split("</tbody>")[0]
    curPrescCount = 0
    activeCount = 0

    theJSON.content.prescriptions.forEach(element => {
        elementCopy = element
        if (elementCopy[0] === "Active"){
            elementCopy[0] = "🟢 Active"
            activeCount += 1
        } else if (elementCopy[0] === "Future"){
            elementCopy[0] = "🟡 Future"
        } else {
            elementCopy[0] = "🔴 Expired"
        }
        newRow = "<tr><td>" + elementCopy.join("</td><td>") + "</td></tr>"
        prescText += newRow
        curPrescCount += 1
    });

    prescText += "</tbody>"
    prescTable.innerHTML = prescText

    if (curPrescCount == 0){
        document.getElementById("prescentry").remove()
    } else {
        document.getElementById("presccount").innerHTML = "Prescription Count: <b>" + curPrescCount + "</b>"
        document.getElementById("activecount").innerHTML = "Active Prescriptions: <b>" + activeCount + "</b>"
    }

    document.getElementById("screenfill").style["display"] = "none";
}

window.addEventListener('load', function () {
    validateKeys().then(function(){
        return canAuthenticate()
    }).then(function(authable){
        if (authable){
            if (canRemoveLoader()){
                bundle = getPass()
                sendMessage({
                    sentinel: "hello world"
                }, "/homedata", bundle[0], bundle[1])
                .then(function(resp){
                    if (resp.status >= 500){
                        throw new Error('oh no');
                    } else {
                        return resp.json()
                    }
                }).then(function(resp){
                    return chunkDecMessage(resp)
                })
                .then(function(message){
                    trueResponse = JSON.parse(message)
                    if (trueResponse.passed){
                        setPageFromJSON(trueResponse)
                    } else {
                        invalidatePass()
                        window.location.href = "/";
                    }
                })
                .catch(function (err) {
                    console.log(err)
                    //invalidatePass()
                    //alert("Sorry, there appears to be an issue on our end. Please try again later.")
                    //window.location.href = "/";
                })
            }
        } else {
            window.location.href = "/"
        }
    })
    const curApptButton = document.getElementById("togglecur");
    curApptButton.addEventListener("click", toggleCurAppt);

    const modConButton = document.getElementById("modcon");
    modConButton.addEventListener("click", modCon);

    const prevApptButton = document.getElementById("toggleprev");
    prevApptButton.addEventListener("click", togglePrevAppt);

    const prescButton = document.getElementById("togglepresc");
    prescButton.addEventListener("click", togglePresc);

    const logoutButton = document.getElementById("logout");
    logoutButton.addEventListener("click", logOut);

    const bookButton = document.getElementById("book");
    bookButton.addEventListener("click", callClinic);
})