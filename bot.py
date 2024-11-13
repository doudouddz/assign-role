import discord
from discord.ext import commands
import asyncio

# Define intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Create bot instance with intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Define the tracked invites and their corresponding role IDs
tracked_invites = {
    "PqnqkyYTS4": 1301987217991798894,  # First invite and its role ID
    "ztBApYAz": 1304438452246548551,  # Second invite and its role ID
}

# Cache invites when the bot starts
invites_cache = {}


@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

    # Cache invites for all guilds the bot is in
    for guild in bot.guilds:
        invites = await guild.invites()
        invites_cache[guild.id] = {
            invite.code: invite.uses
            for invite in invites
        }


@bot.event
async def on_member_join(member):
    # Get the updated list of invites for the guild
    new_invites = await member.guild.invites()

    # Identify which invite was used
    used_invite = None
    for invite in new_invites:
        old_uses = invites_cache.get(member.guild.id, {}).get(invite.code, 0)
        if invite.uses > old_uses:
            used_invite = invite
            break

    # Update the invite cache
    invites_cache[member.guild.id] = {
        invite.code: invite.uses
        for invite in new_invites
    }

    # Check if the used invite is in the tracked invites
    if used_invite and used_invite.code in tracked_invites:
        role_id = tracked_invites[used_invite.code]
        role = discord.utils.get(member.guild.roles, id=role_id)
        if role:
            try:
                await member.add_roles(role)
                print(
                    f"Assigned role to {member.name} based on invite {used_invite.code}"
                )
            except Exception as e:
                print(f"Error assigning role: {e}")
        else:
            print(f"Role with ID {role_id} not found!")
    else:
        print(
            f"Used invite detected: {used_invite.code if used_invite else 'None'}"
        )


@bot.event
async def on_error(event, *args, **kwargs):
    print(f"An error occurred: {event}")


# Run the Discord bot
async def start_bot():
    await bot.start(
        "MTMwNDUxMjE2MDY1NDk1NDU0OA.Gzp5Fy.7Ug62NCAzcxRTN1VC4XE_dicPtMiN8NeHo11-0"
    )


# Run the bot in the main event loop
asyncio.run(start_bot())
