# BSBot

## Features (Callable methods)
1. [Administration](#administration)
    - !addrole(member, role)
        - Role requirements:
          admin, moderator
        - Assigns a specific member a role.
        - Maybe add a role called '!verify' that only gives the 'friend' role
    - !mute(member, mute_time: int, reason)
        - Role requirements:
          admin, moderator
        - Mutes a specific member, for an amount of seconds. Can optionally give a reason.
        Can only be used by admins and moderators.

        Also sends a DM with information on the mute; who applied it, for how long
        and what the reason was (if there was one)
        - Uses asyncio to sleep for mute_time
    - !create-channel(channel_name)
        - Role requirements:
          admin
        - Method to create a channel with a specific name.
        Not sure how useful this is, because you can't put it in a category (or inherit permissions)

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