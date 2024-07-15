import discord
from discord import app_commands, ui
from discord.ext import commands
from discord.utils import get
import api
import config
import sqlite3
import requests
import datetime
import string

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute("""CREATE TABLE "data" (
	"DISCORD ID"	INTEGER,
	"DOMAIN"	TEXT,
	"DOMAIN TYPE"	TEXT,
	"TARGET"	TEXT,
	"created_at"	TEXT
);""")
con.commit()
con.close()

class a_modal(ui.Modal, title="정보를 입력해주세요."):
    answer0 = ui.TextInput(label="원하는 도메인", style=discord.TextStyle.short, placeholder="ex) mc", required=True)
    answer1 = ui.TextInput(label="IP", style=discord.TextStyle.short, placeholder="ex) 127.0.0.1", required=True, max_length=16)
    async def on_submit(client, interaction: discord.Interaction):
        name = client.answer0.value
        target = client.answer1.value
        for char in string.punctuation:
            if char != "-":
                if char in name:
                    await interaction.response.send_message("등록 불가능 도메인입니다.", ephemeral=True)
                    return

        if name not in config.blacklist:
            # DB 연결 및 도메인 등록 개수 확인.
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM data WHERE `DISCORD ID` = ?", (interaction.user.id,))
            data = cur.fetchall()
            subdomain = name
            # 도메인까지 적혀 있을 경우, 서비스 도메인을 새로 정의.
            if f"{config.domain}" in name:
                subdomain = name.replace(f".{config.domain}", "")
            # 블랙리스트 IP인지 확인.
            if f"{target}" in config.blacklist_ip:
                await interaction.response.send_message("등록 금지된 IP입니다.", ephemeral=True)
                return
            # 이미 등록된 레코드인지 확인.
            cur.execute("SELECT * FROM data WHERE `DOMAIN` = ?", (f"{subdomain}.{config.domain}",))
            data2 = cur.fetchall()
            if len(data) < int(config.domain_limit) or interaction.user.id in config.admin_id:
                if len(data2) != 0:
                    await interaction.response.send_message("이미 등록된 도메인입니다.", ephemeral=True)
                    return
                url = f"http://{config.api_host}/autodns/{config.bot_key}/a/{name}/{target}/{config.zone_id}/{config.email}/{config.api_key}"
                response = requests.get(url)
                result = response.status_code
                if result == 200:
                    # DB에 등록.
                    cur.execute("INSERT INTO data VALUES(?, ?, ?, ?, ?);", (interaction.user.id, f"{subdomain}.{config.domain}", "A", target, datetime.datetime.now()))
                    con.commit()
                    await interaction.response.send_message(f"등록 완료\n도메인:\n> {subdomain}.{config.domain}", ephemeral=True)
                    print(f"{subdomain}.{config.domain} is Registered")
                else:
                    print(f"오류 로그: {result}")
                    await interaction.response.send_message("오류가 발생했습니다. 관리자에게 문의하세요.", ephemeral=True)
            else:
                await interaction.response.send_message(f"도메인 최대 등록 개수가 초과하였습니다.\n최대 개수: {config.domain_limit}", ephemeral=True)
            con.close()
        else:
            await interaction.response.send_message("등록 불가능 도메인입니다.", ephemeral=True)
            
class cname_modal(ui.Modal, title="정보를 입력해주세요."):
    answer0 = ui.TextInput(label="원하는 도메인", style=discord.TextStyle.short, placeholder="ex) mc", required=True)
    answer1 = ui.TextInput(label="도메인", style=discord.TextStyle.short, placeholder="ex) alcl.kr", required=True, max_length=16)
    async def on_submit(client, interaction: discord.Interaction):
        name = client.answer0.value
        target = client.answer1.value
        for char in string.punctuation:
            if char != "-":
                if char in name:
                    await interaction.response.send_message("등록 불가능 도메인입니다.", ephemeral=True)
                    return

        if name not in config.blacklist:
            # DB 연결 및 도메인 등록 개수 확인.
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM data WHERE `DISCORD ID` = ?", (interaction.user.id,))
            data = cur.fetchall()
            subdomain = name
            # 도메인까지 적혀 있을 경우, 서비스 도메인을 새로 정의.
            if f"{config.domain}" in name:
                subdomain = name.replace(f".{config.domain}", "")
            # 블랙리스트 IP인지 확인.
            if f"{target}" in config.blacklist_ip:
                await interaction.response.send_message("등록 금지된 도메인입니다.", ephemeral=True)
                return
            # 이미 등록된 레코드인지 확인.
            cur.execute("SELECT * FROM data WHERE `DOMAIN` = ?", (f"{subdomain}.{config.domain}",))
            data2 = cur.fetchall()
            if len(data) < int(config.domain_limit) or interaction.user.id in config.admin_id:
                if len(data2) != 0:
                    await interaction.response.send_message("이미 등록된 도메인입니다.", ephemeral=True)
                    return
                url = f"http://{config.api_host}/autodns/{config.bot_key}/cname/{name}/{target}/{config.zone_id}/{config.email}/{config.api_key}"
                response = requests.get(url)
                result = response.status_code
                if result == 200:
                    # DB에 등록.
                    cur.execute("INSERT INTO data VALUES(?, ?, ?, ?, ?);", (interaction.user.id, f"{subdomain}.{config.domain}", "CNAME", target, datetime.datetime.now()))
                    con.commit()
                    await interaction.response.send_message(f"등록 완료\n도메인:\n> {subdomain}.{config.domain}", ephemeral=True)
                    print(f"{subdomain}.{config.domain} is Registered")
                else:
                    print(f"오류 로그: {result}")
                    await interaction.response.send_message("오류가 발생했습니다. 관리자에게 문의하세요.", ephemeral=True)
            else:
                await interaction.response.send_message(f"도메인 최대 등록 개수가 초과하였습니다.\n최대 개수: {config.domain_limit}", ephemeral=True)
            con.close()
        else:
            await interaction.response.send_message("등록 불가능 도메인입니다.", ephemeral=True)

class srv_modal(ui.Modal, title="정보를 입력해주세요."):
    answer0 = ui.TextInput(label="원하는 도메인", style=discord.TextStyle.short, placeholder="ex) mc", required=True)
    answer1 = ui.TextInput(label="A 레코드:포트", style=discord.TextStyle.short, placeholder="ex) secure.alcl.cloud:25565", required=True)
    async def on_submit(client, interaction: discord.Interaction):
        name = client.answer0.value
        target_port = client.answer1.value
        for char in string.punctuation:
            if char != "-":
                if char in name:
                    await interaction.response.send_message("등록 불가능 도메인입니다.", ephemeral=True)
                    return

        if name not in config.blacklist:
            # DB 연결 및 도메인 등록 개수 확인.
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM data WHERE `DISCORD ID` = ?", (interaction.user.id,))
            data = cur.fetchall()
            if len(data) < int(config.domain_limit) or interaction.user.id in config.admin_id:
                target_port = target_port.strip()
                target, port = target_port.split(':')
                # 도메인까지 적혀 있을 경우, 서비스 도메인을 새로 정의.
                subdomain = name
                if f"{config.domain}" in name:
                    subdomain = name.replace(f".{config.domain}", "")
                cur.execute("SELECT * FROM data WHERE `DOMAIN` = ?", (f"{subdomain}.{config.domain}",))
                data2 = cur.fetchall()
                if len(data2) != 0:
                    await interaction.response.send_message("이미 등록된 도메인입니다.", ephemeral=True)
                    return
                url = f"http://{config.api_host}/autodns/{config.bot_key}/srv/{name}/{target}/{port}/{config.zone_id}/{config.email}/{config.api_key}"
                response = requests.get(url)
                result = response.status_code
                if result == 200:
                    subdomain = name
                    # 도메인까지 적혀 있을 경우, 서비스 도메인을 새로 정의.
                    if f"{config.domain}" in name:
                        subdomain = name.replace(f".{config.domain}", "")
                    # DB에 등록.
                    cur.execute("INSERT INTO data VALUES(?, ?, ?, ?, ?);", (interaction.user.id, f"{subdomain}.{config.domain}", "SRV", target_port, datetime.datetime.now()))
                    con.commit()
                    await interaction.response.send_message(f"등록 완료\n도메인:\n> {subdomain}.{config.domain}", ephemeral=True)
                    print(f"{subdomain}.{config.domain} is Registered")
                else:
                    print(f"오류 로그: {result}")
                    await interaction.response.send_message(f"오류가 발생했습니다. 관리자에게 문의하세요.", ephemeral=True)
            else:
                await interaction.response.send_message(f"도메인 최대 등록 개수가 초과하였습니다.\n최대 개수: {config.domain_limit}", ephemeral=True)
                con.close()
        else:
            await interaction.response.send_message("등록 불가능 도메인입니다.", ephemeral=True)

class removedns_modal(ui.Modal, title="정보를 입력해주세요."):
    answer0 = ui.TextInput(label="원하는 도메인", style=discord.TextStyle.short, placeholder="ex) mc", required=True)
    async def on_submit(client, interaction: discord.Interaction):
        name = client.answer0.value
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        subdomain = name
        if f"{config.domain}" in name:
            subdomain = name.replace(f".{config.domain}", "")
        cur.execute("SELECT * FROM data WHERE `DISCORD ID` = ? AND `DOMAIN` = ?", (interaction.user.id, f"{subdomain}.{config.domain}"))
        data = cur.fetchall()
        if len(data) == 0:
            await interaction.response.send_message("소지한 도메인과 일치하지 않습니다.", ephemeral=True)
            return
        url = f"http://{config.api_host}/autodns/{config.bot_key}/getid/{name}/{config.zone_id}/{config.email}/{config.api_key}/{config.domain}"
        response = requests.get(url)
        if response.status_code == 200:
            id = response.text
        if id == "Error":
            await interaction.response.send_message(f"오류가 발생했습니다. 관리자에게 문의하세요.", ephemeral=True)
        url = f"http://{config.api_host}/autodns/{config.bot_key}/removerecord/{id}/{config.zone_id}/{config.email}/{config.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            subdomain = name
            if f"{config.domain}" in name:
                subdomain = name.replace(f".{config.domain}", "")
            cur.execute("DELETE FROM data WHERE `DOMAIN` = ?", (f"{subdomain}.{config.domain}",))
            con.commit()
            await interaction.response.send_message(f"삭제 완료\n도메인\n> {subdomain}.{config.domain}", ephemeral=True)
            print(f"{subdomain}.{config.domain} is Removed")
        elif response.status_code == 400:
            await interaction.response.send_message("삭제 실패했습니다.", ephemeral=True)
        else:
            print(response.status_code)
            await interaction.response.send_message("오류가 발생했습니다. 관리자에게 문의하세요.", ephemeral=True)
        con.close()
        
class button1(discord.ui.View):
    @discord.ui.button(label="A 레코드", style=discord.ButtonStyle.green)
    async def my_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_modal(a_modal())
    @discord.ui.button(label="CNAME 레코드", style=discord.ButtonStyle.green)
    async def my_select2(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_modal(cname_modal())
    @discord.ui.button(label="SRV 레코드", style=discord.ButtonStyle.green)
    async def my_select3(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_modal(srv_modal())
    @discord.ui.button(label="삭제", style=discord.ButtonStyle.red)
    async def my_select4(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_modal(removedns_modal())
    @discord.ui.button(label="조회", style=discord.ButtonStyle.blurple)
    async def my_select5(self, interaction: discord.Interaction, select: discord.ui.Select):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM data WHERE `DISCORD ID` = ?", (interaction.user.id,))
        data_list = cur.fetchall()
        embed = discord.Embed(title="도메인 조회")
        embed.add_field(name="등록된 도메인 개수", value=len(data_list), inline=False)
        if data_list != 0:
            embed.add_field(name="도메인", value=f"", inline=False)
            for data in data_list:
                embed.add_field(name="", value=f"{data[1]}\n대상: {data[3]}\n", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@client.event
async def on_ready():
    print(client.user.name, 'has connected to Discord!')
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Made by ckfejrdld"))
    await tree.sync(guild=discord.Object(id=1028921403875000321))
    print("ready")
    
@tree.command(name="도메인", description="도메인 패널 불러오기", guild=discord.Object(id=int(config.guild_id)))
async def domain(interaction):
    if interaction.guild.id == int(config.guild_id):
        embed = discord.Embed(title="AL CLOUD Auto DNS", description="아래 버튼을 선택하세요.", color=0xFF2424)
        embed.add_field(name="", value="> **A 레코드**란? IP 형식에 적용 가능한 도메인입니다.\n> **SRV 레코드**란? A 레코드:PORT 형식에 적용 가능한 도메인입니다.")
        await interaction.response.send_message(embed=embed, view=button1(), ephemeral=True)
    else:
        await interaction.response.send_message("허가된 서버가 아닙니다.")

@client.event
async def on_message(message):
    split = message.content.split(" ")
    if message.content == f"{config.prefix}크레딧":
        embed = discord.Embed(title="Credits", color=0x666666)
        embed.add_field(name="개발", value="ckfejrdld", inline=False)
        embed.add_field(name="개발환경", value="Python 3.11", inline=False)
        embed.add_field(name="운영환경", value="Python 3.11", inline=False)
        embed.add_field(name="연락 E-Mail", value="ckfejrdld@nperm.net", inline=False)
        embed.set_footer(text="(C) 2023 ckfejrdld, with All rights reserved.")
        await message.channel.send(embed=embed)

    if message.content == f"{config.prefix}도움말":
        embed = discord.Embed(title = "도움말", description = f"""
        **{config.prefix}도움말**\n``도움말``을 해당 채널에 전송\n``Example: {config.prefix}도움말``\n\n
        **{config.prefix}크레딧**\n봇을 제작하는게 관여한 개발자 및 개발환경을 메시지로 해당 채널에 전송\n``Example: {config.prefix}크래딧``\n\n
        **{config.prefix}도메인**\n 도메인 관리 패널을 불러옵니다.\n``Example: {config.prefix}도메인``
        """
                                ,color = 0xFFC3E8)
        embed.set_footer(text="(C) 2023 ckfejrdld, with All rights reserved.")
        await message.channel.send(embed=embed)

    if message.content.startswith(f"{config.prefix}도메인"):
        if message.guild.id == int(config.guild_id):
            embed = discord.Embed(title="AL CLOUD Auto DNS",description="아래 버튼을 선택하세요.",color=0xFF2424)
            embed.add_field(name="", value="> **A 레코드**란? IP 형식에 적용 가능한 도메인입니다.\n> **CNAME 레코드**란? A/AAAA 레코드 형식에 적용 가능한 도메인입니다.\n> **SRV 레코드**란? A/AAAA 레코드:PORT 형식에 적용 가능한 도메인입니다.")
            await message.channel.send(embed=embed,view = button1())
        else:
            await message.reply("허가된 서버가 아닙니다.")

client.run(config.token)
