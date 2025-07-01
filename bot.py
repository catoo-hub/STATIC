import os
import nextcord, asyncio
from nextcord.ext import commands

import aiohttp

import requests
import json

from utils.config import *

from datetime import datetime
import time
import calendar

from pytz import timezone

client = nextcord.Client()
created_channels = {}
guild = None

# After Effects System
# Plugins System
class PluginsDropdown(nextcord.ui.Select):

  def __init__(self):
    options = [
      nextcord.SelectOption(
        label="AE Camera Morph 1.2.2",
        description=
        "Allows you to morph between your cameras in After Effects just like you do in Cinema 4d."
      ),
      nextcord.SelectOption(
        label="AE Pixel Sorter 2",
        description=
        "AE Pixel Sorter was the first tool to bring the pixel sorting glitch effect."
      ),
      nextcord.SelectOption(
        label="Boris FX Continuum Complete 2022",
        description=
        "ELEGANT GLOWS, POWERFUL NEW TRANSITIONS, AND 250+ CURATED PRESETS."
      ),
      nextcord.SelectOption(
        label="Boris FX Sapphire Plug-ins 2022",
        description=
        "Sapphire plugins let you create stunning organic looks unmatched by any host native effect tools."
      ),
      nextcord.SelectOption(
        label="Color Vibrance",
        description=
        "Deep vibrant colours are tricky, so we've created plugin that make HOT colours easy and instant."
      ),
      nextcord.SelectOption(
        label="Bokeh",
        description=
        "Bokeh is full parametric control of Bokeh shape with beautiful tonal mapping and flares."
      ),
      nextcord.SelectOption(
        label="Deep Glow",
        description="Deep glow the best looking glow right out of the box."
      ),
      nextcord.SelectOption(
        label="Displace Pro",
        description=
        "The humble AE displacement map with more features + juiced up on the GPU."
      ),
      nextcord.SelectOption(
        label="Element 3D",
        description=
        "High Performance After Effects™ Plug-in for creating Motion Design & Visual FX!"
      ),
      nextcord.SelectOption(
        label="FilmConvert Nitrate",
        description=
        "A new set of features to give you even more power and control over your color grading."
      ),
      nextcord.SelectOption(
        label="Glitch 7in1",
        description=
        "The ultimate glitch plugin collection for After Effects."
      )
    ]
    super().__init__(custom_id="custom_id_lol", placeholder="Select the plugin that interests you.",
                     options=options,
                     min_values=1,
                     max_values=1)

  async def callback(self, interaction: nextcord.Interaction):
    # Download Plugins links
    plugindescs = [{
      'Deep Glow':
      'Deep glow the best looking glow right out of the box.',
      'AE Pixel Sorter 2':
      'AE Pixel Sorter was the first tool to bring the pixel sorting glitch effect.',
      'Bokeh':
      'Bokeh is full parametric control of Bokeh shape with beautiful tonal mapping and flares.',
      'Displace Pro':
      'The humble AE displacement map with more features + juiced up on the GPU.',
      'AE Camera Morph 1.2.2':
      'Allows you to morph between your cameras in After Effects just like you do in Cinema 4d.',
      'Boris FX Continuum Complete 2022':
      'ELEGANT GLOWS, POWERFUL NEW TRANSITIONS, AND 250+ CURATED PRESETS.',
      'Boris FX Sapphire Plug-ins 2022':
      'Sapphire plugins let you create stunning organic looks unmatched by any host native effect tools.',
      'Color Vibrance':
      'Deep vibrant colours are tricky, so weve created plugin that make HOT colours easy and instant.',
      'Element 3D':
      'High Performance After Effects™ Plug-in for creating Motion Design & Visual FX!',
      'FilmConvert Nitrate':
      'A new set of features to give you even more power and control over your color grading.',
      'Glitch 7in1':
      'The ultimate glitch plugin collection for After Effects.'
    }]

    dwlinks = [{
      'Deep Glow':
      'https://drive.google.com/drive/folders/1E7CqnTc7CLLZmgmF_DeGTZA_l4DgSb4X',
      'AE Pixel Sorter 2':
      'https://drive.google.com/drive/folders/1H9nnLFQvBd17ygOn5DbdX4uxPvzB_ivl',
      'Bokeh':
      'https://drive.google.com/drive/folders/1oIQSqMUEi_ptOU9qvCDRDgMvi9H39-fZ',
      'Displace Pro':
      'https://drive.google.com/drive/folders/12cEwtRDAyEJdO03wSmvjw6D-l4zhXzm0',
      'AE Camera Morph 1.2.2':
      'https://drive.google.com/drive/folders/1dLyl9_cL0uQPgv486uAE7ekPfD8PA9P8?usp=share_link',
      'Boris FX Continuum Complete 2022':
      'https://drive.google.com/drive/folders/1pW1SBbQJi8YXO1phY0pPNSuQlVwAkcFd?usp=share_link',
      'Boris FX Sapphire Plug-ins 2022':
      'https://drive.google.com/drive/folders/1kurw8tGQF4iaoeJONfpIIWni4X_WrwZO?usp=share_link',
      'Color Vibrance':
      'https://drive.google.com/drive/folders/1Bsi2J25IYjbH2eyY8pFs87A0muY5ED_V?usp=share_link',
      'Element 3D':
      'https://drive.google.com/drive/folders/1CoF28FvUmStL9bzXPtIpMOLnC8X1_ru0?usp=share_link',
      'FilmConvert Nitrate':
      'https://drive.google.com/drive/folders/14cq2t2AtLXsj8Ql6eQjrJpAMbMRPKF0p?usp=share_link',
      'Glitch 7in1':
      'https://drive.google.com/drive/folders/1C2Wjyvr2Gvp1NHuUuuifVm8JPY6eaxiH?usp=share_link'
    }]

    pluginkeys = [{
      '':
      ''
    }]

    # Заменяет ссылку на ссылку из массива 'dwlinks'
    dwlink = dwlinks[0][f'{self.values[0]}']
    plugindesc = plugindescs[0][f'{self.values[0]}']

    embed = nextcord.Embed(
      color=nextcord.Color.from_rgb(43, 45, 49),
      title=f"{self.values[0]}",
      description=f"{plugindesc}",
      url=f"{dwlink}"
    )

    # Plugin message
    await interaction.response.send_message(
      f"You chose `{self.values[0]}` as the plugin. [Download plugin]({dwlink}). \n [Keys are here!](https://drive.google.com/file/d/1HHfoSqWwn-55Ul5eBKKGbIpPEiccSwuU/view?usp=share_link).",
      ephemeral=True, embed=embed)

class PluginsView(nextcord.ui.View):

  def __init__(self):
    super().__init__(timeout=None) # timeout of the view must be set to None)
    self.add_item(PluginsDropdown())

  async def on_timeout(self):
    await self.message.edit(content=configuration_timeout_confirmation_message, view=self)

# Scripts System
class ScriptsDropdown(nextcord.ui.Select):

  def __init__(self):
    options = [
      nextcord.SelectOption(
        label="BlenderAE",
        description=
        "Allows you to morph between your cameras in After Effects just like you do in Cinema 4d."
      ),
      nextcord.SelectOption(
        label="VooDoo",
        description=
        "Advanced analogue of Puppet Tools"
      ),
      nextcord.SelectOption(
        label="FX Console",
        description=
        "Speed up your After Effects work and get stuff done faster!"
      ),
      nextcord.SelectOption(
        label="TextEvo 2",
        description=
        "Script to create text animation."
      ),
      nextcord.SelectOption(
        label="EasyLayers by LankyLucius",
        description=
        "EasyLayers + Twixtor Script"
      ),
      nextcord.SelectOption(
        label="Textbox 2",
        description=
        "Customisable shape behind your text that updates automatically."
      ),
      nextcord.SelectOption(
        label="Tilda",
        description=
        "Script to create and animate wavy lines"
      )
    ]
    super().__init__(custom_id="custom_id_lol2", placeholder="Select the plugin that interests you.",
                     options=options,
                     min_values=1,
                     max_values=1)

  async def callback(self, interaction: nextcord.Interaction):
    
    # Download Scripts links
    scriptdwlinks = [{
      'BlenderAE':
      'https://drive.google.com/drive/folders/1TLMgUl_D_hvhfmABvkd1DnVTdr2FZCLO?usp=sharing',
      'VooDoo':
      'https://cdn.discordapp.com/attachments/848495634776588305/1093093879529603123/voodoo_v.1.000.rar?ex=66320101&is=661f8c01&hm=2eb2851b68011d9fd2f200887b38dd532ff1869686c8330849edf9b78e4ad5f3&',
      'FX Console':
      'https://cdn.discordapp.com/attachments/1140955175511670846/1230940978035032175/FXConsole_1.0.5_Installer_x64_2022.exe?ex=6635261e&is=6622b11e&hm=bd9a81ff9fd61404714dfd3b512d97282ee2d4d2f796103ab8760a2d74120cb4&',
      'TextEvo 2':
      'https://cdn.discordapp.com/attachments/848495634776588305/1099251232725549076/textevo_2.0.0.rar?ex=662cb7fc&is=661a42fc&hm=9c8af35bb3743e9745064795cd8013193d12219e41b95a6fe8b3ac46dc6cce9f&',
      'EasyLayers by LankyLucius':
      'https://cdn.discordapp.com/attachments/848495634776588305/1056136228518514738/EasyLayers_by_LankyLucius.zip?ex=662cc082&is=661a4b82&hm=0d6cdf40b64c9729dc9097e5fb80929df4d51555b2f53846d424fb0d5d8af529&',
      'Textbox 2':
      'https://cdn.discordapp.com/attachments/848495634776588305/1056130023175770152/TextBox2_v1.2.rar?ex=6623803b&is=66222ebb&hm=6c94bf69a7beb74984980d9e8c5e6358f338e7b3c10633c1bc789a7cb967bcb1&',
      'Tilda':
      'https://cdn.discordapp.com/attachments/848495634776588305/1044253842054840371/Tilda_v1.0.rar?ex=662faaad&is=661d35ad&hm=46ee9ee74f1cadd4fbdadb7c62e3731c4f5a501fe8c9e17415fe28802476fee1&'
    }]

    scriptvideos = [{
      'BlenderAE':
      'https://cdn.discordapp.com/attachments/848495634776588305/1007720898205323414/BlenderAe_720p.mp4',
      'VooDoo':
      'https://cdn.discordapp.com/attachments/848495634776588305/1093093878942404648/voodoo.mp4',
      'FX Console':
      'https://cdn.discordapp.com/attachments/996382278311751730/1099257623821439057/fx1.0.1-1.mp4',
      'TextEvo 2':
      'https://cdn.discordapp.com/attachments/848495634776588305/1099251231760855060/TextEvo_2_for_After_Effects.mp4',
      'EasyLayers by LankyLucius':
      'https://cdn.discordapp.com/attachments/848495634776588305/1056136227750952960/EasyLayers_by_LankyLucius_New_Script_For_Fast_Twixtor_Scales_and.mp4',
      'Textbox 2':
      'https://cdn.discordapp.com/attachments/848495634776588305/1056130022483701780/TextBox_Promo.mp4',
      'Tilda':
      'https://cdn.discordapp.com/attachments/848495634776588305/1044253841757052928/Tilda_for_After_Effects_720p.mp4'
    }]

    scriptdescs = [{
      'BlenderAE':
      'Allows you to morph between your cameras in After Effects just like you do in Cinema 4d.',
      'VooDoo':
      'Advanced analogue of Puppet Tools',
      'FX Console':
      'Speed up your After Effects work and get stuff done faster!',
      'TextEvo 2':
      'Script to create text animation.',
      'EasyLayers by LankyLucius':
      'EasyLayers + Twixtor Script',
      'Textbox 2':
      'Customisable shape behind your text that updates automatically.',
      'Tilda':
      'Script to create and animate wavy lines'
    }]

    # Заменяет ссылку на ссылку из массива 'dwlinks'
    scriptdwlink = scriptdwlinks[0][f'{self.values[0]}']
    scriptvideo = scriptvideos[0][f'{self.values[0]}']
    scriptdesc = scriptdescs[0][f'{self.values[0]}']

    embed = nextcord.Embed(
      color=nextcord.Color.from_rgb(43, 45, 49),
      title=f"{self.values[0]}",
      description=f"{scriptdesc}",
      url=f"{scriptdwlink}"
    )

    # Plugin message
    await interaction.response.send_message(
      f"You chose `{self.values[0]}` as the script. [Download script]({scriptdwlink}).", embed=embed, ephemeral=True)

class ScriptsView(nextcord.ui.View):

  def __init__(self):
    super().__init__(timeout=None) # timeout of the view must be set to None)
    self.add_item(ScriptsDropdown())

  async def on_timeout(self):
    await self.message.edit(content=configuration_timeout_confirmation_message, view=self)

# <@&848441067888312340>
# Form Modal Class
class FormModal(nextcord.ui.Modal):

  # Form Modal Constructor
  def __init__(self):
    super().__init__(title=title, custom_id=app_custom_id, timeout=None)

    # Form Modal Fields

    for i in range(0, len(questions)):
      if questions[i]["style"] == "input":
        self.field = nextcord.ui.TextInput(
          label=questions[i]["question"],
          placeholder=questions[i]["placeholder"],
          required=questions[i]["required"],
          style=nextcord.TextInputStyle.short if questions[i]["style"]
          == "short" else nextcord.TextInputStyle.paragraph,
          custom_id=questions[i]["custom_id"],
        )

      self.add_item(self.field)

  # Modal Callback <t:3145315556:f>
  async def callback(self, interaction: nextcord.Interaction) -> None:

    url_avatar = interaction.user.avatar
    url_banner = interaction.user.banner

    date = datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())

    embed = nextcord.Embed(
      color=nextcord.Color.from_rgb(43, 45, 49)
    ).add_field(
      name="Information",
      value=
      f"<:1_:1078417393979764847> Name: {interaction.user.mention}\n<:2_:1078417410274631802> Time: <t:{utc_time}:R>",
      inline=False).set_thumbnail(url=url_avatar)

    # Form Embed Fields
    for question, answer in zip(questions, self.children):
      embed.add_field(
        name=question["question"],
        value=answer.value if answer.value else question_not_answered_message,
        inline=False)

    # Sending Form Embed
    await interaction.response.send_message(submit_message, ephemeral=True)
    submit_channel = await bot.fetch_channel(submit_channel_id)
    await submit_channel.send("<@&849351531060133888>, check this!", embed=embed)


# Form View Class
class FormView(nextcord.ui.View):

  # Form View Constructor
  def __init__(self):
    super().__init__(timeout=None)

  # Form View Button Callback
  @nextcord.ui.button(label=button_name,
                      style=nextcord.ButtonStyle.green,
                      emoji="✅",
                      custom_id="forms:button")
  async def button_callback(self, button: nextcord.ui.Button,
                            interaction: nextcord.Interaction):
    await interaction.response.send_modal(FormModal())


# Bot Subclass
class Bot(commands.Bot):

  # Constructor
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.persistant_modals_added = False
    self.persistant_views_added = False
    # self.instagram_posts = InstagramPosts()
    
  # Voice Channels System
  async def on_voice_state_update(self, member, before, after):
      if before.channel != after.channel:
          if before.channel:
              # Пользователь покинул канал, проверяем, что это был наш созданный канал
              if before.channel.id in created_channels:
                  # Если в канале не осталось пользователей, удаляем его
                  if len(before.channel.members) == 0:
                      del created_channels[before.channel.id]
                      await before.channel.delete()
          if after.channel:
              # Пользователь зашел в канал, проверяем, что это наш канал создания каналов
              if after.channel.id == 1094510513196630156:
                  guild = member.guild  # получаем сервер
                  category = after.channel.category  # получаем категорию, в которой находится канал after.channel
                  overwrites = {
                      guild.default_role: nextcord.PermissionOverwrite(connect=True),
                      member: nextcord.PermissionOverwrite(connect=True, manage_channels=True, manage_permissions=True)
                  }
                  # Создаем новый голосовой канал в той же категории, что и канал after.channel
                  created_channel = await guild.create_voice_channel(f"{member.display_name}'s channel", overwrites=overwrites, category=category)
                  created_channels[created_channel.id] = member.id
                  # Переносим пользователя в созданный канал
                  await member.move_to(created_channel)

  # Ready Event
  async def on_ready(self):

    if self.persistant_modals_added == False:
      self.persistant_modals_added = True
      self.add_modal(FormModal())

    if self.persistant_views_added == False:
      self.persistant_views_added = True
      self.add_view(FormView())
      self.add_view(PluginsView())
      self.add_view(ScriptsView())

      await self.change_presence(activity=nextcord.Game(name="STATIC!"))
      
    print(
      f"----------------------------------\n       LAUNCH INFORMATION\n----------------------------------\nStarted: True\nDebug Mode: False\nDate: {datetime.now(tz = timezone('US/Eastern')).strftime('%Y-%m-%d | Time: %H:%M:%S')}\nPersistant Views Added: {str(self.persistant_views_added)}\nPersistant Modals Added: {str(self.persistant_modals_added)}\n----------------------------------"
    )
    
    # await self.instagram_posts.check_for_new_post()
    
# Bot Instance
bot = Bot(command_prefix=PREFIX,
          intents=nextcord.Intents.all(),
          help_command=None)

# Load Modules
for file in os.listdir("./modules"):
  if file.endswith(".py"):
    bot.load_extension(f"modules.{file[:-3]}")
    print("Loaded module: " + file[:-3])

# Run Bot
bot.run(TOKEN)