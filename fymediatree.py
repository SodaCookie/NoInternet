"""Defines the decision tree for FY media"""

fymediatree = {}

fymediatree["main"] = {
    "message" : [
        "Thank you for calling FYMedia a reseller of *CUX Cable*. For technical assistance please press 'one'. For booking a technical appointment please press 'two'. For other inquiries please pressure 'three'.",
        "1. Technical assistance",
        "2. Book an appointment",
        "3. Other"
    ],
    "choices" : (
        ("representative", "*BEEP*"),
        ("appointment", "*BOOP*"),
        ("main", "This is not the time to use that.")
    )
}

fymediatree["representative"] = {
    "message" : [
        "Thank you for choosing *FYMedia*. A representative will be here to assist you shortly. For quality insurance, this call will be monitered.",
        "1. Begin the waiting game..."
    ],
    "choices" : (
        ("exit", "You turn on speaker mode."),
    ),
    "flag" : "rep"
}

fymediatree["appointment"] = {
    "message" : [
        "This is an automated system for setting up a technical appointment.",
        "Please select your 3 preferred install dates from the list below:",
        "1. {days + 1} (one day from now)",
        "2. {days + 2} (two days from now)",
        "3. {days + 3} (three days from now)"
    ],
    "choices" : (
        ("block", "A bit optimistic, you choose the soonest date."),
        ("block", "Being the realist, you compromise."),
        ("block", "Realizing that you hold no power, you wait.")
    )
}

fymediatree["block"] = {
    "message" : [
        "Please select your preferred install block...",
        "1. 6am - 12pm",
        "2. 1pm - 12am"
    ],
    "choices" : (
        ("complete", "A bit rushed, you want internet."),
        ("complete", "Waking up is hard, you choose to wait."),
    )
}

fymediatree["complete"] = {
    "message" : [
        "Thank you for choosing FYMedia. We will get back to you shortly confirming the date of your install via *email*!",
        "1. Hang up the phone."
    ],
    "choices" : (
        ("exit", "It looks like this might be pretty easy."),
    ),
    "flag" : "setup1"
}

#=======================================================================
# TODO
fymediareptree = {}

fymediareptree["main"] = {
    "message" : [
        "No one picked up.",
        "1. Hang up the phone."
    ],
    "choices" : (
        ("exit", "RIP"),
    )
}
