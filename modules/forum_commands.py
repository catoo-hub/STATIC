import nextcord
import json
import os
from nextcord.ext import commands
from nextcord import ForumChannel, Thread
from utils.config import *

class ForumCommands(commands.Cog, name="Forum Commands"):
    """Команды для работы с форумами Discord."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config_file = "./config/forum_config.json"
        self.load_config()
    
    def load_config(self):
        """Загружает конфигурацию форума"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = {
                    "forum_channel_id": None,
                    "in_progress_tag_name": "In Progress",
                    "auto_create_threads": True
                }
                self.save_config()
        except Exception as e:
            print(f"Ошибка загрузки конфигурации форума: {e}")
            self.config = {
                "forum_channel_id": None,
                "in_progress_tag_name": "In Progress",
                "auto_create_threads": True
            }
    
    def save_config(self):
        """Сохраняет конфигурацию форума"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения конфигурации форума: {e}")
    
    @commands.command(name="setupforum", description="Настроить форум для автоматических заявок")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setup_forum(self, ctx: commands.Context, forum_channel):
        """Настраивает форум для автоматического создания публикаций с заявками"""
        try:
            # Пытаемся найти канал форума разными способами
            found_channel = None
            
            # 1. Пробуем как ID
            if forum_channel.isdigit():
                found_channel = ctx.guild.get_channel(int(forum_channel))
            
            # 2. Пробуем как упоминание
            elif forum_channel.startswith('<#') and forum_channel.endswith('>'):
                channel_id = int(forum_channel[2:-1])
                found_channel = ctx.guild.get_channel(channel_id)
            
            # 3. Пробуем как название канала
            else:
                # Убираем невидимые символы и пробелы
                clean_name = forum_channel.strip().replace('⁠', '').replace('​', '')
                for channel in ctx.guild.channels:
                    if (isinstance(channel, ForumChannel) and 
                        channel.name.lower() == clean_name.lower()):
                        found_channel = channel
                        break
            
            # Проверяем, что канал найден и это форум
            if not found_channel:
                await ctx.send("❌ Канал форума не найден! Убедитесь, что указан правильный форум.")
                return
            
            if not isinstance(found_channel, ForumChannel):
                await ctx.send("❌ Указанный канал не является форумом! Выберите канал типа 'Форум'.")
                return
            
            # Сохраняем настройки
            self.config["forum_channel_id"] = found_channel.id
            self.save_config()
            
            embed = nextcord.Embed(
                title="✅ Форум настроен",
                description=f"Форум {found_channel.mention} успешно настроен для автоматических заявок!",
                color=nextcord.Color.green()
            )
            embed.add_field(name="Форум", value=found_channel.mention)
            embed.add_field(name="Тег по умолчанию", value=self.config["in_progress_tag_name"])
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            error_embed = nextcord.Embed(
                title="❌ Ошибка",
                description=f"Не удалось настроить форум: {str(e)}",
                color=nextcord.Color.red()
            )
            await ctx.send(embed=error_embed)
    
    @commands.command(name="listforums", description="Показать все доступные форумы на сервере")
    @commands.guild_only()
    async def list_forums(self, ctx: commands.Context):
        """Показывает все доступные форумы на сервере"""
        try:
            forum_channels = []
            for channel in ctx.guild.channels:
                if isinstance(channel, ForumChannel):
                    forum_channels.append(channel)
            
            if not forum_channels:
                await ctx.send("❌ На сервере нет форумов!")
                return
            
            embed = nextcord.Embed(
                title="📋 Доступные форумы",
                description=f"Найдено {len(forum_channels)} форумов на сервере:",
                color=nextcord.Color.blue()
            )
            
            for i, forum in enumerate(forum_channels, 1):
                embed.add_field(
                    name=f"{i}. {forum.name}",
                    value=f"ID: `{forum.id}` | {forum.mention}",
                    inline=False
                )
            
            embed.add_field(
                name="💡 Подсказка",
                value="Используйте ID форума или его название для команды `!setupforum`",
                inline=False
            )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            error_embed = nextcord.Embed(
                title="❌ Ошибка",
                description=f"Не удалось получить список форумов: {str(e)}",
                color=nextcord.Color.red()
            )
            await ctx.send(embed=error_embed)
    
    @commands.command(name="checktags", description="Проверить теги в форуме")
    @commands.guild_only()
    async def check_tags(self, ctx: commands.Context):
        """Проверяет теги в настроенном форуме"""
        try:
            if not self.config["forum_channel_id"]:
                await ctx.send("❌ Форум не настроен! Используйте команду `!setupforum`")
                return
            
            forum_channel = ctx.guild.get_channel(self.config["forum_channel_id"])
            if not forum_channel:
                await ctx.send("❌ Найденный форум не существует!")
                return
            
            # Проверяем доступные теги
            tags_info = []
            for tag in forum_channel.available_tags:
                tags_info.append(f"• {tag.name} (ID: {tag.id})")
            
            embed = nextcord.Embed(
                title="🏷️ Теги в форуме",
                description=f"Проверка тегов в форуме {forum_channel.mention}",
                color=nextcord.Color.blue()
            )
            embed.add_field(name="Форум", value=f"{forum_channel.name} (ID: {forum_channel.id})")
            embed.add_field(name="Доступные теги", value="\n".join(tags_info) if tags_info else "Нет тегов", inline=False)
            embed.add_field(name="Количество тегов", value=str(len(forum_channel.available_tags)))
            
            # Проверяем, есть ли тег "In Progress"
            in_progress_tag = None
            for tag in forum_channel.available_tags:
                if tag.name.lower() == "in progress":
                    in_progress_tag = tag
                    break
            
            if in_progress_tag:
                embed.add_field(name="✅ Тег 'In Progress'", value=f"Найден: {in_progress_tag.name} (ID: {in_progress_tag.id})", inline=False)
            else:
                embed.add_field(name="❌ Тег 'In Progress'", value="Не найден! Нужно создать вручную", inline=False)
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            error_embed = nextcord.Embed(
                title="❌ Ошибка",
                description=f"Не удалось проверить теги: {str(e)}",
                color=nextcord.Color.red()
            )
            await ctx.send(embed=error_embed)

def setup(bot: commands.Bot):
    bot.add_cog(ForumCommands(bot)) 
