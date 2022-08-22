from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, Text, EMPTY_KEYBOARD, KeyboardButtonColor

from states import ChangePostData, ctx
from models.db_api import methods as db


bot = Blueprint('change_post')


@bot.on.private_message(text='Change post <ind>')
async def choose_change(message: Message, ind=None):
    if ind is None:
        await message.answer('Use the command correctly: "Change post <num>"')
        return
    

    keyboard = Keyboard()

    keyboard.add(Text('Title'))
    keyboard.add(Text('Text'))
    keyboard.add(Text('Category'))

    user = await db.get_user(id=message.peer_id)

    if user is None:
        await message.answer('You do not have an account')
        return
    
    posts = await db.get_post(peer=user.num)
    post = None

    if ind.isdigit() and int(ind) > 0 and int(ind) <= len(posts):
        index = int(ind)-1
        post = posts[index]

        await message.answer(f'{str(post)}')
    else:
        await message.answer(f'No post found for number {ind}')
        return
    
    ctx.set(message.peer_id, {'post': post, 'user': user})
    await bot.state_dispenser.set(message.peer_id, ChangePostData.WHAT)
    await message.answer('What do you want to change?', keyboard=keyboard)


@bot.on.private_message(state=ChangePostData.WHAT)
async def enter_change(message: Message):
    keyboard = Keyboard()

    keyboard.add(Text('News'))
    keyboard.add(Text('Gaming'))
    keyboard.add(Text('IT'))
    keyboard.add(Text('Economy'))


    data = ctx.get(message.peer_id)
    data['what'] = message.text.lower()
    ctx.set(message.peer_id, data)
    if message.text in ['Title', 'Text']:
        await message.answer(f'Enter your {message.text.lower()}', keyboard=EMPTY_KEYBOARD)
        await bot.state_dispenser.set(message.peer_id, ChangePostData.CHANGE)
    elif message.text == 'Category':
        await message.answer(f'Choose your {message.text.lower()}', keyboard=keyboard)
        await bot.state_dispenser.set(message.peer_id, ChangePostData.CHANGE)
    else:
        await message.answer('Please choose from keyboard')


@bot.on.private_message(state=ChangePostData.CHANGE)
async def change(message: Message):
    keyboard = Keyboard(one_time=True)

    keyboard.add(Text('Create post'))
    keyboard.add(Text('Back', {'cmd': 'my_posts'}), color=KeyboardButtonColor.NEGATIVE)


    data = ctx.get(message.peer_id)
    what = data['what']
    post = data['post']

    user = await db.get_user(id=message.peer_id)

    text = f'Your post\'s {what} has been changed to {message.text}'


    if what == 'title':
        if len(message.text) > 100:
            await message.answer('Title should not be longer than 100 characters')
            return
        
        await db.edit_post(
            id=post.id,
            peer=user.num,
            title=message.text,
            data=post.data,
            category=post.category
        )
        await bot.state_dispenser.delete(message.peer_id)
        await message.answer(text, keyboard=keyboard)
    

    elif what == 'text':
        await db.edit_post(
            id=post.id,
            peer=user.num,
            title=post.title,
            data=message.text,
            category=post.category
        )
        await bot.state_dispenser.delete(message.peer_id)
        await message.answer(text, keyboard=keyboard)
    
    
    elif what == 'category':
        if message.text not in ['News', 'Gaming', 'IT', 'Economy']:
            await message.answer('Choose from keyboard')
            return
        
        await db.edit_post(
            id=post.id,
            peer=user.num,
            title=post.title,
            data=post.data,
            category=message.text
        )
        await bot.state_dispenser.delete(message.peer_id)
        await message.answer(text, keyboard=keyboard)