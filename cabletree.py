cable_appointment_1 = {}

cable_appointment_1["main"] = {
    "message" : [
        "You hear a loud knock on the door.",
        "\"Hello? This the *CUX Cable* here to do your cable installation.\"",
        "1. Answer the door."
    ],
    "choices" : (
        ("answer", "You open the door and let the cable guy in."),
    )
}

cable_appointment_1["answer"] = {
    "message" : [
        "The cable guy begins to pace around the *apartment* back and forth for a good 5 minutes. Scratching his head, he asks you, \"where's the cable jack?\"",
        "1. Look for the cable yourself.",
        "2. Tell the guy you don't know",
        "3. Find the building administration"
    ],
    "choices" : (
        ("search", "You get on your hands and kness and begin searching around with the cable guy. After another 5 minutes you admit defeat."),
        ("search", "\"What's a cable jack?\" you tell the cable guy."),
        ("angry", "You go downstairs in search of someone from administration to help you find the cable jack.")
    )
}

cable_appointment_1["search"] = {
    "message" : [
        "The cable guy enters and exits yoru apartment in order to find the location of this cable jack. You know it exists because your landlord promised you that your apartment had cable.",
        "\nFinally after what felt like an eternity the cable guy walks into your apartment and looks out onto the poach pointing to a metal pipe outside your apartment.",
        "\"The cable is in there. Therefore, your cable is probably buried in your wall somewhere here.\"",
        "He points to the corner of your room.",
        "\"I can drill a few holes into the wall to try to find it.\"",
        "1. Drill away",
        "2. Let me ask my landlord first",
        "3. Give me the drill. I'll do it myself",
    ],
    "choices" : (
        ("drill", "What's the worst that can happen. It's just a few holes."),
        ("angry", "You go find the administration for permission."),
        ("self", "Everyone is an idiot. If you want something done right, do it yourself."),
    )
}

cable_appointment_1["angry"] = {
    "message" : [
        "Upon reaching the administrative office, you ask the nice secretary who is in charge of maintance of the building. She pulls out a walkie-talkie and asks for someone named *Rex*.",
        "Sometime later, a giant man comes lumbering into the apartment.",
        "\"What's the problem\"",
        "1. Explain the situation"
    ],
    "choices" : (
        ("destroy", "You explain the situation to *Rex*."),
    )
}

cable_appointment_1["destroy"] = {
    "message" : [
        ""
    ],
    "choices" : (
        
    )
}
