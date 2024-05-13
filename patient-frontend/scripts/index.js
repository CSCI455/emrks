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

function submitLogin(){
    const ssn = document.getElementById("username").value
    const ssnRe = new RegExp(String.raw`^(\d{9}|\d{3}-\d{2}-\d{4})$`)
    if (!ssnRe.test(ssn)){
        alert("Malformed SSN (" + ssn + ")! Please check input.")
        return
    }

    const pass = document.getElementById("password").value

    if (pass === ""){
        alert("Please enter a password!")
        return
    }

    const savePw = document.getElementById("rememberme").checked

    sendMessage({
        sentinel: "hello world"
    }, "/auth/verifyAuth", ssn, pass)
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
        if (trueResponse.passed){
            setPass(ssn, pass, savePw)
            window.location.href = "/";
        } else {
            alert("Login Failed. Please check username and password.")
        }
    })
    .catch(function (err) {
        console.log(err)
        alert("Sorry, there appears to be an issue on our end. Please try again later.")
    })
}

window.addEventListener('load', function () {
    validateKeys().then(function(){
        return canAuthenticate()
    }).then(function(authable){
        if (authable){
            window.location.href = "/home.html"
        } else {
            if (canRemoveLoader()){
                document.getElementById("screenfill").style["display"] = "none";
            }
        }
    })
    const submitButton = document.getElementById("submitlogin");
    submitButton.addEventListener("click", submitLogin);
})