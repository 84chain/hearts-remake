import asyncio
import io
import random

import discord
from PIL import Image
from discord.ext import commands

from player.players.aggressive_player import AggressivePlayer
from player.players.game_player import GamePlayer
from setup.setup import *

with open("../../hearts_bot/token.txt") as f:
    token = f.readlines()[0]

bot = commands.Bot(command_prefix=".")


def player_order(id):
    return [id, (id + 1) % 4, (id + 2) % 4, (id + 3) % 4]


def next_first_player(table, played_order):
    for card in table.cards:
        if is_taking(table, card):
            return played_order[table.cards.index(card)]


def display_hand(hand):
    """
    Returns the image of current hand
    :param hand: hand
    :return: png
    """
    file_names = []
    if hand.clubs:
        for c in hand.clubs:
            file_names.append(f"cards/{c.to_short_string()}.png")
    if hand.diamonds:
        for c in hand.diamonds:
            file_names.append(f"cards/{c.to_short_string()}.png")
    if hand.spades:
        for c in hand.spades:
            file_names.append(f"cards/{c.to_short_string()}.png")
    if hand.hearts:
        for c in hand.hearts:
            file_names.append(f"cards/{c.to_short_string()}.png")

    background = Image.new("RGB", (250 * (len(file_names) + 1), 726), (0, 0, 0))

    for i in range(len(file_names)):
        img = Image.open(file_names[i])
        background.paste(img, (250 * i, 0), mask=img)

    return background


def display_table(table):
    table_width = 2200
    table_height = 2200
    cards = table.cards
    players = table.players
    background = Image.new("RGB", (table_width, table_height), (0, 200, 0))

    for i in range(len(cards)):
        id = players[i].id
        if id == 1:
            img = Image.open(f"cards/{cards[i].to_short_string()}.png")
            img = img.transpose(Image.ROTATE_90)
            background.paste(img, (0, round((table_height - img.height) / 2)), mask=img)
        elif id == 3:
            img = Image.open(f"cards/{cards[i].to_short_string()}.png")
            img = img.transpose(Image.ROTATE_270)
            background.paste(img, (table_width - img.width, round((table_height - img.height) / 2)), mask=img)
        elif id == 2:
            img = Image.open(f"cards/{cards[i].to_short_string()}.png")
            background.paste(img, (round((table_width - img.width) / 2), 0), mask=img)
        elif id == 0:
            img = Image.open(f"cards/{cards[i].to_short_string()}.png")
            background.paste(img, (round((table_width - img.width) / 2), table_height - img.height), mask=img)

    return background


def valid_pass(cards, hand):
    valids = []
    for card in cards:
        valids.append(in_hand(card, hand))
    return not bool(len([i for i in valids if not i]))


def isCallerAndCorrect(msg, content):
    def inner(message):
        return message.author == msg.author and message.content.lower()[
                                                :4] == content and message.channel == msg.channel

    return inner


@bot.event
async def on_ready():
    print("rdy")


@bot.command(aliases=["sg1v3"])
async def start(ctx, pass_direction):
    deck = [Card(suit + value) for suit in "cdsh" for value in
            [str(n) for n in range(2, 11)] + ["j", "q", "k", "a"]]
    random.shuffle(deck)

    pass_direction = ["", "r", "a", "l"].index(pass_direction)  # 1, -1, 2
    pass_direction_verbose = ["", "Right", "Across", "Left"][pass_direction]

    hands = [deck[:13], deck[13:26], deck[26:39], deck[39:]]
    player_0 = GamePlayer(0, 0)
    player_1 = AggressivePlayer(1, 1)
    player_2 = AggressivePlayer(2, 2)
    player_3 = AggressivePlayer(3, 3)
    players = [player_0, player_1, player_2, player_3]
    pass_data = []

    # Deal cards
    for i in range(4):
        players[i].deal_hand(hands[i])

    setattr(start, "hand", player_0.hand)

    # Display Hand
    img = display_hand(player_0.hand)
    e = discord.Embed(title="Hand",
                      description=f"Passing {pass_direction_verbose}\nPlease specify which 3 cards to pass with:\n`pass <card1>, <card2>, <card3>`")
    with io.BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        e.set_image(url="attachment://image.png")
        await ctx.send(file=discord.File(fp=image_binary, filename='image.png'), embed=e)

    # Wait for pass
    while True:
        try:
            pass_response = await bot.wait_for("message", check=isCallerAndCorrect(ctx.message, "pass"), timeout=60)
            p_0_pass = [Card(i.strip()) for i in pass_response.content[5:].split(",")]
            if valid_pass(p_0_pass, player_0.hand):
                pass_data.append(p_0_pass)
            else:
                raise IndexError
            break
        except asyncio.TimeoutError:
            await ctx.send("You have taken too long, game aborted")
            return
        except IndexError:
            await ctx.send("You do not have those cards, please try again.")
            pass

    p_0_pass = player_0.pass_cards(p_0_pass)
    p_1_pass = player_1.pass_cards()
    p_2_pass = player_2.pass_cards()
    p_3_pass = player_3.pass_cards()

    pass_data.append(p_1_pass)
    pass_data.append(p_2_pass)
    pass_data.append(p_3_pass)

    if pass_direction == 3:
        player_0.receive_pass(p_3_pass)
        player_1.receive_pass(p_0_pass)
        player_2.receive_pass(p_1_pass)
        player_3.receive_pass(p_2_pass)
        pass_received = p_3_pass
    elif pass_direction == 2:
        player_0.receive_pass(p_2_pass)
        player_1.receive_pass(p_3_pass)
        player_2.receive_pass(p_0_pass)
        player_3.receive_pass(p_1_pass)
        pass_received = p_2_pass
    elif pass_direction == 1:
        player_0.receive_pass(p_1_pass)
        player_1.receive_pass(p_2_pass)
        player_2.receive_pass(p_3_pass)
        player_3.receive_pass(p_0_pass)
        pass_received = p_1_pass

    setattr(start, "hand", player_0.hand)

    # Display Hand after pass
    img = display_hand(player_0.hand)
    e = discord.Embed(title="Hand",
                      description=f"You have received {', '.join([i.to_string() for i in pass_received])}")
    with io.BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        e.set_image(url="attachment://image.png")
        await ctx.send(file=discord.File(fp=image_binary, filename='image.png'), embed=e)

    # Round
    player_with_3 = [player for player in players if in_hand(club_3, player.hand)][0].id
    first_player_order = player_order(player_with_3)
    first_table = Table()
    order_list = []

    for p in range(4):
        c_player = players[first_player_order[p]]

        # If Player's Turn
        if c_player.id == 0:

            # Show table
            img = display_table(first_table)
            e = discord.Embed(title="Round 1", description=f"Your Turn")
            with io.BytesIO() as image_binary:
                img.save(image_binary, 'PNG')
                image_binary.seek(0)
                e.set_image(url="attachment://image.png")
                await ctx.send(file=discord.File(fp=image_binary, filename='image.png'), embed=e)

            # Collect input
            while True:
                try:
                    card_response = await bot.wait_for("message", check=isCallerAndCorrect(ctx.message, "play"),
                                                       timeout=60)
                    card = Card(card_response.content[5:].strip())
                    if in_hand(card, c_player.hand):
                        if first_table.players == []:
                            if card.is_eq(club_3):
                                c_player.play_card(card)
                            else:
                                raise KeyError
                        elif in_hand(card, Hand(c_player.legal_moves(first_table))):
                            c_player.play_card(card)
                    else:
                        raise IndexError
                    break
                except asyncio.TimeoutError:
                    await ctx.send("You have taken too long, game aborted")
                    return
                except IndexError:
                    await ctx.send("You do not have that card, please try again")
                    pass
                except KeyError:
                    await ctx.send("You may not play that card, please try again")
                    pass

        # If not Player's Turn
        else:
            card = c_player.play_card(first_table)
        first_table.card_played(card, c_player)

    # Show table at end of round
    img = display_table(first_table)
    e = discord.Embed(title="Round 1", description="Round Over")
    with io.BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        e.set_image(url="attachment://image.png")
        await ctx.send(file=discord.File(fp=image_binary, filename='image.png'), embed=e)

    # Update
    card_list = []
    for card in first_table.cards:
        card_list.append(card.to_string())
    for p in players:
        p.update_round(first_table)
    setattr(start, "hand", player_0.hand)
    order_list.append(player_order(next_first_player(first_table, first_player_order)))

    # Rounds 2-13
    for rounds in range(2, 14):
        table = Table()
        order = order_list[-1]
        for p in range(4):
            c_player = players[order[p]]
            # If Player's Turn
            if c_player.id == 0:

                # Show table
                img = display_table(table)
                e = discord.Embed(title=f"Round {rounds}", description=f"Your Turn")
                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    e.set_image(url="attachment://image.png")
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'), embed=e)

                # Collect input
                while True:
                    try:
                        card_response = await bot.wait_for("message", check=isCallerAndCorrect(ctx.message, "play"),
                                                           timeout=60)
                        card = Card(card_response.content[5:].strip())
                        if in_hand(card, c_player.hand):
                            if table.players == []:
                                c_player.play_card(card)
                            elif in_hand(card, Hand(c_player.legal_moves(table.first_card))):
                                c_player.play_card(card)
                            else:
                                raise KeyError
                        else:
                            raise IndexError
                        break
                    except asyncio.TimeoutError:
                        await ctx.send("You have taken too long, game aborted")
                        return
                    except IndexError:
                        await ctx.send("You do not have that card, please try again")
                        pass
                    except KeyError:
                        await ctx.send("You may not play that card, please try again")
                        pass

            # If not Player's Turn
            else:
                card = c_player.play_card(table)
            table.card_played(card, c_player)

        # Show table at end of round
        img = display_table(table)
        e = discord.Embed(title=f"Round {rounds}", description="Round Over")
        with io.BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            e.set_image(url="attachment://image.png")
            await ctx.send(file=discord.File(fp=image_binary, filename='image.png'), embed=e)

        # Update
        for card in table.cards:
            card_list.append(card.to_string())
        for p in players:
            p.update_round(table)
        setattr(start, "hand", player_0.hand)
        order_list.append(player_order(next_first_player(table, order)))

    # Count points
    pointdata = []
    for p in players:
        p.count_points()
        pointdata.append([p.id, p.points])

    # Send results
    result = discord.Embed(title="Game Over", description="")
    sorted_results = sorted(pointdata, key=lambda x: x[-1])
    standings = "\n".join(
        [f"Player {i[0]}: {i[-1]} points!" if i[0] != 0 else f"You: {i[-1]} points!" for i in sorted_results])
    result.add_field(name="Results", value=standings)
    if sorted_results[0][0] == 0:
        result.set_footer(text="Nice Job!")
    elif sorted_results[-1][0] == 0:
        result.set_footer(text="You can't even beat the AI? Shame.")
    await ctx.send(embed=result)

    # End game
    return


@bot.command(aliases=["h"])
async def hand(ctx):
    img = display_hand(start.hand)
    e = discord.Embed(title="Hand",
                      description="")
    with io.BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        e.set_image(url="attachment://image.png")
        await ctx.send(file=discord.File(fp=image_binary, filename='image.png'), embed=e)

# bot.run(token)
