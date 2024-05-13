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
function submitPayment(){
    pass = document.getElementById("pass").value
    bundle = getPass()
    if (bundle[1] === pass){
        bundle = getPass()
        caseid = Number(window.location.hash.split("#")[1])
        sendMessage({
            caseid: caseid
        }, "/cancelAppt", bundle[0], bundle[1])
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
                info = {
                    type: "Cancellation",
                    accesstime: new Date().toLocaleString(),
                    billid: "N/A",
                    date: trueResponse.date,
                    servrend: "Office Visit",
                    cost: "$0.00",
                    paymentstat: "CANCELLED"
                }
                printUrl = "/receipt.html#" + encodeURIComponent(JSON.stringify(info))
                window.open(printUrl)
                window.location.href = "/home.html"
                return true;
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
    } else {
        alert("Sorry, that didn't work. Please check your password and try again.")
    }
}
window.addEventListener('load', function () {
    validateKeys().then(function(){
        return canAuthenticate()
    }).then(function(authable){
        if (authable){
            if (canRemoveLoader()){
                bundle = getPass()
                caseid = Number(window.location.hash.split("#")[1])
                sendMessage({
                    caseid: caseid
                }, "/billing/confirmCancellable", bundle[0], bundle[1])
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
                        console.log("Appt Cancellable")
                        document.getElementById("statement").innerHTML = "To cancel appointment with ID <b>" + window.location.hash.split("#")[1] + "</b> on <b>" + trueResponse.date + "</b>, please confirm your password."
                        document.getElementById("screenfill").style["display"] = "none";
                        return true;
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
            window.location.href = "/home.html"
        }
    })
    const submitButton = document.getElementById("submitpayment");
    submitButton.addEventListener("click", submitPayment);
})