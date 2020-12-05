# E-Health-Python-Project-2020-UCL
<p>Note to Programming:</p>
<ul>
    <li>use tabulate package to print result from DB</li>
    <li>Keep your venv folder out of the reop it takes up a lot of space. If you have any package use pip freeze and export to the reqirement.txt</li>
</ul>
<p>ER Diagram:</p>
<p>https://dbdiagram.io/d/5fca43c99a6c525a03b9cfdb</p>

<p>Feature List:</p>
<p>General</p>
<ul>
    <li>Create SQL DB (Done)</li>
    <li>login system</li>
    <li>save password as encrypted (wrote the hash function)</li>
    <li>encryption of all data stored(wrote the encrypt/decrypt function)<ul>
        <li style="margin-left: 20px;">beware that the use of LIKE, ORDER BY etc. will not work for encrypted attributes</li>
    </ul>
</ul>
<p>admin</p>
<ul>
    <li>&nbsp; view all record<ul>
            <li style="margin-left: 20px;">&nbsp; allow different filters<ul>
                    <li style="margin-left: 40px;">&nbsp; e.g. date, patients, GP</li>
                </ul>
            </li>
        </ul>
    </li>
    <li>deactivate GP (hold in a table?)</li>
    <li>delete GP (Cascade Delete)</li>
    <li>add / edit patient recrd (Cascade Delete)<ul>
            <li style="margin-left: 20px;">edit patiet detail<ul>
                    <li style="margin-left: 40px;">name, phone, email, address, NHS number</li>
                </ul>
            </li>
        </ul>
    </li>
    <li>add / edit doctor detail<ul>
            <li style="margin-left: 20px;">name, phone, staffID</li>
        </ul>
    </li>
</ul>
<p>GP</p>
<ul>
    <li>login</li>
    <li>add availabiity<ul>
            <li style="margin-left: 20px;">store available time slot in half an hour interval</li>
            <li style="margin-left: 20px;">default option to add normal hours for multiple days, week, month etc.</li>
            <li style="margin-left: 20px;">delete avalability&nbsp;</li>
            <li style="margin-left: 20px;">allocation of rooms</li>
        </ul>
    </li>
    <li>allow confirmation of bookings<ul>
            <li style="margin-left: 20px;">confirm of mutiple bookings</li>
        </ul>
    </li>
    <li>add perscription<ul>
            <li style="margin-left: 20px;">calculation of perscription cost nhsfee*number of row in perscription</li>
            <li style="margin-left: 20px;">Allow the doctor to write down instruction using abbreviations, See the Latin abbreviations part in<ul>
                <li style="margin-left: 40px;">https://bnf.nice.org.uk/about/abbreviations-and-symbols.html</li>
             </ul>
        </ul>
    </li>
    <li>book followup appointments</li>
    <li>allow next appiontment</li>
</ul>
<p><br></p>
<p>Patient</p>
<ul>
    <li>&nbsp; register</li>
    <li>&nbsp; login</li>
    <li>&nbsp; book appointments<ul>
            <li style="margin-left: 20px;">ratings for doctor</li>
            <li style="margin-left: 20px;">chose doctor and time</li>
            <li style="margin-left: 20px;">if no preference chose the earliest avaliable time</li>
            <li style="margin-left: 20px;">base on availability</li>
            <li style="margin-left: 20px;">description for appointment:&nbsp;</li>
            <li style="margin-left: 20px;">description of illness: fever, respirotory symptom</li>
        </ul>
    </li>
    <li>cancel appiontment</li>
    <li>allow patient to place a rate appointments</li>
    <li>allow patient review appiontments and perscription, translating the Latin abbreviations to readable form if needed</li>
</ul>

