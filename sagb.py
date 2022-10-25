import nextcord
from nextcord.ext import commands

TESTING_GUILD_ID = 887723918574645328
VERIFY_CHANNEL_ID = 1034026349435826196
LOGGING_CHANNEL_ID = 1034028449356066866

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
        await interaction.send("Hm. It looks like that answer isn't in the list of accepted responses. Please try again.", ephemeral=True)
        reply = nextcord.Embed(title=f"Incorrect answer entered in #{interaction.channel.name}",
                               description=f"**{interaction.user}** submitted the answer `{answer}`",
                               colour=nextcord.Color.from_rgb(253, 203, 110))
        reply.set_thumbnail(interaction.user.display_avatar)
        reply.add_field(name="User ID", value=interaction.user.id, inline=False)
        reply.add_field(name="Date joined", value=interaction.user.joined_at, inline=False)
        await  bot.get_channel(LOGGING_CHANNEL_ID).send(embed=reply)
    else:
        await interaction.send("Thank you for verifying. Welcome to the server! <3", ephemeral=True)

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