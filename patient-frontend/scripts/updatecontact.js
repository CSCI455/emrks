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

var currentDetailsGlobal;

function submitUpdate(){
    const fname = document.getElementById("fname").value
    if (fname === ""){
        alert("Please enter a first name!")
        return
    }

    const lname = document.getElementById("lname").value
    if (lname === ""){
        alert("Please enter a last name!")
        return
    }

    const email = document.getElementById("email").value
    if (email === ""){
        alert("Please enter an email!")
        return
    }

    const phone = document.getElementById("phone").value
    const phoneRe = new RegExp(String.raw`^(\d{10}|\d{3}-\d{3}-\d{4})$`)
    if (!phoneRe.test(phone)){
        alert("Malformed phone number (" + phone + ")! Please check input.")
        return
    }

    const ccname = document.getElementById("ccname").value
    const ccnum = document.getElementById("ccnum").value
    const ccexp = document.getElementById("ccexp").value
    const cccvv = document.getElementById("cccvv").value

    updatingCard = true
    if (!(ccname + ccnum + ccexp + cccvv === "")){
        if (ccname === ""){
            alert("Please enter a cardholder name!")
            return
        }
        const ccnumRe = new RegExp(String.raw`^(\d{16}|(\d{4}-){3}\d{4})$`)
        if (!ccnumRe.test(ccnum)){
            alert("Malformed credit card number (" + ccnum + ")! Please check input.")
            return
        }
        const ccexpRe = new RegExp(String.raw`^(\d{2}(-|/)\d{2}|\d{2}(-|/)\d{4})$`)
        if (!ccexpRe.test(ccexp)){
            alert("Malformed credit card expiration month (" + ccexp + ")! Please check input.")
            return
        }
        const cccvvRe = new RegExp(String.raw`^\d{3}$`)
        if (!cccvvRe.test(cccvv)){
            alert("Malformed CVV (" + cccvv + ")! Please check input.")
            return
        }
    } else {
        // Card not updated
        updatingCard = false
    }

    updatingPass = false

    pass = document.getElementById("pass").value
    conpass = document.getElementById("conpass").value

    if (!(pass === "" && conpass === "")){
        if (pass === ""){
            alert("Please enter a password!")
            return
        }
        if (conpass === ""){
            alert("Please confirm your password!")
            return
        }
        if (!(pass === conpass)){
            alert("Passwords don't match!")
            return
        }
        updatingPass = true
    }

    pass = document.getElementById("curpass").value
    bundle = getPass()

    if (bundle[1] === pass){
        bundle = getPass()
        billid = Number(window.location.hash.split("#")[1])
        sendMessage({
            ccupd: updatingCard,
            passupd: updatingPass,
            phone: phone,
            email: email,
            fname: fname,
            lname: lname,
            ccname: ccname,
            ccexp: ccexp,
            cccvv: cccvv,
            ccnum: ccnum,
            pw: conpass
        }, "/updateContact", bundle[0], bundle[1])
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
                window.alert("Your details have been updated.")
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
                sendMessage({
                    sentinel: "Hi! Hiiiiii :333"
                }, "/confirmUpdatable", bundle[0], bundle[1])
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
                        console.log("Contact Updatable")
                        currentDetailsGlobal = trueResponse
                        document.getElementById("fname").value = trueResponse.first
                        document.getElementById("lname").value = trueResponse.last
                        document.getElementById("email").value = trueResponse.email
                        document.getElementById("phone").value = trueResponse.phone
                        document.getElementById("curcard").innerHTML = "Your current card on file ends in <b>" + trueResponse.lastfourcc + "</b>."
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
    const submitButton = document.getElementById("submitupdate");
    submitButton.addEventListener("click", submitUpdate);
})