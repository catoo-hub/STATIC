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
                    "applications_role_id": None,
                    "in_progress_tag_name": "In Progress",
                    "auto_create_threads": True
                }
                self.save_config()
        except Exception as e:
            print(f"Ошибка загрузки конфигурации форума: {e}")
            self.config = {
                "forum_channel_id": None,
                "applications_role_id": None,
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
    async def setup_forum(self, ctx: commands.Context, forum_channel: ForumChannel, applications_role: nextcord.Role):
        """Настраивает форум для автоматического создания публикаций с заявками"""
        try:
            # Сохраняем настройки
            self.config["forum_channel_id"] = forum_channel.id
            self.config["applications_role_id"] = applications_role.id
            self.save_config()
            
            embed = nextcord.Embed(
                title="✅ Форум настроен",
                description=f"Форум {forum_channel.mention} успешно настроен для автоматических заявок!",
                color=nextcord.Color.green()
            )
            embed.add_field(name="Форум", value=forum_channel.mention)
            embed.add_field(name="Роль для заявок", value=applications_role.mention)
            embed.add_field(name="Тег по умолчанию", value=self.config["in_progress_tag_name"])
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            error_embed = nextcord.Embed(
                title="❌ Ошибка",
                description=f"Не удалось настроить форум: {str(e)}",
                color=nextcord.Color.red()
            )
            await ctx.send(embed=error_embed)
    
    @commands.command(name="forumstatus", description="Показать текущие настройки форума")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def forum_status(self, ctx: commands.Context):
        """Показывает текущие настройки форума"""
        try:
            if not self.config["forum_channel_id"]:
                await ctx.send("❌ Форум не настроен! Используйте команду `!setupforum`")
                return
            
            forum_channel = ctx.guild.get_channel(self.config["forum_channel_id"])
            applications_role = ctx.guild.get_role(self.config["applications_role_id"])
            
            if not forum_channel or not applications_role:
                await ctx.send("❌ Найденные настройки устарели! Настройте форум заново.")
                return
            
            embed = nextcord.Embed(
                title="📋 Настройки форума",
                description="Текущие настройки для автоматических заявок",
                color=nextcord.Color.blue()
            )
            embed.add_field(name="Форум", value=forum_channel.mention)
            embed.add_field(name="Роль для заявок", value=applications_role.mention)
            embed.add_field(name="Тег по умолчанию", value=self.config["in_progress_tag_name"])
            embed.add_field(name="Автосоздание публикаций", value="✅ Включено" if self.config["auto_create_threads"] else "❌ Отключено")
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            error_embed = nextcord.Embed(
                title="❌ Ошибка",
                description=f"Не удалось получить статус форума: {str(e)}",
                color=nextcord.Color.red()
            )
            await ctx.send(embed=error_embed)

def setup(bot: commands.Bot):
    bot.add_cog(ForumCommands(bot)) 
