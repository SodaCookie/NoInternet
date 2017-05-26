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
