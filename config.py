import toml
from dataclasses import dataclass

conf_file = open("config.toml", "r")
config_settings = toml.loads(conf_file.read())
@dataclass
class Config:
    DISCORD_BOT_TOKEN = config_settings["DISCORD_BOT_TOKEN"]
    VERIFY_CHANNEL_ID = config_settings["VERIFY_CHANNEL_ID"]
    LOGGING_CHANNEL_ID = config_settings["LOGGING_CHANNEL_ID"]
    VERIFIED_ROLE_ID = config_settings["VERIFIED_ROLE_ID"]
    TEST_GUILD_IDS = config_settings["TEST_GUILD_IDS"]
conf_file.close()

msgs_file = open("messages.toml", "r")
messages = toml.loads(msgs_file.read())
@dataclass
class Message:
    @dataclass
    class HEADERMSG:
        OPENER = messages["HEADERMSG_OPENER"]
        QUESTION = messages["HEADERMSG_QUESTION"]
        INSTRUCTION = messages["HEADERMSG_INSTRUCTION"]
    @dataclass
    class VERIFY:
        ALREADY_VERIFIED = messages["VERIFY_ALREADY_VERIFIED"]
        SUCCESS = messages["VERIFY_SUCCESS"]
        FAILURE = messages["VERIFY_FAILURE"]

msgs_file.close()
