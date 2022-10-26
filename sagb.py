import nextcord
from nextcord.ext import commands
from embed_dialogs import dialogBox

TESTING_GUILD_ID = 887723918574645328
VERIFY_CHANNEL_ID = 1034026349435826196
LOGGING_CHANNEL_ID = 1034028449356066866
VERIFIED_ROLE_ID = 1034680496803823707

bot = commands.Bot()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# @bot.slash_command(description="Start a test session.", dm_permission=True,
#                    default_member_permissions=8, guild_ids=[TESTING_GUILD_ID])
# async def testsesh(interaction: nextcord.Interaction):
#     await interaction.user.send("Hey!\nThe moderators at `SERVER` have asked that you answer a question in order to be granted access to the server.\n**Please provide the name of the person who gave you the invite link.**")

@bot.slash_command(description="Answer the verification question.", dm_permission=True, guild_ids=[TESTING_GUILD_ID])
async def verify(interaction: nextcord.Interaction, answer: str):
    valid_answers = [line.rstrip().lower() for line in open('valid_answers.txt')]
    if answer.lower() not in valid_answers:
        # Let the user know that the answer was not correct.
        user_reply = dialogBox("Error", "Incorrect answer", "Hm. It looks like that answer isn't in the list of accepted responses. Please try again.")

        # Send a log to the logging channel visible only to moderators.
        log_reply = dialogBox("Warn", f"Incorrect answer entered in #{interaction.channel.name}",
                              f"**{interaction.user}** submitted the answer `{answer}`")
        log_reply.set_thumbnail(interaction.user.display_avatar)
        log_reply.add_field(name="User ID", value=interaction.user.id, inline=False)
        log_reply.add_field(name="Date joined", value=interaction.user.joined_at, inline=False)

    else:
        # Let the user know that the answer was not correct.
        user_reply = dialogBox("Success", "Verified!", "Thank you for verifying. Welcome to the server! :heart:")

        # Send a log to the logging channel visible only to moderators.
        log_reply = dialogBox("Success", f"User successfully verified in #{interaction.channel.name}",
                              f"**{interaction.user}** submitted the answer `{answer}`")
        log_reply.set_thumbnail(interaction.user.display_avatar)
        log_reply.add_field(name="User ID", value=interaction.user.id, inline=False)
        log_reply.add_field(name="Date joined", value=interaction.user.joined_at, inline=False)

        # Apply the verified role to the user that invoked the command.
        verified_role = interaction.guild.get_role(VERIFIED_ROLE_ID)
        await interaction.user.add_roles(verified_role)
    
    await interaction.send(embed=user_reply, ephemeral=True)
    await bot.get_channel(LOGGING_CHANNEL_ID).send(embed=log_reply)

@bot.event
async def on_message(message):
    # If the message is from someone else and is in the verify channel, delete it. Nothing should go there.
    if message.author == bot.user:
        return
    if message.channel.id != VERIFY_CHANNEL_ID:
        return
    else:
        await message.delete()

token = [line.rstrip() for line in open('token.txt')][0]
bot.run(token)