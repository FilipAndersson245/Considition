# Entry for the Considation constest!

base path = www.theconsidition.se/considition/ironman

#ideas

- other maps than standard does not work with the ath finding algorithm (A*)

- check how long its running straigt and add them up to the speed value and choose speed closed(rounded downwards)
- Add/Subtract value from stream/hills
- Change values of powerups depending on what have happend before and current statuses.

- compute short term best move from all possible combinations to get high index on path with distance of (for example) one tile 
- compute better path taking tile types, streams, hills, weather into account


======

1. Om man kan ta en powerup som gynnar nuläget (terrain), gör det direkt (om man inte har en i inventory)
2. Om man har en powerup som gynnar terrain, använd den (om inte en sån används atm)
3. Försöka kolla kommande väg, väga powerups efter det
4. Om powerups fullt, och ingen gynnsamm för terrain, använd en

5. Om stream inverter används, räkna ut ny path
6. Använd duration misc om inte (om inte används redan)
7. (Använd streams 1 gång om i vatten)

terrain wise:

water:
 - Flippers, 10 turns – Water tiles deduct 25% less movement points

road:
 - Cycletire, 10 turns – Road tiles deduct 25% less movement points

trail:
 - Shoes, 10 turns – Trail tiles deduct 25% less movement points

ingore (atm):
 - ((Umbrella)), 25 turns – Your player is immune to the additional stamina deduction caused by rain tiles
 - ((RemoveCloud)) – Removes rain tiles around your players position. A 10x10 tile area with your player in the middle is cleared of bad weather.
 - InvertStreams

durations misc:
 - Energyboost, 10 turns – You regain 10 more stamina per turn
 - Potion, 5 turns – You gain 50% more movement points
 - StaminaSale, 10 turns – You consume 40% less stamina


RestoreStamina – Instantly sets your players stamina to full