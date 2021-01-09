This project is a bot for League of Legends (LoL), a competitive MOBA video game. The bot is designed for Yuumi (a LoL character) playing the support role. It is fully functioning in Season 10 of LoL.

In LOL each champion has four abilites; Q, W, E, and R. I will go into detail as to what each of Yuumi's abilities does and how we (another student and me) managed to go about having the bot use the abilities properly.

W:
The first ability that we worked on was Yuumi's W. This ability allows Yuumi to attach to an ally champion during which she cannot move or be damaged until she either detaches, that ally recalls or dies. In LOL the map is split into three lanes with one person going into the top lane, one person in the mid lane, two people in the bottom lane and one person who is in the jungle where they frequently interact with all three lanes. Yuumi is typically a support champion going bot lane with another champion which is how we coded the bot which is why the bot by default attaches to the bot laner on Yuumi's team. If the bot laner dies she will try to recall if it is before 15 minutes or if that isn't the case, she will attach to the next best ally in order of priority: Jungler, Mid, Top.  Yuumi will also detach from allies after 20 minutes if another ally is low on hp so that she can use her E to heal them and once that ally is healed she will return to the highest priority available champion.

E:
Yuumi's E is a heal that can be used on an ally so long as she's attached to them. The Yuumi bot automatically calculates how much her E will heal for based on her current items and level to determine if she should or shouldn't heal her ally that she is attached to at the moment. If the ally is below 60% hp she will heal her ally even if it heals more than necessary and isn't being used to its fullest potential.

R:
Yuumi's R is a skillshot that fires 7 shots that does AP damage and if the enemy is hit by it 3 times they are rooted. The Yuumi bot will use R when their ally that they are attached to has lost a given percentage of hp in a given time to try to figure out if their ally is being bursted and thus the enemy must be close range. Her R is automatically aimed towards the enemy's nexus.

Q:
Yuumi's Q fires a beam that can be controlled with the mouse as it is in the air. This is the one ability that we have yet to complete the usage of because of its complexity. This ability will require Yuumi to be able to track the enemy's movement in real time as well as track any other objects that could block the Q like enemy minions or other enemy champions.

In terms of items Yuumi buys the same items every game in the same order and buys items whenever her ally recalls or she recalls and has enough gold to buy the next component.

Thus far, the Yuumi bot currently plays at a Silver 4 level. This is as good or better than 34% of all ranked players in North America.
