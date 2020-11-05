# BSBot

## Features (Callable methods)
1. [Administration](#administration)
    - !addrole(member, role) 
    - !mute(member, mute_time: int, reason)
    - !create-channel(channel_name)

2. [Music](#music)
    - !join
    - !summon(channel)
    - !leave
    - !volume(volume: int)
    - !now
    - !pause
    - !resume
    - !stop
    - !skip
    - !queue(page: int=1)
    - !shuffle
    - !remove(index: int)
    - !loop
    - !play(search: str)

3. [Economy](#economy)
    - !on_join
    - !on_message
    - !balance
    - !xbalance(member)
    - !pay(member, amount: int)
    - !charge(member, amount: int)

4. [Gambling Minigames](#gambling)
    - !roll(num_dice: int, num_sides: int)
    - !bet_npc(amount: int)

5. [Speak](#speak)
    - !speak