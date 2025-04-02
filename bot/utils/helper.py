from aiogram.types import BotCommand


def format_time_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{int(seconds)}с"
    elif seconds < 3600:
        return f"{int(seconds / 60)}м"
    else:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        return f"{hours}ч {minutes}м"


def format_number(num: int) -> str:
    if num < 1000:
        return str(num)
    elif num < 1000000:
        return f"{num / 1000:.1f}K".replace(".0K", "K")
    else:
        return f"{num / 1000000:.1f}M".replace(".0M", "M")


class BotCommands:
    @staticmethod
    async def setup_commands(bot):
        commands = [
            BotCommand(command="start", description="🚀 Start"),
        ]
        await bot.set_my_commands(commands)
