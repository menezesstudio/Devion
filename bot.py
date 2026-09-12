import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
GUILD_ID = 1547347069918904401
GUILD = discord.Object(id=GUILD_ID)

@bot.tree.command(
    name="ping",
    description="Testa se o Devion está online",
    guild=discord.Object(id=1547347069918904401)
)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")
@bot.tree.command(
    name="help",
    description="Mostra os comandos do Devion",
    guild=discord.Object(id=1547347069918904401)
)
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 Devion — Central de Comandos",
        description="Confira os comandos disponíveis do Devion."
    )

    embed.add_field(
        name="🛠️ Utilidades",
        value="`/ping` — Verifica se o Devion está online\n"
              "`/help` — Mostra esta mensagem",
        inline=False
    )

    embed.set_footer(text="Devion • Dev Community")

    await interaction.response.send_message(embed=embed)
@bot.tree.command(
    name="userinfo",
    description="Mostra informações de um usuário",
    guild=discord.Object(id=1547347069918904401)
)
async def userinfo(interaction: discord.Interaction, membro: discord.Member):
    embed = discord.Embed(
        title=f"👤 Informações de {membro.display_name}"
    )

    embed.add_field(name="Nome", value=membro.name, inline=True)
    embed.add_field(name="ID", value=membro.id, inline=True)

    embed.add_field(
        name="Conta criada",
        value=discord.utils.format_dt(membro.created_at, style="D"),
        inline=False
    )

    embed.add_field(
        name="Entrou no servidor",
        value=discord.utils.format_dt(membro.joined_at, style="D"),
        inline=False
    )

    cargos = [cargo.mention for cargo in membro.roles[1:]]
    embed.add_field(
        name="Cargos",
        value=", ".join(cargos) if cargos else "Nenhum",
        inline=False
    )

    embed.set_thumbnail(url=membro.display_avatar.url)
    embed.set_footer(text="Devion • Dev Community")

    await interaction.response.send_message(embed=embed)
@bot.tree.command(
    name="serverinfo",
    description="Mostra informações do servidor",
    guild=discord.Object(id=1547347069918904401)
)
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild

    embed = discord.Embed(
        title=f"🛠️ Informações de {guild.name}",
        description="Informações da Dev Community."
    )

    embed.add_field(
        name="👥 Membros",
        value=str(guild.member_count),
        inline=True
    )

    embed.add_field(
        name="👑 Dono",
        value=guild.owner.mention if guild.owner else "Desconhecido",
        inline=True
    )

    embed.add_field(
        name="🆔 ID",
        value=str(guild.id),
        inline=True
    )

    embed.add_field(
        name="📅 Criado em",
        value=discord.utils.format_dt(guild.created_at, style="D"),
        inline=False
    )

    embed.add_field(
        name="💬 Canais",
        value=str(len(guild.channels)),
        inline=True
    )

    embed.add_field(
        name="🎭 Cargos",
        value=str(len(guild.roles)),
        inline=True
    )

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    embed.set_footer(text="Devion • Dev Community")

    await interaction.response.send_message(embed=embed)
@bot.tree.command(
    name="avatar",
    description="Mostra o avatar de um usuário",
    guild=discord.Object(id=1547347069918904401)
)
async def avatar(interaction: discord.Interaction, membro: discord.Member):
    embed = discord.Embed(
        title=f"🖼️ Avatar de {membro.display_name}"
    )

    embed.set_image(url=membro.display_avatar.url)
    embed.set_footer(text="Devion • Dev Community")

    await interaction.response.send_message(embed=embed)
@bot.tree.command(
    name="botinfo",
    description="Mostra informações do Devion",
    guild=discord.Object(id=1547347069918904401)
)
async def botinfo(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 Devion",
        description="Bot oficial da Dev Community."
    )

    embed.add_field(
        name="🆔 ID",
        value=str(bot.user.id),
        inline=True
    )

    embed.add_field(
        name="👥 Servidores",
        value=str(len(bot.guilds)),
        inline=True
    )

    embed.add_field(
        name="⚙️ Biblioteca",
        value=f"discord.py {discord.__version__}",
        inline=True
    )

    embed.add_field(
        name="💻 Desenvolvido para",
        value="Dev Community",
        inline=False
    )

    embed.set_thumbnail(url=bot.user.display_avatar.url)
    embed.set_footer(text="Devion • Dev Community")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(
    name="clear",
    description="Apaga mensagens do canal",
    guild=GUILD
)
@app_commands.describe(quantidade="Quantidade de mensagens para apagar")
async def clear(interaction: discord.Interaction, quantidade: int):

    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message(
            "❌ Você precisa da permissão **Gerenciar Mensagens**.",
            ephemeral=True
        )
        return

    if quantidade < 1 or quantidade > 100:
        await interaction.response.send_message(
            "❌ Escolha uma quantidade entre **1 e 100**.",
            ephemeral=True
        )
        return

    await interaction.response.defer(ephemeral=True)

    apagadas = await interaction.channel.purge(limit=quantidade)

    await interaction.followup.send(
        f"🧹 **{len(apagadas)} mensagens** foram apagadas.",
        ephemeral=True
    )

@bot.tree.command(
    name="kick",
    description="Expulsa um membro do servidor",
    guild=GUILD
)
@app_commands.describe(membro="Membro que será expulso", motivo="Motivo da expulsão")
async def kick(
    interaction: discord.Interaction,
    membro: discord.Member,
    motivo: str = "Nenhum motivo informado"
):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message(
            "❌ Você precisa da permissão **Expulsar Membros**.",
            ephemeral=True
        )
        return

    if membro == interaction.user:
        await interaction.response.send_message(
            "❌ Você não pode expulsar a si mesmo.",
            ephemeral=True
        )
        return

    if membro == interaction.guild.owner:
        await interaction.response.send_message(
            "❌ Você não pode expulsar o dono do servidor.",
            ephemeral=True
        )
        return

    if membro.top_role >= interaction.user.top_role:
        await interaction.response.send_message(
            "❌ Você não pode expulsar alguém com cargo igual ou superior ao seu.",
            ephemeral=True
        )
        return

    try:
        await membro.kick(reason=motivo)

        await interaction.response.send_message(
            f"👢 **{membro}** foi expulso do servidor.\n"
            f"**Motivo:** {motivo}"
        )

    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Não tenho permissão para expulsar esse membro.",
            ephemeral=True
        )
@bot.tree.command(
    name="ban",
    description="Bane um membro do servidor",
    guild=GUILD
)
@app_commands.describe(membro="Membro que será banido", motivo="Motivo do banimento")
async def ban(
    interaction: discord.Interaction,
    membro: discord.Member,
    motivo: str = "Nenhum motivo informado"
):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message(
            "❌ Você precisa da permissão **Banir Membros**.",
            ephemeral=True
        )
        return

    if membro == interaction.user:
        await interaction.response.send_message(
            "❌ Você não pode banir a si mesmo.",
            ephemeral=True
        )
        return

    if membro == interaction.guild.owner:
        await interaction.response.send_message(
            "❌ Você não pode banir o dono do servidor.",
            ephemeral=True
        )
        return

    if membro.top_role >= interaction.user.top_role:
        await interaction.response.send_message(
            "❌ Você não pode banir alguém com cargo igual ou superior ao seu.",
            ephemeral=True
        )
        return

    try:
        await membro.ban(reason=motivo)

        await interaction.response.send_message(
            f"🔨 **{membro}** foi banido do servidor.\n"
            f"**Motivo:** {motivo}"
        )

    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Não tenho permissão para banir esse membro.",
            ephemeral=True
        )
@bot.tree.command(
    name="unban",
    description="Desbane um usuário do servidor",
    guild=GUILD
)
@app_commands.describe(
    user_id="ID do usuário que será desbanido",
    motivo="Motivo do desbanimento"
)
async def unban(
    interaction: discord.Interaction,
    user_id: str,
    motivo: str = "Nenhum motivo informado"
):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message(
            "❌ Você precisa da permissão **Banir Membros**.",
            ephemeral=True
        )
        return

    try:
        user = await bot.fetch_user(int(user_id))
    except (ValueError, discord.NotFound):
        await interaction.response.send_message(
            "❌ ID de usuário inválido.",
            ephemeral=True
        )
        return

    try:
        await interaction.guild.unban(user, reason=motivo)

        await interaction.response.send_message(
            f"🔓 **{user}** foi desbanido do servidor.\n"
            f"**Motivo:** {motivo}"
        )

    except discord.NotFound:
        await interaction.response.send_message(
            "❌ Esse usuário não está banido.",
            ephemeral=True
        )

    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Não tenho permissão para desbanir usuários.",
            ephemeral=True
        )
@bot.tree.command(
    name="mute",
    description="Silencia um membro temporariamente",
    guild=GUILD
)
@app_commands.describe(
    membro="Membro que será silenciado",
    minutos="Tempo do silêncio em minutos",
    motivo="Motivo do silêncio"
)
async def mute(
    interaction: discord.Interaction,
    membro: discord.Member,
    minutos: int,
    motivo: str = "Nenhum motivo informado"
):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message(
            "❌ Você precisa da permissão **Moderar Membros**.",
            ephemeral=True
        )
        return

    if minutos < 1 or minutos > 40320:
        await interaction.response.send_message(
            "❌ O tempo deve ser entre **1 e 40320 minutos**.",
            ephemeral=True
        )
        return

    if membro == interaction.user:
        await interaction.response.send_message(
            "❌ Você não pode silenciar a si mesmo.",
            ephemeral=True
        )
        return

    if membro == interaction.guild.owner:
        await interaction.response.send_message(
            "❌ Você não pode silenciar o dono do servidor.",
            ephemeral=True
        )
        return

    if membro.top_role >= interaction.user.top_role:
        await interaction.response.send_message(
            "❌ Você não pode silenciar alguém com cargo igual ou superior ao seu.",
            ephemeral=True
        )
        return

    try:
        from datetime import timedelta

        await membro.timeout(
            timedelta(minutes=minutos),
            reason=motivo
        )

        await interaction.response.send_message(
            f"🔇 **{membro}** foi silenciado por **{minutos} minutos**.\n"
            f"**Motivo:** {motivo}"
        )

    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Não tenho permissão para silenciar esse membro.",
            ephemeral=True
        )
@bot.tree.command(
    name="unmute",
    description="Remove o silêncio de um membro",
    guild=GUILD
)
@app_commands.describe(
    membro="Membro que será desilenciado",
    motivo="Motivo do desilenciamento"
)
async def unmute(
    interaction: discord.Interaction,
    membro: discord.Member,
    motivo: str = "Nenhum motivo informado"
):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message(
            "❌ Você precisa da permissão **Moderar Membros**.",
            ephemeral=True
        )
        return

    try:
        await membro.timeout(None, reason=motivo)

        await interaction.response.send_message(
            f"🔊 **{membro}** não está mais silenciado.\n"
            f"**Motivo:** {motivo}"
        )

    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Não tenho permissão para remover o silêncio desse membro.",
            ephemeral=True
        )
warns = {}

LOG_CHANNEL_ID = 1547351086023843850


async def enviar_log(embed):
    canal = bot.get_channel(LOG_CHANNEL_ID)

    if canal:
        await canal.send(embed=embed)

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    embed = discord.Embed(
        title="🗑️ Mensagem apagada",
        color=discord.Color.red()
    )

    embed.add_field(
        name="👤 Usuário",
        value=message.author.mention,
        inline=True
    )

    embed.add_field(
        name="📍 Canal",
        value=message.channel.mention,
        inline=True
    )

    embed.add_field(
        name="💬 Mensagem",
        value=message.content[:1024] if message.content else "Sem texto",
        inline=False
    )

    await enviar_log(embed)
@bot.tree.command(
    name="warn",
    description="Adverte um membro do servidor",
    guild=GUILD
)
@app_commands.describe(
    membro="Membro que receberá a advertência",
    motivo="Motivo da advertência"
)
async def warn(
    interaction: discord.Interaction,
    membro: discord.Member,
    motivo: str = "Nenhum motivo informado"
):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message(
            "❌ Você precisa da permissão **Moderar Membros**.",
            ephemeral=True
        )
        return

    if membro == interaction.user:
        await interaction.response.send_message(
            "❌ Você não pode advertir a si mesmo.",
            ephemeral=True
        )
        return

    if membro == interaction.guild.owner:
        await interaction.response.send_message(
            "❌ Você não pode advertir o dono do servidor.",
            ephemeral=True
        )
        return

    if membro.top_role >= interaction.user.top_role:
        await interaction.response.send_message(
            "❌ Você não pode advertir alguém com cargo igual ou superior ao seu.",
            ephemeral=True
        )
        return

    if membro.id not in warns:
        warns[membro.id] = []

    warns[membro.id].append({
        "motivo": motivo,
        "moderador": interaction.user.id
    })

    quantidade = len(warns[membro.id])

    embed = discord.Embed(
        title="⚠️ Advertência aplicada",
        color=discord.Color.orange()
    )

    embed.add_field(
        name="👤 Membro",
        value=membro.mention,
        inline=True
    )

    embed.add_field(
        name="📋 Advertências",
        value=f"{quantidade}",
        inline=True
    )

    embed.add_field(
        name="📝 Motivo",
        value=motivo,
        inline=False
    )

    embed.set_footer(
        text=f"Aplicada por {interaction.user}"
    )

    await interaction.response.send_message(embed=embed)
@bot.tree.command(
    name="warnings",
    description="Mostra as advertências de um membro",
    guild=GUILD
)
@app_commands.describe(membro="Membro que terá as advertências consultadas")
async def warnings(
    interaction: discord.Interaction,
    membro: discord.Member
):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message(
            "❌ Você precisa da permissão **Moderar Membros**.",
            ephemeral=True
        )
        return

    lista = warns.get(membro.id, [])

    if not lista:
        await interaction.response.send_message(
            f"✅ **{membro}** não possui nenhuma advertência.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title=f"⚠️ Advertências de {membro}",
        description=f"Total: **{len(lista)}**",
        color=discord.Color.orange()
    )

    for i, advertencia in enumerate(lista, 1):
        moderador = interaction.guild.get_member(advertencia["moderador"])

        embed.add_field(
            name=f"Advertência #{i}",
            value=(
                f"**Motivo:** {advertencia['motivo']}\n"
                f"**Moderador:** {moderador.mention if moderador else 'Desconhecido'}"
            ),
            inline=False
        )

    embed.set_thumbnail(url=membro.display_avatar.url)
    embed.set_footer(text="Devion • Sistema de Moderação")

    await interaction.response.send_message(embed=embed)
@bot.tree.command(
    name="clearwarns",
    description="Remove todas as advertências de um membro",
    guild=GUILD
)
@app_commands.describe(membro="Membro que terá as advertências removidas")
async def clearwarns(
    interaction: discord.Interaction,
    membro: discord.Member
):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message(
            "❌ Você precisa da permissão **Moderar Membros**.",
            ephemeral=True
        )
        return

    if membro.id not in warns or not warns[membro.id]:
        await interaction.response.send_message(
            f"ℹ️ **{membro}** não possui advertências.",
            ephemeral=True
        )
        return

    quantidade = len(warns[membro.id])
    warns[membro.id] = []

    await interaction.response.send_message(
        f"🧹 Foram removidas **{quantidade} advertências** de {membro.mention}."
    )
@bot.tree.command(
    name="lock",
    description="Trava o canal para membros",
    guild=GUILD
)
@app_commands.describe(motivo="Motivo do bloqueio")
async def lock(
    interaction: discord.Interaction,
    motivo: str = "Nenhum motivo informado"
):
    if not interaction.user.guild_permissions.manage_channels:
        await interaction.response.send_message(
            "❌ Você precisa da permissão **Gerenciar Canais**.",
            ephemeral=True
        )
        return

    overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = False

    await interaction.channel.set_permissions(
        interaction.guild.default_role,
        overwrite=overwrite,
        reason=motivo
    )

    await interaction.response.send_message(
        f"🔒 **Canal bloqueado.**\n"
        f"**Motivo:** {motivo}"
    )
@bot.tree.command(
    name="unlock",
    description="Destrava o canal para membros",
    guild=GUILD
)
@app_commands.describe(motivo="Motivo do desbloqueio")
async def unlock(
    interaction: discord.Interaction,
    motivo: str = "Nenhum motivo informado"
):
    if not interaction.user.guild_permissions.manage_channels:
        await interaction.response.send_message(
            "❌ Você precisa da permissão **Gerenciar Canais**.",
            ephemeral=True
        )
        return

    overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = None

    await interaction.channel.set_permissions(
        interaction.guild.default_role,
        overwrite=overwrite,
        reason=motivo
    )

    await interaction.response.send_message(
        f"🔓 **Canal desbloqueado.**\n"
        f"**Motivo:** {motivo}"
    )
@bot.tree.command(
    name="slowmode",
    description="Define o modo lento do canal",
    guild=GUILD
)
@app_commands.describe(
    segundos="Tempo entre mensagens em segundos"
)
async def slowmode(
    interaction: discord.Interaction,
    segundos: int
):
    if not interaction.user.guild_permissions.manage_channels:
        await interaction.response.send_message(
            "❌ Você precisa da permissão **Gerenciar Canais**.",
            ephemeral=True
        )
        return

    if segundos < 0 or segundos > 21600:
        await interaction.response.send_message(
            "❌ Escolha um valor entre **0 e 21600 segundos**.",
            ephemeral=True
        )
        return

    await interaction.channel.edit(slowmode_delay=segundos)

    if segundos == 0:
        await interaction.response.send_message(
            "⚡ **Modo lento desativado.**"
        )
    else:
        await interaction.response.send_message(
            f"🐌 **Modo lento ativado:** {segundos} segundos entre mensagens."
        )
@bot.tree.command(
    name="poll",
    description="Cria uma enquete",
    guild=GUILD
)
@app_commands.describe(
    pergunta="Pergunta da enquete",
    opcao1="Primeira opção",
    opcao2="Segunda opção"
)
async def poll(
    interaction: discord.Interaction,
    pergunta: str,
    opcao1: str,
    opcao2: str
):
    embed = discord.Embed(
        title="📊 Enquete",
        description=f"**{pergunta}**\n\n"
                    f"1️⃣ {opcao1}\n"
                    f"2️⃣ {opcao2}",
        color=discord.Color.blurple()
    )

    embed.set_footer(text=f"Criada por {interaction.user}")

    await interaction.response.send_message(embed=embed)

    mensagem = await interaction.original_response()
    await mensagem.add_reaction("1️⃣")
    await mensagem.add_reaction("2️⃣")
@bot.tree.command(
    name="say",
    description="Faz o Devion enviar uma mensagem",
    guild=GUILD
)
@app_commands.describe(mensagem="Mensagem que o bot irá enviar")
async def say(
    interaction: discord.Interaction,
    mensagem: str
):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message(
            "❌ Você precisa da permissão **Gerenciar Mensagens**.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        "✅ Mensagem enviada.",
        ephemeral=True
    )

    await interaction.channel.send(mensagem)
WELCOME_CHANNEL_ID = 1547349090537574481


@bot.event
async def on_member_join(member):
    canal = bot.get_channel(WELCOME_CHANNEL_ID)

    if canal:
        embed = discord.Embed(
            title="👋 Seja bem-vindo ao Dev Community",
            description=(
                f"Olá, {member.mention}.\n\n"
                "É um prazer ter você por aqui.\n"
                "O **Dev Community** é uma comunidade voltada para programação, "
                "desenvolvimento e tecnologia.\n\n"
                "📌 **Para começar**\n"
                "• Leia as regras do servidor\n"
                "• Confira os canais disponíveis\n"
                "• Participe da comunidade\n"
                "• Compartilhe seus projetos e conhecimentos\n\n"
                "Esperamos que aproveite o servidor."
            ),
            color=discord.Color.blurple()
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Devion • {member.guild.name}")

        await canal.send(embed=embed)
TICKET_CHANNEL_ID = 1547350629448552529


class TicketPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Abrir atendimento",
        emoji="🎫",
        style=discord.ButtonStyle.primary,
        custom_id="devion:abrir_ticket"
    )
    async def abrir_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        canal = interaction.guild.get_channel(TICKET_CHANNEL_ID)

        if canal is None:
            await interaction.response.send_message(
                "❌ Canal de tickets não encontrado.",
                ephemeral=True
            )
            return

        nome = f"🎫・atendimento-{interaction.user.name}".lower()

        thread = await canal.create_thread(
            name=nome[:100],
            type=discord.ChannelType.private_thread,
            auto_archive_duration=10080,
            reason=f"Ticket aberto por {interaction.user}"
        )

        await thread.add_user(interaction.user)

        embed = discord.Embed(
            title="🎫 ATENDIMENTO ABERTO",
            description=(
                f"Olá, {interaction.user.mention}.\n\n"
                "Seu atendimento foi criado com sucesso.\n\n"
                "Explique o que você precisa com o máximo de detalhes "
                "possível. Se necessário, envie prints ou outras informações "
                "que possam ajudar a equipe.\n\n"
                "🟢 **Status:** Em atendimento\n"
                "🔒 **Privacidade:** Tópico privado"
            ),
            color=discord.Color.blurple()
        )

        embed.set_footer(text="Devion • Dev Community")

        await thread.send(
            embed=embed,
            view=TicketView()
        )

        await interaction.response.send_message(
            f"✅ Seu atendimento foi criado: {thread.mention}",
            ephemeral=True
        )


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Fechar atendimento",
        emoji="🔴",
        style=discord.ButtonStyle.danger,
        custom_id="devion:fechar_ticket"
    )
    async def fechar_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        thread = interaction.channel

        if not isinstance(thread, discord.Thread):
            await interaction.response.send_message(
                "❌ Este botão só pode ser usado dentro de um ticket.",
                ephemeral=True
            )
            return

        if not interaction.user.guild_permissions.manage_threads:
            await interaction.response.send_message(
                "❌ Você precisa da permissão **Gerenciar Tópicos**.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            "🔒 **Atendimento encerrado.** Este tópico será arquivado."
        )

        await thread.edit(
            archived=True,
            locked=True,
            reason=f"Ticket fechado por {interaction.user}"
        )

    @discord.ui.button(
        label="Adicionar membro",
        emoji="👤",
        style=discord.ButtonStyle.secondary,
        custom_id="devion:adicionar_membro"
    )
    async def adicionar_membro(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        thread = interaction.channel

        if not isinstance(thread, discord.Thread):
            await interaction.response.send_message(
                "❌ Este botão só pode ser usado dentro de um ticket.",
                ephemeral=True
            )
            return

        if not interaction.user.guild_permissions.manage_threads:
            await interaction.response.send_message(
                "❌ Você precisa da permissão **Gerenciar Tópicos**.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            "👤 **Envie o ID do usuário que deseja adicionar ao ticket.**",
            ephemeral=True
        )

        def check(message):
            return (
                message.author == interaction.user
                and message.channel == thread
                and message.content.isdigit()
            )

        try:
            mensagem = await bot.wait_for(
                "message",
                timeout=60,
                check=check
            )

            membro = interaction.guild.get_member(int(mensagem.content))

            if membro is None:
                await thread.send(
                    "❌ Não encontrei esse membro no servidor."
                )
                return

            await thread.add_user(membro)

            await thread.send(
                f"👤 {membro.mention} foi **adicionado ao atendimento** por "
                f"{interaction.user.mention}."
            )

        except TimeoutError:
            await interaction.followup.send(
                "⌛ Tempo esgotado. Tente novamente.",
                ephemeral=True
            )


@bot.event
async def on_ready():
    bot.add_view(TicketPanelView())
    bot.add_view(TicketView())

    bot.tree.clear_commands(guild=None)
    await bot.tree.sync()
    await bot.tree.sync(guild=GUILD)

    print(f"Devion conectado como {bot.user}")


bot.run(os.getenv("DISCORD_TOKEN"))
