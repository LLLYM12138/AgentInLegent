# coding=utf-8
from liquid import Template

#实体识别prompt
general_system = '''You are a home embodied intelligent robot equipped with a camera. You can get pictures of your indoor environment through the camera.
Your task is to generate a textual description of an interior photo taken by the camera based on that photo.
'''
general = '''
Task Description:
You are a home embodied intelligent robot equipped with a camera. You can get pictures of your indoor environment through the camera.
Your task is to generate a textual description of an interior photo taken by the camera based on that photo.
You need to focus on the spatial relationships between the objects and furniture in the interior, while ignoring: the texture and texture of the objects, the details of fixed decorations such as walls and floors. The description needs to use simple, plain language and avoid complex rhetorical devices.
The description should list the location of individual pieces of furniture in detail and then indicate small objects placed on top or peripheral moveable items.
 At the end of the description, include a list of all movable or interactive objects within the picture (e.g., usable furniture, tabletop items, etc.).

Notes:
Emphasise Spatial Relationships: focus on describing the relative position and layout between furniture and objects.
Small Object Identification: pay special attention and list all identifiable small objects, e.g., pen holders on desktops, book covers on shelves, etc.
Ignore Texture and Decoration: do not describing the material of the object or the features of the walls or floors.
Use concise language: use direct, easy-to-understand vocabulary and sentence structure.
List moveable/interactive objects: at the end of the description, clearly list all moveable or interactive items in the picture.

An example Output:
This family room has a queen-size bed in the center, next to a tall wardrobe with half-open doors.
Across from the bed is a rectangular dining table with bowls and plates and four chairs around it.
On the table, a white porcelain plate with a few apples is on the right side, while an empty glass is on the left.
Near the table, a black refrigerator stands against the wall.
On the opposite side, a brown sofa faces a TV stand, which holds a TV, a remote control, and a few magazines.
Movable or Interactable Objects: [bed, wardrobe, door, table, bowls, plates, chairs, apples, glass, fridge, sofa, TV, remote control, magazines]

Can you do this for the following picture:
'''
chinese_identify_system = '''
你是一个能够分析图像并根据图像内容回答问题的视觉理解智能助手。
我将提供给你室内家居场景拍摄的一张图片，你的任务是根据我提供的图片生成对应室内家居场景的文本描述。
'''
identify_system = '''
You are a visual understanding intelligent assistant capable of analyzing images and answering questions based on their content.
I will provide you with a picture taken in an indoor home setting, and your task is to generate a corresponding text description of the indoor home scene based on the picture I provide.
'''
chinese_identify_user = '''
你需要关注室内物体和家具之间的空间关系，同时忽略：物体的质地和纹理，墙壁、地板和门窗等固定装饰的细节。描述需要使用简单明了的语言，避免复杂的修辞手法。
描述应详细列出单个家具的位置，然后指出放置在顶部或外围可移动物品上的小物体。
在描述的最后，用json形式列出图片中所有对象的列表（可用的家具、桌面物品等）以及这些对象的属性，如颜色、材质等。

注意事项：
小物件识别：特别注意并列出所有可识别的小物件，例如桌面上的笔架、书架上的书皮等。
忽略纹理和装饰：不要描述墙壁、地板和门窗的特征，也不要把这些对象作为识别结果。
使用精确而简洁的语言：不要输出模糊或概括性的名称，如“白色方块”等。使用直接、易于理解的词汇和句子结构。
按个体输出所有物体：如果同一种物体有多个，如椅子、碗、衣服等，也要分别列出。可以分别命名为“椅子1”、“椅子2”等。
以json格式列出所有物品以及物品的描述性属性：在输出最后以严格的json形式列出图片中的家具和物品以及属性。

输入：室内家居场景的一张图片。
输出示例：
这间家庭房的中心有一张大号床，旁边是一个半开门的衣柜。
床对面是一张长方形的餐桌，周围摆放着碗、盘和两把椅子。
桌子上，右边放着一只盛着几个苹果的白瓷盘，左边放着一个空杯子。
在桌子旁边，一个黑色的冰箱靠墙放着。
所有物体：
[
    {
        "名称":"床",
        "属性":{"颜色":"蓝色","材质":"木质"}
    },
    {
        "名称": "衣柜",
        "属性": {"颜色": "白色蓝色相间","样式": "西式衣柜"}
    },
    {
        "名称": "桌子",
        "属性": {"颜色": "黄色","材质": "木质"}
    },
    {
        "名称": "杯子",
        "属性": {"颜色": "透明","形状":"高脚杯"}
    },
    {
        "名称": "盘子",
        "属性": {"颜色": "白色","材质": "陶瓷"}
    },
    {
        "名称": "椅子1",
        "属性": {"颜色": "黄色","材质": "木质"}
    },
    {
        "名称": "椅子2",
        "属性": {"颜色": "黄色","材质": "木质"}
    },
    {
        "名称": "苹果1",
        "属性": {"颜色": "红色"}
    },
    {
        "名称": "苹果2",
        "属性": {"颜色": "红色"}
    },
    {
        "名称": "冰箱",
        "属性": {"颜色": "白色"}
    }
]

输入图片如下，逐步思考并按要求给出结果：
'''
identify_user = '''
You need to pay attention to the spatial relationship between indoor objects and furniture, while ignoring the texture and texture of objects, and the details of fixed decoration such as walls, floors, doors and windows. Description needs to use simple and clear language to avoid complex rhetoric.
The description should detail the location of individual furniture, and then point out the small objects placed on the top or peripheral movable items.
At the end of the description, the list of all objects in the picture (available furniture, desktop items, etc.) and the attributes of these objects, such as color, material, etc., are listed in JSON form.

Precautions:
Small object identification: pay special attention to and list all identifiable small objects, such as the pen holder on the desktop, the book cover on the bookshelf, etc.
Ignore texture and decoration: do not describe the features of walls, floors, doors and windows, and do not take these objects as recognition results.
Use precise and concise language: do not output vague or general names, such as "white squares". Use words and sentence structures that are direct and easy to understand.
Output all objects by individual: if there are multiple objects of the same kind, such as chairs, bowls, clothes, etc., they should also be listed separately. It can be named "chair 1", "chair 2" and so on.
List all items and descriptive attributes of items in JSON format: at the end of the output, list the furniture, items and attributes in the picture in strict JSON format.

Input: a picture of the indoor home scene.
Output example:
There is a king size bed in the center of this family room and a half open wardrobe next to it.
Opposite the bed is a rectangular dining table, surrounded by bowls, plates and two chairs.
On the table, there is a white porcelain plate with several apples on the right, and an empty cup on the left.
Next to the table, a black refrigerator stood against the wall.
All objects:
[
    {
        "name": "bed",
        "attributes": {"color": "blue", "material": "wood"}
    },
    {
        "name": "Wardrobe",
        "attributes": {"color": "white and blue", "style": "western style Wardrobe"}
    },
    {
        "name": "table",
        "attributes": {"color": "yellow", "material": "wood"}
    },
    {
        "name": "Cup",
        "attributes": {"color": "transparent", "shape": "goblet"}
    },
    {
        "name": "plate",
        "attributes": {"color": "white", "material": "ceramic"}
    },
    {
        "name": "chair 1",
        "attributes": {"color": "yellow", "material": "wood"}
    },
    {
        "name": "chair 2",
        "attributes": {"color": "yellow", "material": "wood"}
    },
    {
        "name": "apple 1",
        "attributes": {"color": "red"}
    },
    {
        "name": "Apple 2",
        "attributes": {"color": "red"}
    },
    {
        "name": "refrigerator",
        "attributes": {"color": "white"}
    }
]

Input the picture as follows, think step by step and give the results as required:
'''
# chinese_identify_system_1 = '''
# 请根据给出的不同视角的图片，描述物体的位置，首先描述房间内物体的摆放，然后用一个列表将房间中的物体表述出来，不需要对这个房间的布局进行描述。
# 参考以下示例，严格按照该格式生成结果：
#     床位于房间的中央，床头靠着房间的一面墙，两边各有一个床头柜。台灯放置在每个床头柜上，床头两侧各有一盏。单人沙发椅位于房间的左上角，靠着墙壁摆放。办公桌位于房间左下角靠墙处，桌上有一台电脑，桌旁有一把椅子。白色柜子位于房间的正下方，靠近床尾。暖气片悬挂在房间左侧墙壁的中上部，靠近办公桌。一盆植物放在办公桌旁的地面上，靠墙角处。
#     物体列表：[床, 床头柜（2个）,台灯（2盏）,单人沙发椅,办公桌,电脑,椅子,电视或暖气片,白色柜子,植物,门]
# '''
# chinese_identify_system_2 = '''
# 你是一个3D场景中的AI视觉助手。你需要一步一步的进行分析，首先识别出图片中存在的所有物体，接着构建以json格式表示的场景图。
# 该场景包含一些物体，这些物体构成了一个以json格式表示的场景图。场景图中的每个实体表示一个物体实例，具有类别标签和物体ID。"属性"描述了物体本身的属性，例如“颜色”、“材质”等。"关系"描述了物体与其他物体之间的空间关系。
# 例如，从场景图 {‘沙发-1’: {‘属性’: {‘颜色’: ‘红色’}, ‘关系’: [‘房屋的左中央, ‘椅子的右边-2’, ‘桌子的前面-3’]}, ‘椅子-2’: {‘属性’: {‘颜色’: ‘棕色’}, ‘关系’: [‘房屋的中央’, ‘沙发的左边-1’,]}, ‘桌子-3’: {‘熟悉’: {‘材质’: ‘木质’}, ‘关系’: []}} 我们可以知道：1）沙发是红色的，2）椅子是棕色的，3）桌子是木制的，4）椅子在沙发的左边，5）椅子在桌子的前面，6）沙发在房屋的左中央位置，7）椅子在房屋的中央位置。
# 所有的空间位置关系必须可以从"关系"直接推导，任何带有不确定性的空间关系不能出现在答案中。
# 最后，单独以列表形式列举出所有物品。
# '''

chinese_identify_user_1 = '下面是图片输入：'
#################################################################################################
#################################################################################################
#数据清洗prompt
process_result_system = '''You are a data processing assistant, and your task is to identify entities in home scenarios from given text descriptions. 
Please output your results in a list format, as shown in the example below:
["Entity 1", "Entity 2", ...]
'''

process_result = Template('''
Task Description:
You need to extract entities from given textual descriptions of home scenarios and returning them in a list format.
These entities include, but are not limited to, furniture (such as sofas, beds, tables, etc.), household items (such as cups, books, TVs, etc.), and other objects that may appear in a home.
Your task is to accurately identify and extract all relevant entities mentioned in the text based on the provided descriptions.

Notes:
1.Accuracy: Ensure that the extracted entities match the content in the text descriptions exactly, without omitting or adding any unrelated entities.
2.Completeness: When extracting entities, consider all relevant information in the text descriptions to ensure that the extraction results are comprehensive and complete.
3.Format Specification: The returned results should be presented in a list format. No additional descriptions or explanations are required.

Examples:

    Example 1:
    Input: The living room has a brown sofa, next to which is a round coffee table with a few magazines and a remote control on it.
    Output:[Sofa,Coffee Table,Magazines,Remote Control]
    
    Example 2:
    Input: The bedroom has a double bed, with a lamp and an alarm clock on the bedside table, and the wardrobe is filled with clothes.
    Output:[Double Bed,Bedside Table,Lamp,Alarm Clock,Wardrobe,Clothes]

Here is the given text:
{{text}}

Please output your final results in a list format:
''')

process_chinese_system = '''
你是一名数据处理助手，你的任务是从给定家庭场景的文本描述中识别实体。
请以列表格式输出结果，如下例所示：
["实体 1", "实体 2",...]
'''

process_chinese = Template('''
任务描述：
你需要从给定的家庭场景文本描述中提取实体，并以列表形式返回。
这些实体包括但不限于家具（如沙发、床、桌子等）、家居用品（如杯子、书籍、电视等）以及可能出现在家中的其他物品。
你的任务是根据所提供的描述，准确识别并提取文本中提及的所有相关实体。

注意事项：
1. 准确性：确保提取的实体与文本描述中的内容完全匹配，不遗漏或添加任何无关实体。
2. 完整性：提取实体时，要考虑文本描述中的所有相关信息，以确保提取结果全面且完整。
3. 格式规范：返回的结果应以列表形式呈现。无需额外的描述或解释。

示例：

示例1：
输入：客厅有一个棕色沙发，沙发旁边是一张圆形咖啡桌，桌上有几本杂志和一个遥控器。
输出：[沙发, 咖啡桌, 杂志, 遥控器]

示例2：
输入：卧室有一张双人床，床头柜上有一盏灯和一个闹钟，衣柜里装满了衣服。
输出：[双人床, 床头柜, 灯, 闹钟, 衣柜, 衣服]

以下是给定文本：
{{text}}

请以列表形式输出你的最终结果：
''')
#################################################################################################
#################################################################################################
#测试准确率/匹配
cal_correct_system = '''
You are a data processing assistant, and your task is to determine whether the given two sets of data match.
'''

cal_correct = Template('''
Task Description:
This task requires you to process two sets of data. The first set of data is a list of household entities, which contain the names of various furniture or household items. The second set of data is a single entity (hereinafter referred to as the target object), which may be the name of a piece of furniture or a household item.
Your task is to determine whether this single target object is in the first set of data or whether it refers to the same item as an entity in the first set of data. If it does, answer "YES"; if it does not, answer "NO".

Notes:
When making a determination, please consider the semantic similarity between entities. As long as the entities may be different names for the same item, you should answer "YES". For example, "sofa" and "three-seater sofa" should be considered as referring to the same item, and "meat" and "roasted chicken" might be different names for the same piece of meat (depending on context), and should also be considered as referring to the same item. However, "sofa" and "dining table" are not.
Please ignore differences in case and punctuation. For example, "bookshelf" and "bookshelf." should be considered as the same entity.
If there is an obvious spelling error or variant between the single entity and an entity in the list, but it can be judged as the same item based on common sense, you should also answer "YES". For example, "coffee table" and "tea table" (assuming "tea table" is a variant or misspelling intended as "coffee table" in this context) should be considered as the same entity.

Input Format:
The first line inputs a list of household entities, with the entities separated by commas, and no extra spaces before or after each entity.
The second line inputs a single entity (i.e., the target object), which is a string.

Output Format:
First, output the thought process. Then, on a new line, output a string that is either "YES" or "NO".

Example 1:
    Input:
        Entity List: bed, sofa, dining table, bookcase
        Target Object: chair
    Output:
        Compare "chair" one by one with "bed", "sofa", "dining table", and "bookcase" in the list. It is found that "chair" does not match any of the entities in the list. Therefore, the final result is:
        NO

Example 2:
    Input:
        Entity List: desk, chair, lamp, bookshelf
        Target Object: desk (with drawers)
    Output:
        Compare "desk (with drawers)" with "desk" in the list. Although the names are different, based on common sense and context, it can be judged that they refer to the same item (i.e., a desk). Therefore, the final result is:
        YES

Please process the following data according to the above rules, think through the steps, and output the results in the specified format:
Entity List: {{list}}
Target Object: {{object}}
''')

cal_correct_chinese_system = '''
你是一名数据处理助手，你的任务是判断所给两组数据之间是否匹配。
'''

cal_correct_chinese = Template('''
任务描述：
本任务要求您处理两组数据。第一组数据是一个家居实体的列表，其中包含多种家具或生活物品的名称。第二组数据是一个单独的实体（下文称为目标对象），可能是家具或生活物品的名称。
您的任务是判断这个单独的目标对象是否在第一组数据中，或者是否与第一组数据中的某个实体代指同一个物品。如果是，则回答“YES”；如果不是，则回答“NO”。

注意事项：
在判断时，请考虑实体之间的语义相似性。只要实体可能是同一物品的不同称谓，就应回答“YES”。例如，“沙发”和“三人沙发”应该被视为代指同一个物品，“肉”和“烤鸡”可能是同一块肉的不同称为，也应视为同意物品。而“沙发”和“餐桌”则不是。
请忽略大小写和标点符号的差异。例如，“书架”和“书架。”应被视为相同的实体。
如果单独实体与列表中的某个实体存在明显的拼写错误或变体，但根据常识可以判断为同一物品，您也应回答“YES”。例如，“茶几”和“茶机”应被视为相同的实体。

输入格式：
第一行输入一个家居实体的列表，列表中的实体以逗号分隔，每个实体前后无多余空格。
第二行输入一个单独的实体（即目标对象），该实体为一个字符串。

输出格式：
先输出思考过程。然后换行输出一个字符串，为“YES”或“NO”。

示例1：
输入：
    实体列表：[床,沙发,餐桌,书柜]
    目标对象：椅子
输出：
    逐一比较“椅子”与列表中的“床”、“沙发”、“餐桌”和“书柜”。发现“椅子”与列表中的任何一个实体都不匹配。因此，最终的结果为：
    NO

示例2：
输入：
    实体列表：[书桌,椅子,台灯,书架]
    目标对象：书桌（带抽屉）
输出：
    比较“书桌（带抽屉）”与列表中的“书桌”。虽然名称上有所不同，但根据常识和语境可以判断它们代指同一个物品（即书桌）。因此，最终的结果为：
    YES

请你按上述规则处理以下数据，逐步思考并按格式输出结果：
实体列表：{{list}}
目标对象：{{object}}
''')
#################################################################################################
#################################################################################################
#实体对齐
entity_alignment_chinese_system = '''
你是一名数据处理助手，你的任务是在给定的两组实体列表之间进行实体对齐。
实体对齐是判断两个或者多个不同来源的实体是否为指向真实世界中同一个对象。如果多个实体表征同一个对象，则在这些实体之间构建对齐关系。
'''
entity_alignment_system = '''
You are a data processing assistant. Your task is to align entities between a given list of two groups of entities.
Entity alignment is to determine whether two or more entities from different sources point to the same object in the real world. If multiple entities represent the same object, an alignment relationship is built between these entities.
'''
#实体属性的匹配: 除了名称外，实体的属性或描述（如颜色、尺寸、材质等）也可能帮助你判断它们是否表征同一个对象。

#附加属性帮助判断:每个输入的对象都附带属性信息，你可以通过判断属性信息的匹配度进行对齐。你的比较顺序应该是：首先判断名称是否匹配，然后再判断颜色是否匹配，最后判断其他属性是否匹配。

entity_alignment_chinese = Template('''
任务描述：
本任务要求您处理两组数据，在存在潜在错误的识别结果列表和真实实体列表之间，通过语义分析，构建严格一对一的对齐关系，并分离出无法匹配的错误实体。
具体来说，你需要在两个列表之间执行实体对齐任务：一个是家居实体识别结果列表（可能包含错误识别），另一个是环境真实实体列表。两个列表都通过json格式给出，且每个实体包括名字和属性等信息。
你的任务是识别出两个列表中表征同一个对象的实体，并在它们之间构建一对一的对齐关系。注意，本任务中实体对齐关系只能是一对一，不能是一对多。任务完成后，你需要输出两个结果：
1.对齐结果：识别结果列表中所有与真实实体列表成功对齐的实体及其对应关系。分行输出，每行一对对齐实体。
2.错误实体列表：识别结果列表中无法与真实实体列表对齐的实体（即错误识别实体），以json格式输出。


注意事项:

实体的语义相似性: 同一个对象可能以不同的名称或描述出现在两个列表中。例如，"沙发"可能在一个列表中被描述为"三人沙发"，而在另一个列表中被描述为"布艺沙发"。
一对一关系: 每个识别结果实体只能与一个真实实体对齐，反之亦然。如果识别结果中有多个实体可能与同一个真实实体匹配，只能选择最匹配的一个。如果识别结果中的实体无法与任何真实实体匹配，则将其归类为错误实体。
实体可能没有属性:输入的实体列表可能没有属性信息，只有名称。在这种情况下，你只需根据名称判断进行对齐。
运用先验知识判断:不要仅仅从字面上判断实体是否匹配，而应该运用你对词语的理解考虑两个词是否有可能指代同一物体。例如，“电视”和“电视柜”虽然部分相似，但并不指代同一物体（电视和柜子不同）。但“茶壶”和“水壶”可能指代同一物体（都是某种壶）。
输出格式: 首先输出思考过程，然后以列表形式给出对齐结果和错误实体列表。注意输出的对齐结果和错误实体列表一定要与输入列表的序号或id、名字、属性完全一致。对齐结果分行输出，每一行代表一对对齐的对象。


输入格式：
第一行输入家居实体识别结果列表，列表中的实体以逗号分隔，每个实体前后无多余空格。
第二行输入环境真实实体列表，格式同上。

输出格式：
先输出思考过程。然后换行输出对齐结果（注意每行一对），然后换行输出错误实体列表。

示例：
输入：
    识别结果列表:
    [
        {
            "物体序号":1,
            "名称": "餐桌",
            "属性": {"材质":"木质","形状":"圆形"}
        },
        {
            "物体序号":2,        
            "名称": "沙发",
            "属性": {"颜色": "灰色","材质": "布料"}
        },
        {
            "物体序号":3,   
            "名称": "椅子",
            "属性": {"颜色": "红色"}
        },
        {
            "物体序号":4,   
            "名称": "冰箱",
            "属性": {"颜色": "白色"}
        }
    ]
    真实实体列表:
    [
        {
            "id":61,
            "名称":"床",
            "属性":{"颜色":"蓝色","材质":"木质"}
        },
        {
            "id":64,
            "名称": "衣柜",
            "属性": {"颜色": "白色蓝色相间","样式": "西式衣柜"}
        },
        {
            "id":65,        
            "名称": "木桌",
            "属性": {"颜色": "黄色","材质": "木质"}
        },
        {
            "id":91,
            "名称": "杯子",
            "属性": {"颜色": "透明","形状":"高脚杯"}
        },
        {
            "id":92,
            "名称": "盘子",
            "属性": {"颜色": "白色","材质": "陶瓷"}
        },
        {
            "id":93,
            "名称": "椅子",
            "属性": {"颜色": "黄色","材质": "木质"}
        },
        {
            "id":94,
            "名称": "苹果",
            "属性": {"颜色": "红色"}
        },
        {
            "id":95,
            "名称": "冰箱",
            "属性": {"颜色": "白色"}
        }
    ]
输出：
    思考过程：
        实体1分析：识别结果中的"餐桌"与真实实体列表中的"木桌"在材质上匹配，"餐桌"和"木桌"都可以代指"桌子"这个物体，名称在语义上相似，认为是同一个物体。
        实体2分析：识别结果中的"沙发"与真实实体列表中的任一对象都不同，判定为错误识别。
        实体3分析：识别结果中的"红色椅子"与真实实体列表中的"蓝色椅子"在颜色上存在冲突，无法匹配。
        实体4分析：识别结果中的"冰箱"与真实实体列表中的"冰箱"在属性上完全匹配，判断匹配。
    对齐结果:
        {"物体序号":1,"名称": "餐桌","属性": {"材质":"木质","形状":"圆形"}} <=> {"id":65,"名称":"桌子","属性": {"颜色": "黄色","材质": "木质"}}
        {"物体序号":4,"名称": "冰箱","属性": {"颜色": "白色"}} <=> {"id":95,"名称": "冰箱","属性": {"颜色": "白色"}}
    错误实体列表:
    [
        {"物体序号":2,"名称": "沙发","属性": {"颜色": "灰色","材质": "布料"}},
        {"物体序号":3,"名称": "椅子","属性": {"颜色": "红色"}}
    ]


再次强调一遍，输出结果中的名称，属性，id必须与输入列表中完全相同。
请你按上述规则处理以下数据，逐步思考并按格式输出结果：
识别结果列表:{{list}}
真实实体列表:{{list_truth}}
''')

#Additional attributes help judge: each input object is attached with attribute information. You can align it by judging the matching degree of attribute information. Your comparison order should be: first judge whether the name matches, then judge whether the color matches, and finally judge whether other attributes match.
#Note that if there are multiple real entities matching from attribute, color, or name, please select one at random.
entity_alignment_user = Template('''
Task description:
This task requires you to process two sets of data, build a strict one-to-one alignment relationship between the identification result list with potential errors and the real entity list through semantic analysis, and separate the unmatched wrong entities.
Specifically, you need to perform entity alignment tasks between two lists: one is the list of household entity recognition results (which may contain false recognition), and the other is the list of environmental real entities. Both lists are given in JSON format, and each entity includes information such as name and attribute.
Your task is to identify the entities representing the same object in two lists and build a one-to-one alignment between them. Note that the entity alignment relationship in this task can only be one-to-one, not one to many. After completing the task, you need to output two results:
1. alignment result: identify all entities in the result list that are successfully aligned with the real entity list and their corresponding relationships. Output in rows, one pair of aligned entities per row.
2. wrong entity list: the entities in the identification result list that cannot be aligned with the real entity list (i.e. wrong identification entities) are output in JSON format.


Precautions:

Semantic similarity of entities: the same object may appear in two lists with different names or descriptions. For example, "sofa" may be described as "three person sofa" in one list and "fabric sofa" in another list.
One to one relationship: each identified result entity can only be aligned with one real entity, and vice versa. If multiple entities in the recognition result may match the same real entity, only the most matching one can be selected.
Entities may have no attributes: The input list of entities may only have names without attribute information. In this case, you only need to make the alignment based on the names.
Use prior knowledge to judge: Do not merely judge whether the entities match based on the literal meaning. Instead, consider whether the two words could possibly refer to the same object by using your understanding of the words. For example, "TV" and "TV cabinet" are partially similar, but they do not refer to the same object (a TV and a cabinet are different). However, "teapot" and "water kettle" might refer to the same object (both are some kind of kettle).
Wrong entity: if the entity in the recognition result cannot match any real entity, it will be classified as wrong entity.
Output format: first output the thinking process, and then give the alignment results and the list of error entities in the form of a list. Note that the output alignment result and the list of error entities must be completely consistent with the serial number or ID, name and attribute of the input list. The alignment results are output in separate lines, and each line represents a pair of aligned objects.


Input format:
In the first line, enter the list of household entity recognition results. The entities in the list are separated by commas, and there are no extra spaces before and after each entity.
In the second line, enter the list of real entities in the environment in the same format as above.

Output format:
Output the thinking process first. Then, line feed output the alignment results (note that each line is a pair), and then line feed output the list of error entities.

Example:
Input:
    List of identification results:
    [
        {
            "object number": 1,
            "name": "dining table",
            "attributes": {"material": "wood", "shape": "circle"}
        },
        {
            "object number": 2,
            "name": "sofa",
            "attributes": {"color": "gray", "material": "cloth"}
        },
        {
            "object number": 3,
            "name": "chair",
            "attributes": {"color": "red"}
        },
        {
            "object number": 4,
            "name": "refrigerator",
            "attributes": {"color": "white"}
        }
    ]
List of real entities:
    [
        {
            "ID":61,
            "name": "bed",
            "attributes": {"color": "blue", "material": "wood"}
        },
        {
            "ID":64,
            "name": "Wardrobe",
            "attributes": {"color": "white and blue", "style": "western style Wardrobe"}
        },
        {
            "ID":65,        
            "name": "wooden table",
            "attributes": {"color": "yellow", "material": "wood"}
        },
        {
            "ID":91,
            "name": "Cup",
            "attributes": {"color": "transparent", "shape": "goblet"}
        },
        {
            "ID":92,
            "name": "plate",
            "attributes": {"color": "white", "material": "ceramic"}
        },
        {
            "ID":93,
            "name": "chair",
            "attributes": {"color": "yellow", "material": "wood"}
        },
        {
            "ID":94,
            "name": "apple",
            "attributes": {"color": "red"}
        },
        {
            "ID":95,
            "name": "refrigerator",
            "attributes": {"color": "white"}
        }
    ]
Output:
    Thinking process:
        Entity 1 Analysis: the "dining table" in the recognition result matches the "wooden table" in the real entity list in terms of material. Both "dining table" and "wooden table" can refer to the object "table". The names are semantically similar and are considered to be the same object.
        Entity 2 Analysis: if the "sofa" in the recognition result is different from any object in the real entity list, it is judged as wrong recognition.
        Entity 3 Analysis: the "red chair" in the recognition result conflicts with the "blue chair" in the real entity list in color and cannot be matched.
        Entity 4 Analysis: the "refrigerator" in the recognition result matches the "refrigerator" in the list of real entities in terms of attributes, and it is judged to match.
    Alignment results:
        {"object number": 1, "name": "table", "attribute": {"material": "wood", "shape": "circle"}} <=> {"ID": 65, "name": "table", "attribute": {"color": "yellow", "material": "wood"}}
        {"object number": 4, "name": "refrigerator", "attribute": {"color": "white"}} <=> {"ID": 95, "name": "refrigerator", "attribute": {"color": "white"}}
    List of error entities:
    [
        {"object number": 2,"name": "sofa","attributes": {"color": "gray", "material": "cloth"}},
        {"object number": 3,"name": "chair","attributes": {"color": "red"}}
    ]


Again, the name, attribute and ID in the output result must be exactly the same as those in the input list.You must strictly follow the format in the example when outputting the result!! Do not add any extra characters or formats!!!
Please process the following data according to the above rules, think step by step and output the results in format:
List of identification results: {{list}}
List of real entities: {{list_truth}}
''')
#################################################################################################
#################################################################################################
#构建图谱
KG_history_chinese_user = Template('''
经过与环境中物体的真实数据对比发现在你的上文实体识别结果中有一些实体是错误的，真实环境中并不存在这些实体。请在接下来的任务中删去这些错误结果。

接下来的任务是分析上文给出的家居图片以及你之前识别出的实体列表（不包括错误结果），构建一个以 JSON 格式表示的场景图。场景图中的每个实体代表一个物体实例，名称应与上文识别列表中保持一致。"属性"字段描述了物体本身的属性（如颜色、材质、形状等），"关系"字段描述了物体与其他物体之间的空间关系。所有空间关系必须明确且可直接从"关系"中推导，任何带有不确定性的空间关系不能出现在结果中。

注意事项：
1. 严格遵从你的实体识别结果：你上文识别出实体列表包括了图片中所有需要处理的物体实例和名称。不要添加上文识别结果中不存在的实体。
2. 不要忽略：不要忽略你的实体识别结果中任何一个没有错误的实体。只要识别结果中的实体没有错误，就必须出现在最终的json结果中，而且名字必须与识别结果中的名字完全一致。你要在思考过程中检查这一点。
2. 注意删去错误实体：不要在接下来的思考过程中考虑我说的错误实体。
3. 每个物体的属性（如颜色、材质、形状等）必须准确描述，且基于图片中的可见信息。
4. 物体之间的空间关系必须明确，且可以直接从图片中推导。
5. 输出必须严格遵循 JSON 格式，包含物体实体、id、属性和关系。

示例：
    输入示例：
        上文识别结果中，错误的实体有：
            [遥控器]
    输出示例：
        根据之前我的文字输出，上文中我识别出的实体列表有：
            [沙发, 椅子, 桌子, 茶几, 遥控器]
        我被告知这些识别结果中[遥控器]是错误的，所以接下来我将删去遥控器，所以我接下来要处理的物体列表是：
            [沙发, 椅子, 桌子, 茶几]                #注：名称必须与识别的实体列表一致
        综合分析最初的图像和这个要构建的实体列表，我给出环境的场景图如下：
            [
                {
                    '实体':'沙发',
                    'id': 1,
                    '属性': {'颜色': '红色'},
                    '关系': [{'关系对象id': 2, '关系':'在椅子的右边'},{'关系对象id': 3, '关系':'在桌子的前面'}]
                },
                {
                    '实体':'椅子',
                    'id': 2,
                    '属性': {'材质': '木质'},
                    '关系': [{'关系对象id': 1, '关系':'在沙发的左边'}]
                },
                {
                    '实体':'桌子',
                    'id': 3,
                    '属性':{'颜色': '棕色'},
                    '关系': [{'关系对象id': 1, '关系':'在沙发的后面'}]
                },
                {
                    '实体':'茶几',
                    'id': 4,
                    '属性':{'形状': '方形'},
                    '关系': []
                },
            ]
示例结束       
  

请参照输出示例中的思考模式，逐步思考并按格式输出结果。
上文识别结果中，错误的实体有：
    [遥控器]
''')
KG_chinese_system = '''
你是一个能够分析图像并根据图像内容回答问题的视觉理解智能助手。
'''
KG_system = '''
You are a visual understanding intelligent assistant that can analyze images and answer questions according to image content.
'''
KG_chinese_user = Template('''
任务描述：
我将提供给你室内家居场景拍摄的一张图片，以及这个场景中存在的实体列表。你的任务是分析我提供的这些图片和实体列表，并据此构建一个以 JSON 格式表示的空间场景图谱。
场景图谱由关系列表构成，"关系"字段描述了物体与其他物体之间的空间关系。每个关系包括了关系序号，构成关系的头实体和尾实体，关系类型，关系的描述。
关系的形式一般可以表示为（头实体，关系，尾实体）。头实体是指关系三元组中的起始实体，通常用于表示关系中的主体或发起者；尾实体是指关系三元组中的目标实体或客体，用于表示关系中头实体的关联对象或动作的接受者。
    比如，“衣服在柜子里”这个关系，头实体是“衣服”，尾实体是“柜子”，关系类型是“on”（在...上方）。
在本任务中，你只需要识别in与on两种空间关系。"in"关系是指一个实体在另一个实体的内部，比如“衣服在柜子里”或“食物在冰箱里”。"on"关系是指一个实体在另一个实体表面上，比如“遥控器在桌子上”、“蛋糕在盘子上”等等。
所有空间关系必须明确且可直接从"关系"中推导，任何带有不确定性的空间关系不能出现在结果中。

注意事项：
实体列表：输入会提供一个实体列表，包含图片中所有需要处理的实体以及实体的属性（如颜色，材质等）。你输出场景图中的实体必须仅来自我提供的实体列表，不能自己编造实体。
只识别in与on：本任务只需要你识别in与on两种任务关系，请严格按照定义识别in和on关系，不要识别其他关系。
JSON 格式：输出必须严格遵循 JSON 格式，由若干个关系构成关系列表。每个关系包含关系序号、构成关系的头实体和尾实体、关系类型、关系内容、描述。
    注意，输出的实体id、名称一定要与输入列表的实体id、名称完全一致。
关系描述中实体顺序：注意保证关系属性中头实体和尾实体之间的正确顺序。比如“遥控器在桌子上”是正确描述，但“桌子在遥控器上”是错误的，所以头实体应该是“遥控器”,尾实体应该是“桌子”。


示例
    输入：
        场景中存在的实体列表：
            [
                {
                    'id': 50,                    
                    '名称':'衣服',
                    '属性': {'颜色': '黑色','材质':'羊毛'},
                },
                {
                    'id': 51,                
                    '名称':'衣柜',
                    '属性': {'颜色': '白色','材质': '木质'},
                },
                {
                    'id': 64,                
                    '名称':'椅子',
                    '属性':{'颜色': '黄色'},
                },
                {
                    'id': 65,                
                    '名称':'茶几',
                    '属性':{'颜色':'白色','形状': '方形'},
                },
                {
                    'id': 66,                
                    '名称':'遥控器',
                    '属性':{'颜色': '黑色'},
                }
            ]
        室内家居场景图片如下：一张图片
    输出：
        给定的场景中实体列表为：衣服, 衣柜, 椅子, 茶几, 遥控器
        依次判断实体之间的空间关系，可以发现：
            衣服在衣柜里，所以关系类型是in；
            遥控器在茶几上，所以关系类型是on。
        因此，生成环境的场景图如下：
            [
                {
                    '关系序号': 1,                
                    '头实体':{'id': 50, '名称':'遥控器'},
                    '尾实体':{'id': 51, '名称':'衣柜'},                  
                    '关系类型': in,
                    '关系描述': "衣服在衣柜里"
                },
                {
                    '关系序号': 2,                
                    '头实体':{'id': 66, '名称':'衣服'},
                    '尾实体':{'id': 65, '名称':'茶几'},                    
                    '关系类型': on,
                    '关系描述': "遥控器在茶几上"
                }
            ]
示例结束

重复一遍，输出的id和名称必须与输入完全一致。
下面请参照输出示例中的思考模式，逐步思考并按格式输出结果。
场景中存在的实体列表为：{{list}}
室内家居场景图片如下：
''')
KG_user = Template('''
Task description:
I will provide you with a picture of the indoor home scene and a list of entities in the scene. Your task is to analyze these pictures and entity lists provided by me and build a spatial scene map in JSON format.
The scene map consists of a list of relationships. The "relationship" field describes the spatial relationship between objects and other objects. Each relationship includes the relationship serial number, the head entity and tail entity constituting the relationship, the relationship type, and the description of the relationship.
The form of relationship can generally be expressed as (head entity, relationship, tail entity). The head entity refers to the starting entity in the relationship triplet, which is usually used to represent the subject or initiator in the relationship; The tail entity refers to the target entity or object in the relational triplet, which is used to represent the associated object or the recipient of the action of the head entity in the relationship.
For example, for the relationship of "clothes in the cabinet", the head entity is "clothes", the tail entity is "cabinet", and the relationship type is "on" Above).
In this task, you only need to identify the two spatial relationships of in and on. "In" relationship means that one entity is inside another entity, such as "clothes in the cabinet" or "food in the refrigerator". "On" relationship means that one entity is on the surface of another entity, such as "remote control on the table", "cake on the plate", etc.
All spatial relationships must be clear and can be derived directly from the "relationship", and any spatial relationship with uncertainty cannot appear in the results.

Precautions:
Entity list: input will provide a list of entities, including all entities to be processed in the picture and the attributes of entities (such as color, material, etc.). The entities in your output scene graph must only come from the entity list provided by me, and you cannot make up entities yourself.
Only identify in and on: this task only requires you to identify the relationship between in and on. Please identify the relationship between in and on in strict accordance with the definition, and do not identify other relationships.
JSON format: the output must strictly follow the JSON format, and the relationship list is composed of several relationships. Each relationship includes relationship sequence number, head entity and tail entity constituting the relationship, relationship type, relationship content and description.
Note that the output entity ID and name must be exactly the same as the entity ID and name of the input list.
Entity order in relation description: pay attention to the correct order between the head entity and the tail entity in relation attributes. For example, "the remote control is on the table" is the correct description, but "the table is on the remote control" is wrong, so the head entity should be "the remote control", and the tail entity should be "the table".


Examples
    Input:
        List of entities in the scene:
            [
                {
                    'ID': 50,
                    'name': 'clothes',
                    'attributes': {'color': 'Black', 'material': 'wool'},
                },
                {
                    'ID': 51,
                    'name': 'wardrobe',
                    'attributes': {'color': 'white', 'material': 'wood'},
                },
                {
                    'ID': 64,
                    'name': 'chair',
                    'attributes': {'color': 'yellow'},
                },
                {
                    'ID': 65,
                    'name': 'coffee table',
                    'attributes': {'color': 'white', 'shape': 'Square'},
                },
                {
                    'ID': 66,
                    'name': 'remote control',
                    'attributes': {'color': 'Black'},
                }
            ]
        The picture of indoor home scene is as follows: one picture
    Output:
        The list of entities in the given scene is: clothes, wardrobe, chair, coffee table, remote control
        Judging the spatial relationship between entities in turn, we can find that:
            The clothes are in the wardrobe, so the relationship type is in;
            The remote control is on the coffee table, so the relationship type is on.
        Therefore, the scenario diagram of the generation environment is as follows:
            [
                {
                    'relationship number': 1,
                    'head entity': {'ID': 50, 'name': 'remote control'},
                    'tail entity': {' ID': 51,' name ':' wardrobe '},
                    'relationship type': in,
                    'relationship description ': "the clothes are in the Wardrobe"
                },
                {
                    'relationship number': 2,
                    'head entity': {'ID': 66, 'name': 'clothes'},
                    'tail entity': {' ID': 65,' name ':' coffee table '},
                    'relationship type': on,
                    'relationship description': "the remote control is on the coffee table"
                }
            ]
End of sample

Repeat, the output ID and name must be exactly the same as the input.
Next, please refer to the thinking mode in the output example to think step by step and output the results in format.
The list of entities in the scene is: {{list}}
Pictures of indoor home scenes are as follows:
''')