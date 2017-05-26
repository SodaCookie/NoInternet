neighbour_norm_tree = {}

neighbour_norm_tree["main"] = {
    "message" : [
        "Hello? Who is this?",
        "1. Ask about borrowing internet.",
        "2. And his name is John Cena!",
        "3. ..."
    ],
    "choices" : (
        ("internet", "You explain that you have no internet and that you are looking to get it installed soon."),
        ("annoyed", "*Airhorns* *Airhorns* *Airhorns*"),
        ("hangup", "You are at odds about what to ")
    )
}

neighbour_norm_tree["annoyed"] = {
    "message" : [
        "Look dude, I don't know what your beef is, but I'm gonna hang up the phone now.",
        "1. Hang up the phone"
    ],
    "choices" : (
        ("exit", "You hang up the phone and think hard about yourself as a person."),
    ),
    "flag" : "annoyed"
}

neighbour_norm_tree["hangup"] = {
    "message" : [
        "The line goes dead.",
        "1. Hang up the phone"
    ],
    "choices" : (
        ("exit", "Maybe you should have said something else."),
    )
}

neighbour_norm_tree["internet"] = {
    "message" : [
        "Yeah! You can borrow the internet over the wifi there's a guest network already setup that you can connect to right now, 'PrettyFlyForAWifi'. The password is my name, John Cenan.",
        "1. Thank the neighbour for his time."
    ],
    "choices" : (
        ("exit", "You immediately try to access the internet and you connect. Albeit the internet the signal is a bit weak."),
    ),
    "flag" : "partial"
}
