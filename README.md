# BSBot

## Features (Callable methods)
1. [Administration](#administration)
2. [Music](#music)
3. [Economy](#economy)
4. [Gambling Minigame](#gambling)
5. [Speak](#speak)



### administration
    - addmuted (not callable)
        - checks for "muted" role and adds it if it's not there
    - !addrole(member, role)
        - Role requirements:
          admin, moderator
        - Assigns a specific member a role.
        - Maybe add a role called '!verify' that only gives the 'friend' role
    - !mute(member, mute_time: int, reason)
        - (addmuted function required)
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

### music
    - !join
        - Role requirements:
          anyone
        - Joins the invoking member's current voice channel.
    - !summon(channel)
        - Role requirements:
          should be (admin, moderator)
        - Summons the bot to a voice channel.
        If no channel was specified, it joins your channel.
    - !leave
        - Role requiresments:
          manage_guild = manage server i guess?
        - Clears queue and leaves channel
    - !volume(volume: int)
        - Role requirements:
          none
        - Sets the volume based on int (0-100)
    - !now or !current, !playing
        - Role requirements:
          none
        - Displays the currently playing song + creates embed
    - !pause
        - Role requirements:
          manage_guild
        - Pauses the song and adds play/pause emoji reaction to your message
    - !resume
        - Role requirements:
          manage_guild
        - Resumes currently playing song and adds play/pause emoji reaction to your message
    - !stop
        - Role requirements:
          manage_guild
        - Stop playing song and clears queue, adds Stop emoji reaction to your message
    - !skip
        - Role requirements:
          can skip without vote if you requested the song playing
        - initializes a vote to skip
        - if you're the person who requested the song, you can auto-skip
    - !queue(page: int=1)
        - Role requirements:
          none
        - Show's the player's queue, with the ability to specify the number of pages you want to show
    - !shuffle
        - Role requirements:
          none
        - Confirms queue has been shuffled with the green_check emoji reaction
    - !remove(index: int)
        - Role requirements:
          none
        - removes the song at specified position in queue (starting from 1)
    - !loop
        - Role requirements:
          none
        - loops song, invoke again to unlooop
        - adds green_check emoji as confirmation
    - !play(search: str)
        - Role requirements:
          none (maybe should change this)
        - can either take a URL, or searches various sites if no URL is given

### economy
    - !on_join
    - !on_message
    - !balance
    - !xbalance(member)
    - !pay(member, amount: int)
    - !charge(member, amount: int)
    
    Non-callable methods:
    - !update_balance

### gambling
    - !roll(num_dice: int, num_sides: int)
    - !bet_npc(amount: int)

### speak
    - !speak