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

const facts = [
    "Eyeballs contain roughly 70% of all sensing receptors in one's body",
    "Roughly 2.4 million eye injuries occur yearly within the United States",
    "With only 2% of people having them, green eyes are the rarest color of eyes",
    "Doctors still don't know how to transplant eyeballs, wear safety glasses",
    "Brown is the most prevalent eye color; 41% of people have them",
    "Over 150 million Americans rely on corrective lenses",
    "If the human eye was a digital camera, it would have 576 megapixels",
    "In the right conditions and lighting, humans can see the light of a candle from 14 miles away"
]

window.addEventListener('load', function () {
    validateKeys()
    const factholder = document.getElementById("factholder");
    const random = Math.floor(Math.random() * facts.length);
    factholder.innerHTML = "Optometry Fact: " + facts[random] + "!";
})