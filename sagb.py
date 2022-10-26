import nextcord
from nextcord.ext import commands
from embed_dialogs import dialogBox
from config import Config, Message

bot = commands.Bot()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.slash_command(description="Post the header message again. Useful for initial set-up or channel wipes.", dm_permission=False,
                   default_member_permissions=8, guild_ids=Config.TEST_GUILD_IDS)
async def headermsg(interaction: nextcord.Interaction):
    guild_name = str(interaction.guild)
    description = f"Hey!\n{Message.HEADERMSG.OPENER}\n\n**{Message.HEADERMSG.QUESTION}**\n\n{Message.HEADERMSG.INSTRUCTION}"
    reply = dialogBox("Info", "Welcome!", description)
    reply.set_image(url="https://media.discordapp.net/attachments/887723918574645331/1034724639085182996/unknown.png")
    await interaction.channel.send(embed=reply)
    await interaction.send("Header message posted and is visible to everyone in the channel.", ephemeral=True)

@bot.slash_command(description="Answer the verification question.", dm_permission=False, guild_ids=Config.TEST_GUILD_IDS)
async def verify(interaction: nextcord.Interaction, answer: str):
    user_reply = None
    log_reply = None
    valid_answers = [line.rstrip().lower() for line in open('valid_answers.txt')]

    # Check if the user is already verified
    user_already_verified = type(interaction.user.get_role(Config.VERIFIED_ROLE_ID)) == nextcord.role.Role
    if user_already_verified:
        user_reply = dialogBox("Info", "Already verified", Message.VERIFY.ALREADY_VERIFIED)

    # Check if the answer was valid
    elif answer.lower() not in valid_answers:
        # Let the user know that the answer was not correct.
        user_reply = dialogBox("Error", "Unrecognised answer", Message.VERIFY.FAILURE)

        # Send a log to the logging channel visible only to moderators.
        log_reply = dialogBox("Warn", f"Incorrect answer entered in #{interaction.channel.name}",
                              f"**{interaction.user}** submitted the answer `{answer}`")
        log_reply.set_thumbnail(interaction.user.display_avatar)
        log_reply.add_field(name="User ID", value=interaction.user.id, inline=False)
        log_reply.add_field(name="Date joined", value=interaction.user.joined_at, inline=False)

    # If the user is not currently verified and they entered the correct answer...
    else:
        # Let the user know that the answer was correct.
        user_reply = dialogBox("Success", "Verified!", Message.VERIFY.SUCCESS)

        # Send a log to the logging channel visible only to moderators.
        log_reply = dialogBox("Success", f"User successfully verified in #{interaction.channel.name}",
                              f"**{interaction.user}** submitted the answer `{answer}`")
        log_reply.set_thumbnail(interaction.user.display_avatar)
        log_reply.add_field(name="User ID", value=interaction.user.id, inline=False)
        log_reply.add_field(name="Date joined", value=interaction.user.joined_at, inline=False)

        # Apply the verified role to the user that invoked the command.
        verified_role = interaction.guild.get_role(Config.VERIFIED_ROLE_ID)
        await interaction.user.add_roles(verified_role)
    
    # Send the stored replies (if they've been set)
    if user_reply is not None:
        await interaction.send(embed=user_reply, ephemeral=True)
    if log_reply is not None:
        await bot.get_channel(Config.LOGGING_CHANNEL_ID).send(embed=log_reply)

@bot.event
async def on_message(message):
    # If the message is from someone else... 
    if message.author == bot.user:
        return
    # ...and it is in the verify channel...
    if message.channel.id != Config.VERIFY_CHANNEL_ID:
        return
    # ...then delete it. Nothing should go there.
    else:
        await message.delete()

token = config.DISCORD_BOT_TOKEN
bot.run(token)