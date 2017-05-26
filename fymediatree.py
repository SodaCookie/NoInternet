"""Defines the decision tree for FY media"""

fymediatree = {}

fymediatree["main"] = {
    "message" : [
        "Welcome to FYMedia. A Reseller of CUX Cable.",
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
        "Thank you for choosing FYMedia. We will get back to you shortly confirming the date of your install via email!",
        "1. Hang up the phone."
    ],
    "choices" : (
        ("exit", "It looks like this might be pretty easy."),
    ),
    "flag" : ("setup", 3)
}
