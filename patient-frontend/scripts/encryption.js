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

const serverURL = "/api"
var keysLoaded = false

async function setCookie(cname, cvalue, exdays) {
    // No longer using cookies. Using localstorage now.
    /*
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/;samesite=lax";
    */
    window.localStorage.setItem(cname, cvalue);
    return awaitCookie(cname).then(function(){
        return getCookie(cname)
    })
}

function getCookie(cname) {
    // No longer using cookies. Using localstorage now.
    /*
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
    */

    const val = window.localStorage.getItem(cname);
    if (val === null){
        return ""
    } else {
        return val
    }
}

async function awaitCookie(cname){
    while (getCookie(cname) == ""){
        await new Promise(r => setTimeout(r, 100))
    }
    return getCookie(cname)
}

function setPass(user, pass, savePass){
    if (savePass){
        setCookie("user", user, 0)
        .then(function(){
            setCookie("pass", pass, 0)
        })
        .then(function(){
            ;
        })
    }

    sessionStorage.setItem("user", user);
    sessionStorage.setItem("pass", pass);
    return new Promise(r => setTimeout(r, 100))
    .then(function(){
        return true
    })


}

function checkPassSaved(){
    if (!(getCookie("user") === "") && !(getCookie("pass") === "")){
        sessionStorage.setItem("user", getCookie("user"))
        sessionStorage.setItem("pass", getCookie("pass"))
    }
    user = sessionStorage.getItem("user");
    pass = sessionStorage.getItem("pass");

    if (user === null || pass === null){
        return false
    }

    return true
}

function getPass(){
    return [getCookie("user"), getCookie("pass")]
}

function invalidatePass(){
    localStorage.removeItem("user");
    localStorage.removeItem("pass");
}

function canAuthenticate(){
    if (!checkPassSaved()){
        return false
    }

    bundle = getPass();
    const user = bundle[0];
    const pass = bundle[1];

    return sendMessage({
        sentinel: "hello world"
    }, "/auth/verifyAuth", user, pass)
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
            return true
        } else {
            invalidatePass();
            return false
        }
    })
    .catch(function (err) {
        console.log(err)
        return false
    })
}

function spkiToPEM(keydata) {
    var keydataS = arrayBufferToString(keydata);
    var keydataB64 = window.btoa(keydataS);
    var keydataB64Pem = formatAsPem(keydataB64);
    return keydataB64Pem;
}

function arrayBufferToString(buffer) {
    var binary = '';
    var bytes = new Uint8Array(buffer);
    var len = bytes.byteLength;
    for (var i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return binary;
}

function stringToArrayBuffer(str) {
    var buf = new ArrayBuffer(str.length * 2); // 2 bytes for each char
    var bufView = new Uint8Array(buf);
    for (var i = 0, strLen = str.length; i < strLen; i++) {
        bufView[i] = str.charCodeAt(i);
    }
    return buf;
}

function formatAsPem(str) {
    var finalString = '-----BEGIN PUBLIC KEY-----\n';

    while (str.length > 0) {
        finalString += str.substring(0, 64) + '\n';
        str = str.substring(64);
    }

    finalString = finalString + "-----END PUBLIC KEY-----";

    return finalString;
}

function manufactureLogin() {
    var html = `<div class="logincontainer">
            <h2 class="loginheader">Authentication Required!</h2>
            <label class="loginitemlabel" for="uname"><b>Username</b></label>
            <input class="loginitem" type="text" placeholder="Enter Username" name="uname" required>
            <label class="loginitemlabel" for="psw"><b>Password</b></label>
            <input class="loginitem" type="password" placeholder="Enter Password" name="psw" required>
            <label class="rememberme">
                <input type="checkbox" checked="checked" name="remember"> Remember me
            </label>
            <button class="loginbutton" type="submit"><span>Login</span><span>&#8618;</span></button>
        </div>`;
    return html
}

async function importClientPrivKey() {
    return window.crypto.subtle.importKey(
        "jwk", //can be "jwk" (public or private), "spki" (public only), or "pkcs8" (private only)
        JSON.parse(getCookie("clientPrivKey")),
        {   //these are the algorithm options
            name: "RSA-OAEP",
            hash: { name: "SHA-1" }, //can be "SHA-1", "SHA-256", "SHA-384", or "SHA-512"
        },
        true, //whether the key is extractable (i.e. can be used in exportKey)
        ["decrypt"] //"encrypt" or "wrapKey" for public key import or
        //"decrypt" or "unwrapKey" for private key imports
    )
}


async function importClientPubKey() {
    return window.crypto.subtle.importKey(
        "jwk", //can be "jwk" (public or private), "spki" (public only), or "pkcs8" (private only)
        JSON.parse(getCookie("clientPubKey")),
        {   //these are the algorithm options
            name: "RSA-OAEP",
            hash: { name: "SHA-1" }, //can be "SHA-1", "SHA-256", "SHA-384", or "SHA-512"
        },
        true, //whether the key is extractable (i.e. can be used in exportKey)
        ["encrypt"] //"encrypt" or "wrapKey" for public key import or
        //"decrypt" or "unwrapKey" for private key imports
    )
}

async function exportClientPubKey() {
    return importClientPubKey().then(function (key) {
        //returns a publicKey (or privateKey if you are importing a private key)
        return window.crypto.subtle.exportKey("spki", key);
    }).then(function (spki) {
        return spkiToPEM(spki)
    })

}

async function encryptMessage(msg, key) {
    return window.crypto.subtle.encrypt(
        {
            name: "RSA-OAEP",
            //label: Uint8Array([...]) //optional
        },
        key, //from generateKey or importKey above
        msg //ArrayBuffer of data you want to encrypt
    );
}

async function decryptMessage(msg) {
    return importClientPrivKey().then(function (key) {
        //returns a publicKey (or privateKey if you are importing a private key)
        return window.crypto.subtle.decrypt(
            {
                name: "RSA-OAEP"
            },
            key,
            msg,
        )
    })
        .then(function (msg) {
            var stopAt = new Uint8Array(msg).indexOf(0)
            if (stopAt == -1) {
                return arrayBufferToString(msg)
            } else {
                var clippedArray = new Uint8Array(msg).slice(0, stopAt)
                return arrayBufferToString(clippedArray)
            }
        })
        .catch(function (err) {
            console.error(err);
        });
}

function genKeys() {
    console.log("Generating client keys...")

    let keyPair =
        window.crypto.subtle.generateKey(
            {
                name: "RSA-OAEP",
                // Consider using a 4096-bit key for systems that require long-term security
                modulusLength: 4096,
                publicExponent: new Uint8Array([1, 0, 1]),
                hash: "SHA-1",
            },
            true,
            ["encrypt", "decrypt"]
        )

    return keyPair.then(function(key){
        // Export privkey
        window.crypto.subtle.exportKey(
            "jwk",
            key.privateKey
        )
        .then(function (keydata) {
            // Set cookie
            return setCookie("clientPrivKey", JSON.stringify(keydata), 1)
        })
        .then(function(){
            return awaitCookie("clientPrivKey")
        })
        .then(function(){
            window.crypto.subtle.exportKey(
                "jwk",
                key.publicKey
            )
            .then(function (keydata) {
                // Set cookie
                return setCookie("clientPubKey", JSON.stringify(keydata), 1)
            })
            .then(function(){
                return awaitCookie("clientPubKey")
            })
            .then(function(){
                console.log("keys stored.")
                return new Promise(r => setTimeout(r, 100))
            })
            .then(function(){
                console.log("timeout complete")
                window.location.reload();
            })
        })
        .then(function(){
            return 0
        })
    
        .catch(function (err) {
            alert(err);
        });
    });
    console.log("Client keys generated and stored to cookies.")
}

async function chunkDecMessage(messageArray) {
    // If the message exceeds 216 bytes, RSA encryption fails.
    // We should thus chunk the message.
    numBlocks = messageArray.length
    outputBlocks = new Array(numBlocks)

    for (let i = 0; i < numBlocks; i++) {
        await decryptMessage(new Uint8Array(stringToArrayBuffer(atob(messageArray[i]))).slice(0, 512))
            .then(function (decBlock) {
                outputBlocks[i] = decBlock
            })
    }

    return outputBlocks.join("")
}

async function chunkEncMessage(messageArray, key) {
    // If the message exceeds 216 bytes, RSA encryption fails.
    // We should thus chunk the message.
    numBlocks = Math.floor(messageArray.byteLength / 216) + 1
    writtenBlocks = new Array(numBlocks - 1)

    for (let i = 0; i < numBlocks - 1; i++) {
        await encryptMessage(new Uint8Array(messageArray.slice(i * 216, (i + 1) * 216)), key)
            .then(function (encBlock) {
                writtenBlocks[i] = btoa(String.fromCharCode.apply(null, new Uint8Array(encBlock)));
            })
    }

    await encryptMessage(messageArray.slice(numBlocks * 216, messageArray.length), key)
        .then(function (encBlock) {
            writtenBlocks[numBlocks - 1] = btoa(String.fromCharCode.apply(null, new Uint8Array(encBlock)));
        })

    return writtenBlocks
}

function canRemoveLoader(){
    return keysLoaded;
}

async function validateKeys() {
    const chunkValidationMsg = `Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.`

    if (getCookie("clientPrivKey") == "" || getCookie("clientPubKey") == "") {
        genKeys().then(function(){
            //window.location.reload();
        })
    } else {

        console.log("[VAL] Loading key and running self-test.")

        exportClientPubKey().then(function (pubKeyText) {
            console.log("[VAL_PUBKEY_EXP] Result of pubkey export test:")
            console.log("[VAL_PUBKEY_EXP]\n" + pubKeyText)
        })

        absolutelyDoNotDisplayContents = false;
        const testMessage = "Hello RSA!"
        console.log("[VAL_ENC_DEC] Test of sample message encryption:")
        console.log("[VAL_ENC_DEC] Input text: " + testMessage)

        return importClientPubKey().then(function (key) {
            keysLoaded = true;
            return encryptMessage(stringToArrayBuffer(testMessage), key)
        })
            .then(function (encMsg) {
                console.log("[VAL_ENC_DEC] Encrypted message: " + arrayBufferToString(encMsg))
                return decryptMessage(encMsg)
            })
            .then(function (decMsg) {
                console.log("[VAL_ENC_DEC] Decrypted message: " + decMsg)
                if (decMsg == testMessage) {
                    console.log("[VAL_ENC_DEC] Test passed!")
                    return true
                } else {
                    throw new error("[VAL_ENC_DEC] Test failed!")
                }
            })
            .catch(function (err) {
                alert("Sorry, there appears to be an issue with your session keys. Please clear your browser cookies and try again.")
            })
        /*
        return sendMessage(chunkValidationMsg, "/auth/echoobsc", "000000000", "testpass")
            .then(function (resp) {
                return resp.json()
            })
            .then(function (responseJSON) {
                return chunkDecMessage(responseJSON)
            })
            .then(function (clearText) {
                console.log(clearText)
                msg = stringToArrayBuffer(clearText)
                var stopAt = new Uint8Array(msg).indexOf(0)
                var clippedArray = new Uint8Array(msg).slice(0, stopAt)
                console.log(arrayBufferToString(clippedArray))
                return JSON.parse(arrayBufferToString(clippedArray)).message
            })
            .then(function (clearText) {
                if (clearText.localeCompare(chunkValidationMsg) == 0) {
                    console.log("Working")
                } else {
                    console.log("Not working")
                    console.log(clearText)
                    console.log(chunkValidationMsg)
                }
            })*/
        
    }
}

async function sendMessage(message, url, username, password) {
    clientPubKey = await exportClientPubKey()
    serverPubKey = await getServerPubkey()
    messageChunks = await chunkEncMessage(
        stringToArrayBuffer(
            JSON.stringify({
                password: password,
                message: message,
                pubkey: clientPubKey
            })
        ), serverPubKey
    )

    return fetch(serverURL + url, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
            timestamp: "Hello from JS!",
            user: username,
            content: messageChunks
        }),
    })
}

function makeRequest(opts) {
    return new Promise(function (resolve, reject) {
        var xhr = new XMLHttpRequest();
        xhr.open(opts.method, opts.url);
        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                resolve(xhr.response);
            } else {
                reject({
                    status: xhr.status,
                    statusText: xhr.statusText
                });
            }
        };
        xhr.onerror = function () {
            reject({
                status: xhr.status,
                statusText: xhr.statusText
            });
        };
        if (opts.headers) {
            Object.keys(opts.headers).forEach(function (key) {
                xhr.setRequestHeader(key, opts.headers[key]);
            });
        }
        var params = opts.params;
        // We'll need to stringify if we've been given an object
        // If we have a string, this is skipped.
        if (params && typeof params === 'object') {
            params = Object.keys(params).map(function (key) {
                return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
            }).join('&');
        }
        xhr.send(params);
    });
}



async function getServerPubkey() {
    return makeRequest({
        method: "GET",
        url: serverURL + "/auth/requestpubkey"
    })
        .then(function (resp) {
            var keyJson = JSON.parse(resp)
            return window.crypto.subtle.importKey(
                "jwk", //can be "jwk" (public or private), "spki" (public only), or "pkcs8" (private only)
                keyJson,
                {   //these are the algorithm options
                    name: "RSA-OAEP",
                    hash: { name: "SHA-1" }, //can be "SHA-1", "SHA-256", "SHA-384", or "SHA-512"
                },
                false, //whether the key is extractable (i.e. can be used in exportKey)
                ["encrypt"] //"encrypt" or "wrapKey" for public key import or
                //"decrypt" or "unwrapKey" for private key imports
            )
        })
}
