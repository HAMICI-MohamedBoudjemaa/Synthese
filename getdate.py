# -*- coding: utf-8 -*-
import datefinder


text = '14 mai 1610. Le Mans du roi Henri IV est bloqué rue de la Ferronnerie, à Paris, par une charrette de foin. Ravaillac en profite pour monter sur une des roues et poignarde le roi !Ravaillac sera torturé, écartelé, brûlé, et ses cendres jetées au vent.'

matches = datefinder.find_dates(text)

for match in matches:
    print match

