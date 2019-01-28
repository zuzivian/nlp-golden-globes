from helpers import *


gg2013_categories = [
        "Best Motion Picture - Drama",
        "Best Motion Picture - Musical or Comedy",
        "Best Performance by an Actress in a Motion Picture - Drama",
        "Best Performance by an Actor in a Motion Picture - Drama",
        "Best Performance by an Actress in a Motion Picture - Musical or Comedy",
        "Best Performance by an Actor in a Motion Picture - Musical or Comedy",
        "Best Performance by an Actress in a Supporting Role in any Motion Picture",
        "Best Performance by an Actor in a Supporting Role in any Motion Picture",
        "Best Director - Motion Picture",
        "Best Screenplay - Motion Picture",
        "Best Motion Picture - Animated",
        "Best Motion Picture - Foreign Language",
        "Best Original Score - Motion Picture",
        "Best Original Song - Motion Picture",
        "Best Television Series - Drama"
    ]

gg2015_categories = {
        "Best Motion Picture – Drama",
        "Best Motion Picture – Musical or Comedy",
        "Best Motion Picture – Foreign Language",
        "Best Motion Picture – Animated",
        "Best Director – Motion Picture"
        "Best Actor – Motion Picture Drama",
        "Best Actor – Motion Picture Musical or Comedy",
        "Best Actress – Motion Picture Drama",
        "Best Actress – Motion Picture Musical or Comedy",
        "Best Supporting Actor – Motion Picture",
        "Best Supporting Actress – Motion Picture",
        "Best Screenplay – Motion Picture",
        "Best Original Score – Motion Picture",
        "Best Original Song – Motion Picture",
        "Cecil B. DeMille Award for Lifetime Achievement in Motion Pictures",
        "Best Television Series – Drama",
        "Best Television Series – Musical or Comedy",
        "Best Miniseries or Television Film",
        "Best Actor – Television Series Drama",
        "Best Actor – Television Series Musical or Comedy",
        "Best Actor – Miniseries or Television Film",
        "Best Actress – Television Series Drama",
        "Best Actress – Television Series Musical or Comedy",
        "Best Actress – Miniseries or Television Film",
        "Best Supporting Actor – Series, Miniseries or Television Film",
        "Best Supporting Actress – Series, Miniseries or Television Film",
        "Best Documentary Film",
        "Best English-Language Foreign Film",
        "New Star of the Year – Actor",
        "New Star of the Year – Actress",
        "Henrietta Award (World Film Favorite – Female)",
        "Henrietta Award (World Film Favorite – Male)",
        "Best Film Promoting International Understanding",
        "Golden Globe Award for Best Cinematography",
        }


# award classification
def award_classifier(tweets, award_list):
    return