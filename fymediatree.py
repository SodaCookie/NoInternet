"""Defines the decision tree for FY media"""

fymediatree = {}

fymediatree["main"] = {
    "message" : [
        "Welcome to FYMedia. A Reseller of CUX Cable.",
        "Please select your 3 preferred install dates from the list below:",
        "1 -> {day + 10}",
        "2 -> {day + 11}",
        "3 -> {day + 12}"
    ],
    "choices" : ["block", "block", "block"]
}

fymediatree["block"] = {
    "message" = [
        "Please select your preferred install block...",
        "1 -> 6am - 12pm",
        "2 -> 1pm - 12am"
    ],
    "choices" = ["complete", "complete"]
}

fymediatree["complete"] = {
    "message" = [
        "Thank you for choosing FYMedia. We will get back to you shortly confirming the date of your install!"
    ],
    "choices" = []
}

#--Time passes--
"Your install date has been confirmed for {day + 12} from {1pm - 12am}. A CUX representative will come to install. Have a nice day!"
