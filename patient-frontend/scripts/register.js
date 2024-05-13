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

function submitRegistration(){
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

    const ssn = document.getElementById("ssn").value
    const ssnRe = new RegExp(String.raw`^(\d{9}|\d{3}-\d{2}-\d{4})$`)
    if (!ssnRe.test(ssn)){
        alert("Malformed SSN (" + ssn + ")! Please check input.")
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
    if (ccname === ""){
        alert("Please enter a cardholder name!")
        return
    }
    const ccnum = document.getElementById("ccnum").value
    const ccnumRe = new RegExp(String.raw`^(\d{16}|(\d{4}-){3}\d{4})$`)
    if (!ccnumRe.test(ccnum)){
        alert("Malformed credit card number (" + ccnum + ")! Please check input.")
        return
    }

    const ccexp = document.getElementById("ccexp").value
    const ccexpRe = new RegExp(String.raw`^(\d{2}(-|/)\d{2}|\d{2}(-|/)\d{4})$`)
    if (!ccexpRe.test(ccexp)){
        alert("Malformed credit card expiration month (" + ccexp + ")! Please check input.")
        return
    }

    const cccvv = document.getElementById("cccvv").value
    const cccvvRe = new RegExp(String.raw`^\d{3}$`)
    if (!cccvvRe.test(cccvv)){
        alert("Malformed CVV (" + cccvv + ")! Please check input.")
        return
    }

    const pass = document.getElementById("pass").value
    const conpass = document.getElementById("conpass").value

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

    sendMessage({
        FName: fname,
        LName: lname,
        SSN: ssn,
        Email: email,
        PhoneNo: phone,
        CredCardNo: ccnum,
        CVV: cccvv,
        ExpDate: ccexp,
        CredCardName: ccname,
        Password: pass
    }, "/register", "000000000", "temp")
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
        console.log(trueResponse)
        if (trueResponse.registered){
            alert("You have successfully registered :3")
            window.location.href = "/";
        } else {
            alert("Your registration was denied for reason: " + trueResponse.reason)
        }
    })
    .catch(function (err) {
        console.log(err)
        alert("Sorry, there appears to be an issue on our end. Please try again later.")
    })
}

window.addEventListener('load', function () {
    validateKeys().then(function(){
        document.getElementById("screenfill").style["display"] = "none";
    })
    const submitButton = document.getElementById("submitreg");
    submitButton.addEventListener("click", submitRegistration);
})